from EcoCleanUp import app, db
from flask import render_template, redirect, url_for, request, session, flash


# ============================================================
# Helpers (Admin)
# ============================================================

def admin_required():
    """Return True if current user is logged in and has admin role."""
    return ('loggedin' in session) and (session.get('role') == 'admin')


def access_denied():
    """Standard access denied response."""
    return render_template('access_denied.html'), 403


def require_admin():
    """Common guard: redirect to login if not logged in; otherwise 403 if not admin."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if not admin_required():
        return access_denied()
    return None


# ============================================================
# Admin Home (Dashboard)
# ============================================================

@app.route('/admin/home')
def admin_home():
    """
    Admin dashboard:
    - Quick links
    - Platform-wide summary statistics
    """
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS n FROM events;")
        total_events = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM users WHERE role='volunteer';")
        total_volunteers = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM users WHERE role='event_leader';")
        total_event_leaders = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM users WHERE role='admin';")
        total_admins = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM feedback;")
        total_feedback = cursor.fetchone()['n']

        cursor.execute("SELECT AVG(rating)::numeric(10,2) AS avg_rating FROM feedback;")
        avg_rating = cursor.fetchone()['avg_rating']

    return render_template(
        'admin/admin_home.html',
        total_events=total_events,
        total_volunteers=total_volunteers,
        total_event_leaders=total_event_leaders,
        total_admins=total_admins,
        total_feedback=total_feedback,
        avg_rating=avg_rating)


# ============================================================
# View Users + Filter/Search (full name / role / status)
# ============================================================

@app.route('/admin/users')
def admin_users():
    """
    Admin can view all users with role and status.
    Supports filters:
    - full name keyword
    - role
    - status (active/inactive)
    """
    guard = require_admin()
    if guard:
        return guard

    keyword = request.args.get('keyword', '').strip()
    role = request.args.get('role', '').strip()
    status = request.args.get('status', '').strip()

    sql = """
        SELECT user_id, username, full_name, role, status, contact_number
        FROM users
        WHERE 1=1
    """
    params = []

    if keyword:
        sql += " AND (full_name ILIKE %s OR username ILIKE %s)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    if role:
        sql += " AND role = %s"
        params.append(role)

    if status:
        sql += " AND status = %s"
        params.append(status)

    sql += " ORDER BY user_id ASC;"

    with db.get_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        users = cursor.fetchall()

    return render_template(
        'admin/users_list.html',
        users=users,
        keyword=keyword,
        role=role,
        status=status)


# ============================================================
# Change user status (active/inactive)
# ============================================================

@app.route('/admin/users/<int:user_id>/status', methods=['POST'])
def admin_change_user_status(user_id):
    """Admin can activate/deactivate users."""
    guard = require_admin()
    if guard:
        return guard

    new_status = request.form.get('status', '').strip()
    if new_status not in ('active', 'inactive'):
        flash("Invalid status.", "warning")
        return redirect(request.referrer or url_for('admin_users'))

    with db.get_cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET status = %s
            WHERE user_id = %s;
        """, (new_status, user_id))

    flash("User status updated.", "success")
    return redirect(request.referrer or url_for('admin_users'))




# ============================================================
# Admin: Volunteer participation history (past events + attendance)
# ============================================================

