from EcoCleanUp import app, db
from flask import redirect, render_template, session, url_for, request, flash


# ============================================================
# Helpers (Leader)
# ============================================================

def leader_required() -> bool:
    """Return True only when the current user is logged in as an event leader."""
    return 'loggedin' in session and session.get('role') == 'event_leader'


def access_denied():
    """Render the access denied page consistently."""
    return render_template('access_denied.html'), 403


def require_leader_login():
    """
    Guard for leader routes.

    Returns:
    - A redirect/response if access is not allowed.
    - None if the user is an authenticated event leader.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if not leader_required():
        return access_denied()
    return None


def parse_positive_int(value: str, default: int = 0) -> int:
    """Parse a positive integer from a string. Returns default if invalid."""
    try:
        x = int(str(value).strip())
        return x if x > 0 else default
    except Exception:
        return default


def get_leader_event_or_404(cursor, leader_id: int, event_id: int):
    """Fetch an event owned by the leader. Returns None if not found."""
    cursor.execute("""
        SELECT e.event_id, e.event_name, e.location, e.event_type,
               e.event_date, e.start_time, e.end_time, e.duration,
               e.description, e.supplies, e.safety_instructions,
               COALESCE(e.status, 'upcoming') AS status
        FROM events e
        WHERE e.event_id = %s AND e.event_leader_id = %s;
    """, (event_id, leader_id))
    return cursor.fetchone()


# ============================================================
# Leader Home (Dashboard)
# ============================================================

@app.route('/leader/home')
def leader_home():
    """
    Leader dashboard page.
    Shows:
    - Upcoming events created by the current leader (start datetime > NOW())
    - Total number of events created by the current leader
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time,
                   e.location, e.event_type, COALESCE(e.status, 'upcoming') AS status
            FROM events e
            WHERE e.event_leader_id = %s
              AND COALESCE(e.status, 'upcoming') <> 'cancelled'
              AND (e.event_date::timestamp + e.start_time) > NOW()
            ORDER BY e.event_date ASC, e.start_time ASC
            LIMIT 8;
        """, (leader_id,))
        upcoming = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM events
            WHERE event_leader_id = %s;
        """, (leader_id,))
        total_events = cursor.fetchone()['total']

    return render_template(
        'leader/leader_home.html',
        upcoming=upcoming,
        total_events=total_events,
        active_page='dashboard'
    )


# ============================================================
# Browse Events (Upcoming + Filters)
# ============================================================

@app.route('/leader/events/browse')
def leader_browse_events():
    """
    Browse cleanup events (leader view).

    Filters (GET):
    - scope: all / upcoming / past
    - date_from / date_to
    - location (exact match)
    - event_type (exact match)
    - leader_id (optional)
    """
    guard = require_leader_login()
    if guard:
        return guard

    current_user_id = session.get('user_id')

    scope = request.args.get('scope', 'all').strip()  # all/upcoming/past
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    location = request.args.get('location', '').strip()
    event_type = request.args.get('event_type', '').strip()
    leader_id = request.args.get('leader_id', '').strip()

    sql = """
        SELECT
            e.event_id, e.event_name, e.event_date, e.start_time, e.end_time,
            e.location, e.event_type,
            COALESCE(e.status, 'upcoming') AS status,
            COALESCE(u.full_name, u.username) AS leader_name,
            (e.event_leader_id = %s) AS is_mine
        FROM events e
        JOIN users u ON u.user_id = e.event_leader_id
        WHERE COALESCE(e.status, 'upcoming') <> 'cancelled'
    """
    params = [current_user_id]

    if scope == 'upcoming':
        sql += " AND e.event_date >= CURRENT_DATE"
    elif scope == 'past':
        sql += " AND e.event_date < CURRENT_DATE"

    if date_from:
        sql += " AND e.event_date >= %s"
        params.append(date_from)

    if date_to:
        sql += " AND e.event_date <= %s"
        params.append(date_to)

    if location:
        sql += " AND e.location = %s"
        params.append(location)

    if event_type:
        sql += " AND e.event_type = %s"
        params.append(event_type)

    if leader_id:
        sql += " AND e.event_leader_id = %s"
        params.append(leader_id)

    sql += " ORDER BY e.event_date ASC, e.start_time ASC;"

    with db.get_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        events = cursor.fetchall()

        cursor.execute("""
            SELECT DISTINCT event_type
            FROM events
            WHERE event_type IS NOT NULL AND TRIM(event_type) <> ''
              AND COALESCE(status, 'upcoming') <> 'cancelled'
            ORDER BY event_type;
        """)
        types = cursor.fetchall()

        cursor.execute("""
            SELECT DISTINCT location
            FROM events
            WHERE location IS NOT NULL AND TRIM(location) <> ''
              AND COALESCE(status, 'upcoming') <> 'cancelled'
            ORDER BY location;
        """)
        locations = cursor.fetchall()

        cursor.execute("""
            SELECT DISTINCT u.user_id, COALESCE(u.full_name, u.username) AS leader_name
            FROM events e
            JOIN users u ON u.user_id = e.event_leader_id
            WHERE COALESCE(e.status, 'upcoming') <> 'cancelled'
            ORDER BY leader_name;
        """)
        leaders = cursor.fetchall()

    return render_template(
        'leader/events_browse.html',
        events=events,
        types=types,
        locations=locations,
        leaders=leaders,
        scope=scope,
        date_from=date_from,
        date_to=date_to,
        event_type=event_type,
        location=location,
        leader_id=leader_id,
        active_page='browse_events'
    )


# ============================================================
# Create Event
# ============================================================

@app.route('/leader/events/create', methods=['GET', 'POST'])
def leader_create_event():
    """
    Create a new cleanup event.
    Required:
    - event_name, location, event_date, start_time, end_time, duration
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        location = request.form.get('location', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        start_time = request.form.get('start_time', '').strip()
        end_time = request.form.get('end_time', '').strip()
        duration = parse_positive_int(request.form.get('duration', '').strip(), default=0)

        description = request.form.get('description', '').strip()
        supplies = request.form.get('supplies', '').strip()
        safety_instructions = request.form.get('safety_instructions', '').strip()

        if not event_name or not location or not event_date or not start_time or not end_time:
            flash("Please fill in required fields (name, location, date, start/end time).", "warning")
            return redirect(url_for('leader_create_event'))

        if duration <= 0:
            flash("Duration must be a positive number (minutes).", "warning")
            return redirect(url_for('leader_create_event'))

        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (
                    event_name, location, event_type, event_date,
                    start_time, end_time, duration, description,
                    supplies, safety_instructions, event_leader_id,
                    status, created_at, updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'upcoming', NOW(), NOW());
            """, (
                event_name,
                location,
                event_type or None,
                event_date,
                start_time,
                end_time,
                duration,
                description or None,
                supplies or None,
                safety_instructions or None,
                leader_id
            ))

        flash("Event created successfully.", "success")
        return redirect(url_for('leader_manage_events'))

    return render_template(
        'leader/event_form.html',
        mode="create",
        event=None,
        active_page='create_event'
    )


# ============================================================
# My Events (Manage: list + edit + cancel)
# ============================================================

@app.route('/leader/events')
def leader_manage_events():
    """
    Manage events created by the current leader.
    Shows:
    - All non-cancelled events (past + future)
    - Edit / Cancel actions
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time, e.duration,
                   COALESCE(e.status, 'upcoming') AS status
            FROM events e
            WHERE e.event_leader_id = %s
              AND COALESCE(e.status, 'upcoming') <> 'cancelled'
            ORDER BY e.event_date DESC, e.start_time DESC;
        """, (leader_id,))
        events = cursor.fetchall()

    return render_template(
        'leader/events_manage.html',
        events=events,
        active_page='my_events'
    )


# ============================================================
# Event Detail
# ============================================================