@app.route('/admin/participation-history')
def admin_participation_history():
    """
    Admin view: participation summary for ALL volunteers.
    Similar to leader participation history.
    """
    guard = require_admin()
    if guard:
        return guard

    keyword = request.args.get('keyword', '').strip()

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT
                u.user_id AS volunteer_id,
                COALESCE(u.full_name, u.username) AS full_name,
                u.contact_number,

                -- total joined = count of registrations excluding soft removed
                COALESCE(reg.total_joined, 0) AS total_joined,

                -- total attended = attended count excluding soft removed
                COALESCE(reg.total_attended, 0) AS total_attended
            FROM users u
            LEFT JOIN (
                SELECT
                    volunteer_id,
                    COUNT(*) AS total_joined,
                    SUM(CASE WHEN attendance = 'attended' THEN 1 ELSE 0 END) AS total_attended
                FROM eventregistrations
                WHERE COALESCE(attendance, 'registered') <> 'cancelled'
                GROUP BY volunteer_id
            ) reg ON reg.volunteer_id = u.user_id
            WHERE u.role = 'volunteer'
              AND (%s = '' OR u.full_name ILIKE %s OR u.username ILIKE %s)
            ORDER BY full_name ASC;
        """, (keyword, f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()

    return render_template(
        'admin/participation_history.html',
        rows=rows,
        keyword=keyword,
        active_page='users'
    )
@app.route('/admin/users/<int:user_id>/history')
def admin_user_history(user_id):
    """
    Admin view: participation history for a volunteer.
    Shows past events the volunteer participated in, including attendance status.
    """
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT user_id,
                   COALESCE(full_name, username) AS full_name,
                   role,
                   status
            FROM users
            WHERE user_id = %s;
        """, (user_id,))
        volunteer = cursor.fetchone()

        if not volunteer:
            flash("User not found.", "warning")
            return redirect(url_for('admin_users'))

        if volunteer['role'] != 'volunteer':
            flash("Participation history is available for volunteers only.", "warning")
            return redirect(url_for('admin_users'))

        cursor.execute("""
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time,
                   r.attendance
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND (e.event_date::timestamp + e.start_time) <= NOW()
            ORDER BY e.event_date DESC, e.start_time DESC;
        """, (user_id,))
        history = cursor.fetchall()

    return render_template(
        'admin/user_history.html',
        volunteer=volunteer,
        history=history,
        user_id=user_id)

# ============================================================
# Manage Events (Admin sees ALL events)
# ============================================================