@app.route('/leader/events/<int:event_id>')
def leader_event_detail(event_id: int):
    """
    Leader event detail:
    - Event info
    - Volunteers list (default hide attendance='cancelled')
    - Attendance summary (exclude cancelled)
    - Outcomes (one per event)
    - Feedback list
    - Optional: show_cancelled=1 to include cancelled volunteers
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    active_tab = request.args.get('tab', 'tab-volunteers')
    show_cancelled = request.args.get('show_cancelled', '0') == '1'

    with db.get_cursor() as cursor:
        # 1) Event (exclude cancelled events)
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time,
                   e.location, e.event_type, e.duration,
                   e.description, e.supplies, e.safety_instructions,
                   COALESCE(e.status, 'upcoming') AS status,
                   e.event_leader_id,
                   COALESCE(u.full_name, u.username) AS leader_name
            FROM events e
            JOIN users u ON u.user_id = e.event_leader_id
            WHERE e.event_id = %s
              AND COALESCE(e.status, 'upcoming') <> 'cancelled';
        """, (event_id,))
        event = cursor.fetchone()

        if not event:
            flash("Event not found.", "warning")
            return redirect(url_for('leader_browse_events'))

        is_mine = (event['event_leader_id'] == leader_id)

        # 2) Volunteers list (default hide cancelled)
        sql = """
            SELECT r.volunteer_id,
                   COALESCE(v.full_name, v.username) AS volunteer_name,
                   v.email,
                   v.contact_number,
                   r.attendance,
                   r.reminder_flag,
                   r.registered_at
            FROM eventregistrations r
            JOIN users v ON v.user_id = r.volunteer_id
            WHERE r.event_id = %s
        """
        params = [event_id]
        if not show_cancelled:
            sql += " AND r.attendance <> 'cancelled'"
        sql += " ORDER BY volunteer_name ASC;"

        cursor.execute(sql, tuple(params))
        volunteers = cursor.fetchall()

        # 3) Outcomes
        cursor.execute("""
            SELECT o.num_attendees,
                   o.bags_collected,
                   o.recyclables_sorted,
                   o.other_achievements,
                   o.recorded_by,
                   o.recorded_at,
                   COALESCE(u2.full_name, u2.username) AS recorder_name
            FROM eventoutcomes o
            JOIN users u2 ON u2.user_id = o.recorded_by
            WHERE o.event_id = %s;
        """, (event_id,))
        outcomes = cursor.fetchone()

        # 4) Feedback (read-only for leader)
        cursor.execute("""
            SELECT f.rating,
                   f.comments,
                   f.submitted_at,
                   COALESCE(v.full_name, v.username) AS volunteer_name
            FROM feedback f
            JOIN users v ON v.user_id = f.volunteer_id
            WHERE f.event_id = %s
            ORDER BY f.submitted_at DESC, f.feedback_id DESC;
        """, (event_id,))
        feedback_list = cursor.fetchall()

        # 5) Summary (exclude cancelled)
        cursor.execute("""
            SELECT
              COUNT(*) AS total_registrations,
              SUM(CASE WHEN attendance = 'registered' THEN 1 ELSE 0 END) AS registered,
              SUM(CASE WHEN attendance = 'attended' THEN 1 ELSE 0 END) AS attended,
              SUM(CASE WHEN attendance = 'absent' THEN 1 ELSE 0 END) AS absent
            FROM eventregistrations
            WHERE event_id = %s
              AND attendance <> 'cancelled';
        """, (event_id,))
        history_summary = cursor.fetchone()

        # 6) Average rating
        cursor.execute("""
            SELECT AVG(rating)::numeric(10,2) AS avg_rating
            FROM feedback
            WHERE event_id = %s;
        """, (event_id,))
        avg_row = cursor.fetchone()
        if history_summary is not None and avg_row is not None:
            history_summary['avg_rating'] = avg_row['avg_rating']

    return render_template(
        'leader/event_detail.html',
        event=event,
        is_mine=is_mine,
        volunteers=volunteers,
        outcomes=outcomes,
        feedback_list=feedback_list,
        history_summary=history_summary,
        active_tab=active_tab,
        show_cancelled=show_cancelled,
        active_page='browse_events'
    )