@app.route('/admin/events')
def admin_events():
    """
    Admin: manage all events with filters.
    Filters:
    - scope: all | upcoming | past (based on start datetime)
    - date_from, date_to (date-only)
    - location
    - event_type
    - leader_id
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return access_denied()

    # -------------------- Read filters --------------------
    scope = request.args.get('scope', 'all').strip().lower()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    location = request.args.get('location', '').strip()
    event_type = request.args.get('event_type', '').strip()
    leader_id = request.args.get('leader_id', '').strip()  # string from query

    # -------------------- Base SQL --------------------
    sql = """
        SELECT e.event_id, e.event_name, e.location, e.event_type,
               e.event_date, e.start_time, e.end_time, e.duration,
               e.event_leader_id,
               COALESCE(u.full_name, u.username) AS leader_name
        FROM events e
        LEFT JOIN users u ON u.user_id = e.event_leader_id
        WHERE 1=1
    """
    params = []

    # -------------------- Scope filter --------------------
    if scope == 'upcoming':
        sql += " AND (e.event_date::timestamp + e.start_time) > NOW()"
    elif scope == 'past':
        sql += " AND (e.event_date::timestamp + e.start_time) <= NOW()"

    # -------------------- Date range filter --------------------
    if date_from:
        sql += " AND e.event_date >= %s"
        params.append(date_from)

    if date_to:
        sql += " AND e.event_date <= %s"
        params.append(date_to)

    # -------------------- Location filter --------------------
    if location:
        sql += " AND e.location = %s"
        params.append(location)

    # -------------------- Type filter --------------------
    if event_type:
        sql += " AND e.event_type = %s"
        params.append(event_type)

    # -------------------- Leader filter --------------------
    if leader_id:
        try:
            leader_id_int = int(leader_id)
            sql += " AND e.event_leader_id = %s"
            params.append(leader_id_int)
        except Exception:
            leader_id = ''  # ignore invalid leader id

    sql += " ORDER BY e.event_date DESC, e.start_time DESC;"

    with db.get_cursor() as cursor:
        # 1) Events list
        cursor.execute(sql, tuple(params))
        events = cursor.fetchall()

        # 2) Type dropdown options
        cursor.execute("""
            SELECT DISTINCT event_type
            FROM events
            WHERE event_type IS NOT NULL
            ORDER BY event_type;
        """)
        types = cursor.fetchall()

        # 3) Location dropdown options
        cursor.execute("""
            SELECT DISTINCT location
            FROM events
            WHERE location IS NOT NULL AND TRIM(location) <> ''
            ORDER BY location;
        """)
        locations = cursor.fetchall()

        # 4) Leader dropdown options (event leaders only)
        cursor.execute("""
            SELECT user_id, COALESCE(full_name, username) AS leader_name
            FROM users
            WHERE role = 'event_leader'
            ORDER BY leader_name ASC;
        """)
        leaders = cursor.fetchall()

    return render_template(
        'admin/events_manage.html',
        events=events,
        types=types,
        locations=locations,
        leaders=leaders,
        scope=scope,
        date_from=date_from,
        date_to=date_to,
        location=location,
        event_type=event_type,
        leader_id=leader_id)

@app.route('/admin/events/<int:event_id>/volunteers')
def admin_event_volunteers(event_id):
    """Admin view: list of volunteers registered for a particular event."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return access_denied()

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time, e.location,
                   COALESCE(u.full_name, u.username) AS leader_name
            FROM events e
            LEFT JOIN users u ON u.user_id = e.event_leader_id
            WHERE e.event_id = %s;
        """, (event_id,))
        event = cursor.fetchone()

        if not event:
            flash("Event not found.", "warning")
            return redirect(url_for('admin_events'))

        cursor.execute("""
            SELECT r.volunteer_id,
                   COALESCE(u.full_name, u.username) AS full_name,
                   u.contact_number,
                   u.status,
                   r.attendance
            FROM eventregistrations r
            JOIN users u ON u.user_id = r.volunteer_id
            WHERE r.event_id = %s
            ORDER BY full_name ASC;
        """, (event_id,))
        volunteers = cursor.fetchall()

    return render_template('admin/event_volunteers.html', event=event, volunteers=volunteers)


@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
def admin_edit_event(event_id):
    """Admin can edit any event."""
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE event_id=%s;", (event_id,))
        event = cursor.fetchone()

    if not event:
        flash("Event not found.", "warning")
        return redirect(url_for('admin_events'))

    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        location = request.form.get('location', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        start_time = request.form.get('start_time', '').strip()
        end_time = request.form.get('end_time', '').strip()
        duration = request.form.get('duration', '').strip()
        description = request.form.get('description', '').strip()
        supplies = request.form.get('supplies', '').strip()
        safety_instructions = request.form.get('safety_instructions', '').strip()

        if not event_name or not location or not event_date or not start_time or not end_time:
            flash("Please fill in required fields.", "warning")
            return redirect(url_for('admin_edit_event', event_id=event_id))

        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET event_name=%s, location=%s, event_type=%s, event_date=%s,
                    start_time=%s, end_time=%s, duration=%s, description=%s,
                    supplies=%s, safety_instructions=%s
                WHERE event_id=%s;
            """, (
                event_name, location, event_type or None, event_date,
                start_time, end_time, duration or None, description or None,
                supplies or None, safety_instructions or None,
                event_id
            ))

        flash("Event updated.", "success")
        return redirect(url_for('admin_events'))

    return render_template('admin/event_form.html', event=event)


@app.route('/admin/events/<int:event_id>/cancel', methods=['POST'])
def admin_cancel_event(event_id):
    """Admin cancels an event ."""
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        cursor.execute("DELETE FROM eventregistrations WHERE event_id=%s;", (event_id,))
        cursor.execute("DELETE FROM feedback WHERE event_id=%s;", (event_id,))
        cursor.execute("DELETE FROM events WHERE event_id=%s;", (event_id,))

    flash("Event cancelled (deleted).", "success")
    return redirect(url_for('admin_events'))


# ============================================================
# Platform-wide Reports (summary)
# ============================================================