# ============================================================
# Remove volunteer (soft remove -> attendance='cancelled')
# ============================================================

@app.route('/leader/events/<int:event_id>/volunteers/<int:volunteer_id>/remove', methods=['POST'])
def leader_remove_volunteer(event_id: int, volunteer_id: int):
    """
    Soft remove a volunteer by marking attendance as 'cancelled' (enum-safe).
    IMPORTANT:
    - Volunteer can re-register later IF volunteer side uses UPSERT.
    - Clear reminder flags so removed volunteer won't see reminders.
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        event = get_leader_event_or_404(cursor, leader_id, event_id)
        if not event or event.get('status') == 'cancelled':
            return access_denied()

        cursor.execute("""
            UPDATE eventregistrations
            SET attendance = 'cancelled',
                reminder_flag = FALSE,
                reminder_message = NULL
            WHERE event_id = %s AND volunteer_id = %s;
        """, (event_id, volunteer_id))

    flash("Volunteer removed from the event.", "success")
    return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-volunteers'))


# ============================================================
# Leader: Update attendance (owner-only)
# ============================================================

@app.route('/leader/events/<int:event_id>/attendance', methods=['POST'])
def leader_update_attendance(event_id: int):
    """
    Update attendance for a volunteer in a leader-owned event.
    Allowed: registered / attended / absent / cancelled
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    volunteer_id = request.form.get('volunteer_id', type=int)
    new_status = request.form.get('attendance', type=str)

    allowed_statuses = {'registered', 'attended', 'absent', 'cancelled'}
    if not volunteer_id or not new_status or new_status not in allowed_statuses:
        flash("Invalid attendance update.", "warning")
        return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-attendance'))

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT event_leader_id, COALESCE(status, 'upcoming') AS status
            FROM events
            WHERE event_id = %s;
        """, (event_id,))
        e = cursor.fetchone()

        if not e or e['status'] == 'cancelled':
            flash("Event not found.", "warning")
            return redirect(url_for('leader_browse_events'))

        if e['event_leader_id'] != leader_id:
            flash("You can only update attendance for your own events.", "danger")
            return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-attendance'))

        cursor.execute("""
            UPDATE eventregistrations
            SET attendance = %s
            WHERE event_id = %s AND volunteer_id = %s;
        """, (new_status, event_id, volunteer_id))

    flash("Attendance updated.", "success")
    return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-attendance'))


# ============================================================
# Leader: Record / Update outcomes (owner-only, Upsert)
# ============================================================

@app.route('/leader/events/<int:event_id>/outcomes', methods=['POST'])
def leader_record_outcomes(event_id: int):
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    num_attendees = request.form.get('num_attendees', type=int) or 0
    bags_collected = request.form.get('bags_collected', type=int) or 0
    recyclables_sorted = request.form.get('recyclables_sorted', type=int) or 0
    other_achievements = (request.form.get('other_achievements') or "").strip()

    if num_attendees < 0 or bags_collected < 0 or recyclables_sorted < 0:
        flash("Outcomes values must be non-negative.", "warning")
        return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-outcomes'))

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT event_leader_id, COALESCE(status, 'upcoming') AS status
            FROM events
            WHERE event_id = %s;
        """, (event_id,))
        e = cursor.fetchone()

        if not e or e['status'] == 'cancelled':
            flash("Event not found.", "warning")
            return redirect(url_for('leader_browse_events'))

        if e['event_leader_id'] != leader_id:
            flash("You can only record outcomes for your own events.", "danger")
            return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-outcomes'))

        cursor.execute("""
            INSERT INTO eventoutcomes (
                event_id,
                num_attendees,
                bags_collected,
                recyclables_sorted,
                other_achievements,
                recorded_by,
                recorded_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (event_id)
            DO UPDATE SET
                num_attendees = EXCLUDED.num_attendees,
                bags_collected = EXCLUDED.bags_collected,
                recyclables_sorted = EXCLUDED.recyclables_sorted,
                other_achievements = EXCLUDED.other_achievements,
                recorded_by = EXCLUDED.recorded_by,
                recorded_at = NOW();
        """, (
            event_id,
            num_attendees,
            bags_collected,
            recyclables_sorted,
            other_achievements,
            leader_id
        ))

    flash("Outcomes recorded.", "success")
    return redirect(url_for('leader_event_detail', event_id=event_id, tab='tab-outcomes'))