@app.route('/admin/reports/platform')
def admin_platform_report():
    """Platform-wide report summary for admin."""
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS n FROM events;")
        total_events = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM users WHERE role='volunteer';")
        total_volunteers = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM users WHERE role='event_leader';")
        total_event_leaders = cursor.fetchone()['n']

        cursor.execute("SELECT COUNT(*) AS n FROM feedback;")
        total_feedback = cursor.fetchone()['n']

        cursor.execute("SELECT AVG(rating)::numeric(10,2) AS avg_rating FROM feedback;")
        avg_rating = cursor.fetchone()['avg_rating']

    return render_template(
        'admin/report_platform.html',
        total_events=total_events,
        total_volunteers=total_volunteers,
        total_event_leaders=total_event_leaders,
        total_feedback=total_feedback,
        avg_rating=avg_rating )


# ============================================================
# Event Reports (admin sees all events)
# ============================================================

@app.route('/admin/reports/events')
def admin_event_reports():
    """
    Admin Event Reports (filtered):
    - Attendance summary (registered / attended / absent)
    - Volunteer engagement (feedback count + avg rating)
    Filters:
      date_from, date_to, leader_id, location, event_type
    """
    guard = require_admin()
    if guard:
        return guard

    # -----------------------------
    # Read filters
    # -----------------------------
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    leader_id = request.args.get('leader_id', '').strip()
    location = request.args.get('location', '').strip()
    event_type = request.args.get('event_type', '').strip()

    # -----------------------------
    # Fetch dropdown options
    # -----------------------------
    with db.get_cursor() as cursor:
        # Leaders who have created events
        cursor.execute("""
            SELECT DISTINCT u.user_id, COALESCE(u.full_name, u.username) AS display_name
            FROM events e
            JOIN users u ON u.user_id = e.event_leader_id
            WHERE COALESCE(e.status,'upcoming') <> 'cancelled'
            ORDER BY display_name ASC;
        """)
        leader_options = cursor.fetchall()

        # Locations that exist in events
        cursor.execute("""
            SELECT DISTINCT e.location
            FROM events e
            WHERE e.location IS NOT NULL AND e.location <> ''
              AND COALESCE(e.status,'upcoming') <> 'cancelled'
            ORDER BY e.location ASC;
        """)
        location_options = [row['location'] for row in cursor.fetchall()]

        # Event types that exist in events
        cursor.execute("""
            SELECT DISTINCT e.event_type
            FROM events e
            WHERE e.event_type IS NOT NULL AND e.event_type <> ''
              AND COALESCE(e.status,'upcoming') <> 'cancelled'
            ORDER BY e.event_type ASC;
        """)
        type_options = [row['event_type'] for row in cursor.fetchall()]

    # -----------------------------
    # Base query (pre-aggregate then LEFT JOIN)
    # -----------------------------
    sql = """
        SELECT
            e.event_id,
            e.event_name,
            e.event_date,
            e.location,
            e.event_type,
            COALESCE(u.full_name, u.username) AS leader_name,

            COALESCE(reg.registered_count, 0) AS registered_count,
            COALESCE(reg.attended_count, 0) AS attended_count,
            COALESCE(reg.absent_count, 0) AS absent_count,

            COALESCE(fb.feedback_count, 0) AS feedback_count,
            fb.avg_rating AS avg_rating

        FROM events e
        LEFT JOIN users u ON u.user_id = e.event_leader_id

        LEFT JOIN (
            SELECT
                event_id,
                SUM(CASE WHEN COALESCE(attendance,'registered')='registered' THEN 1 ELSE 0 END) AS registered_count,
                SUM(CASE WHEN attendance='attended' THEN 1 ELSE 0 END) AS attended_count,
                SUM(CASE WHEN attendance='absent' THEN 1 ELSE 0 END) AS absent_count
            FROM eventregistrations
            WHERE COALESCE(attendance,'registered') <> 'cancelled'
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

        WHERE COALESCE(e.status,'upcoming') <> 'cancelled'
    """
    params = []

    # -----------------------------
    # Apply filters
    # -----------------------------
    if date_from:
        sql += " AND e.event_date >= %s"
        params.append(date_from)

    if date_to:
        sql += " AND e.event_date <= %s"
        params.append(date_to)

    if leader_id:
        sql += " AND e.event_leader_id = %s"
        params.append(leader_id)

    if location:
        sql += " AND e.location = %s"
        params.append(location)

    if event_type:
        sql += " AND e.event_type = %s"
        params.append(event_type)

    sql += " ORDER BY e.event_date DESC;"

    with db.get_cursor() as cursor:
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()

    return render_template(
        'admin/report_events.html',
        rows=rows,
        filters={
            'date_from': date_from,
            'date_to': date_to,
            'leader_id': leader_id,
            'location': location,
            'event_type': event_type
        },
        leader_options=leader_options,
        location_options=location_options,
        type_options=type_options,
        active_page='event_reports'
    )