# ============================================================
# Edit Event (owner-only)
# ============================================================

@app.route('/leader/events/<int:event_id>/edit', methods=['GET', 'POST'])
def leader_edit_event(event_id: int):
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        event = get_leader_event_or_404(cursor, leader_id, event_id)

    if not event or event.get('status') == 'cancelled':
        flash("Event not found or you do not have permission.", "warning")
        return redirect(url_for('leader_manage_events'))

    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        location = request.form.get('location', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        start_time = request.form.get('start_time', '').strip()
        end_time = request.form.get('end_time', '').strip()
        duration = parse_positive_int(request.form.get('duration', '').strip(), default=0)

        description = request.form.get('description', '').strip()
        supplies = request.form.get('supplies', '').strip()
        safety_instructions = request.form.get('safety_instructions', '').strip()

        if not event_name or not location or not event_date or not start_time or not end_time:
            flash("Please fill in required fields (name, location, date, start/end time).", "warning")
            return redirect(url_for('leader_edit_event', event_id=event_id))

        if duration <= 0:
            flash("Duration must be a positive number (minutes).", "warning")
            return redirect(url_for('leader_edit_event', event_id=event_id))

        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET event_name=%s,
                    location=%s,
                    event_type=%s,
                    event_date=%s,
                    start_time=%s,
                    end_time=%s,
                    duration=%s,
                    description=%s,
                    supplies=%s,
                    safety_instructions=%s,
                    updated_at=NOW()
                WHERE event_id=%s AND event_leader_id=%s
                  AND COALESCE(status,'upcoming') <> 'cancelled';
            """, (
                event_name,
                location,
                event_type or None,
                event_date,
                start_time,
                end_time,
                duration,
                description or None,
                supplies or None,
                safety_instructions or None,
                event_id,
                leader_id
            ))

        flash("Event updated successfully.", "success")
        return redirect(url_for('leader_event_detail', event_id=event_id))

    return render_template(
        'leader/event_form.html',
        mode="edit",
        event=event,
        active_page='my_events'
    )


# ============================================================
# Cancel Event (Soft cancel, keep history)
# ============================================================

@app.route('/leader/events/<int:event_id>/cancel', methods=['POST'])
def leader_cancel_event(event_id: int):
    """
    Cancel an event (soft cancel).
    - events.status = 'cancelled'
    - set all attendance='registered' to 'cancelled'
    - clear reminders
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        event = get_leader_event_or_404(cursor, leader_id, event_id)
        if not event:
            return access_denied()

        cursor.execute("""
            UPDATE events
            SET status='cancelled',
                updated_at=NOW()
            WHERE event_id=%s AND event_leader_id=%s;
        """, (event_id, leader_id))

        cursor.execute("""
            UPDATE eventregistrations
            SET attendance='cancelled',
                reminder_flag=FALSE,
                reminder_message=NULL
            WHERE event_id=%s AND attendance='registered';
        """, (event_id,))

    flash("Event cancelled.", "success")
    return redirect(request.referrer or url_for('leader_manage_events'))


# ============================================================
# Volunteers List (owner-only)
# ============================================================

@app.route('/leader/events/<int:event_id>/volunteers')
def leader_event_volunteers(event_id: int):
    """
    Dedicated volunteers list page (owner-only).
    Default hides cancelled.
    Use ?show_cancelled=1 to include cancelled.
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    show_cancelled = request.args.get('show_cancelled', '0') == '1'

    with db.get_cursor() as cursor:
        event = get_leader_event_or_404(cursor, leader_id, event_id)
        if not event or event.get('status') == 'cancelled':
            flash("Event not found or you do not have permission.", "warning")
            return redirect(url_for('leader_manage_events'))

        sql = """
            SELECT r.volunteer_id,
                   COALESCE(u.full_name, u.username) AS full_name,
                   u.email,
                   u.contact_number,
                   r.attendance,
                   r.reminder_flag,
                   r.registered_at
            FROM eventregistrations r
            JOIN users u ON u.user_id = r.volunteer_id
            WHERE r.event_id = %s
        """
        params = [event_id]
        if not show_cancelled:
            sql += " AND r.attendance <> 'cancelled'"
        sql += " ORDER BY full_name ASC;"

        cursor.execute(sql, tuple(params))
        volunteers = cursor.fetchall()

    return render_template(
        'leader/event_volunteers.html',
        event=event,
        volunteers=volunteers,
        show_cancelled=show_cancelled,
        active_page='my_events'
    )


# ============================================================
# Participation History (Leader scope)
# ============================================================

@app.route('/leader/volunteers/history')
def leader_volunteer_history():
    """
    Participation history summary for volunteers across events managed by the current leader.
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    keyword = request.args.get('keyword', '').strip()

    sql = """
        SELECT u.user_id AS volunteer_id,
               COALESCE(u.full_name, u.username) AS full_name,
               u.contact_number,
               COUNT(*) AS total_joined,
               SUM(CASE WHEN r.attendance='attended' THEN 1 ELSE 0 END) AS total_attended,
               SUM(CASE WHEN r.attendance='absent' THEN 1 ELSE 0 END) AS total_absent,
               SUM(CASE WHEN r.attendance='cancelled' THEN 1 ELSE 0 END) AS total_cancelled
        FROM eventregistrations r
        JOIN events e ON e.event_id = r.event_id
        JOIN users u ON u.user_id = r.volunteer_id
        WHERE e.event_leader_id = %s
          AND COALESCE(e.status,'upcoming') <> 'cancelled'
    """
    params = [leader_id]

    if keyword:
        sql += " AND (u.full_name ILIKE %s OR u.username ILIKE %s)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    sql += """
        GROUP BY u.user_id, full_name, u.contact_number
        ORDER BY total_attended DESC, total_joined DESC, full_name ASC;
    """

    with db.get_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()

    return render_template(
        'leader/volunteer_history.html',
        rows=rows,
        keyword=keyword,
        active_page='participation'
    )


@app.route('/leader/volunteers/<int:volunteer_id>/history')
def leader_volunteer_history_detail(volunteer_id: int):
    """
    Detailed participation records for one volunteer (leader scope only).
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT COALESCE(full_name, username) AS full_name, contact_number, email
            FROM users
            WHERE user_id=%s;
        """, (volunteer_id,))
        volunteer = cursor.fetchone()

        if not volunteer:
            flash("Volunteer not found.", "warning")
            return redirect(url_for('leader_volunteer_history'))

        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time,
                   e.location, e.event_type,
                   COALESCE(e.status, 'upcoming') AS event_status,
                   r.attendance
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE e.event_leader_id = %s AND r.volunteer_id = %s
              AND COALESCE(e.status,'upcoming') <> 'cancelled'
            ORDER BY e.event_date DESC, e.start_time DESC;
        """, (leader_id, volunteer_id))
        history = cursor.fetchall()

    return render_template(
        'leader/volunteer_history_detail.html',
        volunteer=volunteer,
        history=history,
        active_page='participation'
    )


# ============================================================
# Event Reminders (Popup on volunteer login)
# ============================================================

@app.route('/leader/events/<int:event_id>/reminder', methods=['POST'])
def leader_send_reminder(event_id: int):
    """
    Send a reminder for an event.
    - Only for upcoming events (status='upcoming' and date >= today)
    - Only to attendance='registered'
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    message = (request.form.get('message') or '').strip()
    if not message:
        message = "Reminder: you have an upcoming cleanup event. Please check details on your dashboard."

    with db.get_cursor() as cursor:
        event = get_leader_event_or_404(cursor, leader_id, event_id)
        if not event or event.get('status') == 'cancelled':
            return access_denied()

        cursor.execute("""
            SELECT 1
            FROM events
            WHERE event_id=%s
              AND event_leader_id=%s
              AND COALESCE(status,'upcoming')='upcoming'
              AND event_date >= CURRENT_DATE;
        """, (event_id, leader_id))
        ok = cursor.fetchone()
        if not ok:
            flash("You can only send reminders for upcoming events.", "warning")
            return redirect(url_for('leader_event_detail', event_id=event_id))

        cursor.execute("""
            UPDATE eventregistrations
            SET reminder_flag = TRUE,
                reminder_message = %s
            WHERE event_id = %s
              AND attendance = 'registered';
        """, (message, event_id))

    flash("Reminder sent (will popup on volunteer login).", "success")
    return redirect(url_for('leader_event_detail', event_id=event_id))


# ============================================================
# Review Feedback (Leader scope)
# ============================================================

@app.route('/leader/feedback')
def leader_review_feedback():
    """
    Review feedback submitted by volunteers for events managed by the current leader.
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT f.event_id,
                   e.event_name,
                   e.event_date,
                   f.volunteer_id,
                   COALESCE(u.full_name, u.username) AS full_name,
                   f.rating,
                   f.comments,
                   f.submitted_at
            FROM feedback f
            JOIN events e ON e.event_id = f.event_id
            JOIN users u ON u.user_id = f.volunteer_id
            WHERE e.event_leader_id = %s
              AND COALESCE(e.status,'upcoming') <> 'cancelled'
            ORDER BY e.event_date DESC, f.rating ASC, f.submitted_at DESC;
        """, (leader_id,))
        rows = cursor.fetchall()

    return render_template(
        'leader/feedback_list.html',
        rows=rows,
        active_page='feedback'
    )


# ============================================================
# Leader: Event Reports (summary list)
# ============================================================

@app.route('/leader/reports')
def leader_reports():
    """
    Report summary list for leader-owned events.
    Includes:
    - registered/attended/absent/cancelled counts
    - feedback count + avg rating
    - outcome recorded + outcome fields
    Filters: date_from/date_to (event_date)
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    sql = """
        SELECT
            e.event_id,
            e.event_name,
            e.event_date,
            e.start_time,
            e.end_time,
            e.location,
            e.event_type,
            COALESCE(e.status, 'upcoming') AS status,

            COALESCE(reg.registered_count, 0) AS registered_count,
            COALESCE(reg.attended_count, 0) AS attended_count,
            COALESCE(reg.absent_count, 0) AS absent_count,
            COALESCE(reg.cancelled_count, 0) AS cancelled_count,

            COALESCE(fb.feedback_count, 0) AS feedback_count,
            fb.avg_rating AS avg_rating,

            (o.outcome_id IS NOT NULL) AS outcome_recorded,
            o.num_attendees,
            o.bags_collected,
            o.recyclables_sorted,
            o.other_achievements,
            o.recorded_at

        FROM events e

        LEFT JOIN (
            SELECT
                event_id,
                SUM(CASE WHEN attendance='registered' THEN 1 ELSE 0 END) AS registered_count,
                SUM(CASE WHEN attendance='attended' THEN 1 ELSE 0 END) AS attended_count,
                SUM(CASE WHEN attendance='absent' THEN 1 ELSE 0 END) AS absent_count,
                SUM(CASE WHEN attendance='cancelled' THEN 1 ELSE 0 END) AS cancelled_count
            FROM eventregistrations
            GROUP BY event_id
        ) reg ON reg.event_id = e.event_id

        LEFT JOIN (
            SELECT
                event_id,
                COUNT(*) AS feedback_count,
                AVG(rating)::numeric(10,2) AS avg_rating
            FROM feedback
            GROUP BY event_id
        ) fb ON fb.event_id = e.event_id

        LEFT JOIN eventoutcomes o ON o.event_id = e.event_id

        WHERE e.event_leader_id = %s
          AND COALESCE(e.status,'upcoming') <> 'cancelled'
    """
    params = [leader_id]

    if date_from:
        sql += " AND e.event_date >= %s"
        params.append(date_from)
    if date_to:
        sql += " AND e.event_date <= %s"
        params.append(date_to)

    sql += " ORDER BY e.event_date DESC, e.start_time DESC;"

    with db.get_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()

    return render_template(
        'leader/report_events.html',
        rows=rows,
        filters={'date_from': date_from, 'date_to': date_to},
        active_page='reports'
    )