# ============================================================
# Event Reports detail
# ============================================================
@app.route('/admin/reports/events/<int:event_id>')
def admin_event_report_detail(event_id):
    """
    Admin view: detailed report for one event.
    Includes:
    - Event info
    - Attendance summary
    - Volunteer engagement summary (feedback count + avg rating)
    - Volunteer list + attendance
    - Feedback list
    """
    guard = require_admin()
    if guard:
        return guard

    with db.get_cursor() as cursor:
        # ---------------------------------------------------------
        # Event info
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time, e.location,
                   COALESCE(u.full_name, u.username) AS leader_name
            FROM events e
            LEFT JOIN users u ON u.user_id = e.event_leader_id
            WHERE e.event_id=%s;
        """, (event_id,))
        event = cursor.fetchone()

        if not event:
            flash("Event not found.", "warning")
            return redirect(url_for('admin_event_reports'))

        # ---------------------------------------------------------
        # Attendance summary (same logic as reports)
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT
              SUM(CASE WHEN COALESCE(attendance,'registered')='registered' THEN 1 ELSE 0 END) AS registered_count,
              SUM(CASE WHEN attendance='attended' THEN 1 ELSE 0 END) AS attended_count,
              SUM(CASE WHEN attendance='absent' THEN 1 ELSE 0 END) AS absent_count
            FROM eventregistrations
            WHERE event_id=%s
              AND COALESCE(attendance,'registered') <> 'cancelled';
        """, (event_id,))
        att_sum = cursor.fetchone()

        # ---------------------------------------------------------
        # Engagement summary (feedback count + avg rating)
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT
              COUNT(*) AS feedback_count,
              AVG(rating)::numeric(10,2) AS avg_rating
            FROM feedback
            WHERE event_id=%s;
        """, (event_id,))
        fb_sum = cursor.fetchone()

        # ---------------------------------------------------------
        # Volunteers + attendance list (exclude cancelled)
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT r.volunteer_id,
                   COALESCE(u.full_name, u.username) AS full_name,
                   u.contact_number,
                   COALESCE(r.attendance, 'registered') AS attendance
            FROM eventregistrations r
            JOIN users u ON u.user_id = r.volunteer_id
            WHERE r.event_id=%s
              AND COALESCE(r.attendance,'registered') <> 'cancelled'
            ORDER BY full_name ASC;
        """, (event_id,))
        volunteers = cursor.fetchall()

        # ---------------------------------------------------------
        # Feedback list (try with submitted_at; fallback if column doesn't exist)
        # ---------------------------------------------------------
        try:
            cursor.execute("""
                SELECT COALESCE(u.full_name, u.username) AS full_name,
                       f.rating, f.comments, f.submitted_at
                FROM feedback f
                JOIN users u ON u.user_id = f.volunteer_id
                WHERE f.event_id=%s
                ORDER BY f.submitted_at DESC;
            """, (event_id,))
        except Exception:
            cursor.execute("""
                SELECT COALESCE(u.full_name, u.username) AS full_name,
                       f.rating, f.comments
                FROM feedback f
                JOIN users u ON u.user_id = f.volunteer_id
                WHERE f.event_id=%s
                ORDER BY f.rating ASC;
            """, (event_id,))
        feedback_rows = cursor.fetchall()

    return render_template(
        'admin/report_event_detail.html',
        event=event,
        volunteers=volunteers,
        feedback_rows=feedback_rows,
        att_sum=att_sum,
        fb_sum=fb_sum,
        active_page='event_reports')