# ============================================================
# Leader: Event Report Detail
# ============================================================

@app.route('/leader/reports/events/<int:event_id>')
def leader_event_report_detail(event_id: int):
    """
    Detailed report for one event:
    - event info
    - volunteers list (include cancelled for audit)
    - attendance summary (include cancelled)
    - feedback list + summary
    - outcomes detail
    """
    guard = require_leader_login()
    if guard:
        return guard

    leader_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time,
                   e.location, e.event_type,
                   COALESCE(e.status, 'upcoming') AS status,
                   COALESCE(u.full_name, u.username) AS leader_name
            FROM events e
            LEFT JOIN users u ON u.user_id = e.event_leader_id
            WHERE e.event_id=%s AND e.event_leader_id=%s
              AND COALESCE(e.status, 'upcoming') <> 'cancelled';
        """, (event_id, leader_id))
        event = cursor.fetchone()

        if not event:
            flash("Event not found or you do not have permission.", "warning")
            return redirect(url_for('leader_reports'))

        cursor.execute("""
            SELECT r.volunteer_id,
                   COALESCE(u.full_name, u.username) AS full_name,
                   u.contact_number,
                   u.email,
                   r.attendance,
                   r.registered_at
            FROM eventregistrations r
            JOIN users u ON u.user_id = r.volunteer_id
            WHERE r.event_id=%s
            ORDER BY full_name ASC;
        """, (event_id,))
        volunteers = cursor.fetchall()

        cursor.execute("""
            SELECT
                SUM(CASE WHEN attendance='registered' THEN 1 ELSE 0 END) AS registered_count,
                SUM(CASE WHEN attendance='attended' THEN 1 ELSE 0 END) AS attended_count,
                SUM(CASE WHEN attendance='absent' THEN 1 ELSE 0 END) AS absent_count,
                SUM(CASE WHEN attendance='cancelled' THEN 1 ELSE 0 END) AS cancelled_count
            FROM eventregistrations
            WHERE event_id=%s;
        """, (event_id,))
        att_sum = cursor.fetchone()

        cursor.execute("""
            SELECT COALESCE(u.full_name, u.username) AS full_name,
                   f.rating, f.comments, f.submitted_at
            FROM feedback f
            JOIN users u ON u.user_id = f.volunteer_id
            WHERE f.event_id=%s
            ORDER BY f.submitted_at DESC;
        """, (event_id,))
        feedback_rows = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS feedback_count,
                   AVG(rating)::numeric(10,2) AS avg_rating
            FROM feedback
            WHERE event_id=%s;
        """, (event_id,))
        fb_sum = cursor.fetchone()

        cursor.execute("""
            SELECT
                o.num_attendees,
                o.bags_collected,
                o.recyclables_sorted,
                o.other_achievements,
                o.recorded_at,
                COALESCE(u.full_name, u.username) AS recorded_by_name
            FROM eventoutcomes o
            LEFT JOIN users u ON u.user_id = o.recorded_by
            WHERE o.event_id=%s;
        """, (event_id,))
        outcome = cursor.fetchone()

    return render_template(
        'leader/report_event_detail.html',
        event=event,
        volunteers=volunteers,
        feedback_rows=feedback_rows,
        att_sum=att_sum,
        fb_sum=fb_sum,
        outcome=outcome,
        active_page='reports'
    )