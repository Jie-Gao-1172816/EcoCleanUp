from EcoCleanUp import app, db
from flask import redirect, render_template, request, session, url_for, flash


# ============================================================
# Volunteer: Home (dashboard + reminders)
# ============================================================
@app.route('/volunteer/home')
def volunteer_home():
    """
    Volunteer dashboard:
    - Shows upcoming registered events.
    - Shows reminder popups for reminder-flagged upcoming events.
    - Clears ONLY the reminders that were displayed.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        # Upcoming events for the dashboard
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time, e.location
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND COALESCE(r.attendance,'registered') = 'registered'
              AND (e.event_date::timestamp + e.start_time) > NOW()
            ORDER BY e.event_date ASC, e.start_time ASC
            LIMIT 10;
        """, (user_id,))
        upcoming = cursor.fetchall()

        # Reminder list (only upcoming + flagged)
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.location, r.reminder_message
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND COALESCE(r.attendance,'registered') = 'registered'
              AND r.reminder_flag = TRUE
              AND (e.event_date::timestamp + e.start_time) > NOW()
            ORDER BY e.event_date ASC, e.start_time ASC
            LIMIT 10;
        """, (user_id,))
        reminders = cursor.fetchall()

        # Clear only reminders that were actually displayed
        if reminders:
            reminder_event_ids = [row['event_id'] for row in reminders]
            cursor.execute("""
                UPDATE eventregistrations
                SET reminder_flag = FALSE,
                    reminder_message = NULL
                WHERE volunteer_id = %s
                  AND event_id = ANY(%s);
            """, (user_id, reminder_event_ids))

    return render_template(
        'volunteer/volunteer_home.html',
        upcoming=upcoming,
        reminders=reminders,
        active_page='home'
    )

# ============================================================
# Volunteer: Browse Events + Filter (scope/date/location/type)
# ============================================================
@app.route('/volunteer/events')
def volunteer_events():
    """
    Browse cleanup events with filters:
    - scope: all (default), upcoming, past
    - date_from, date_to
    - location (dropdown)
    - event_type (dropdown)
    Also includes:
    - is_upcoming (derived from start datetime > NOW())
    - my_attendance (registration status, if any)
    - my_feedback_id (feedback existence, if any)
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    # -------------------- Read filters from query string --------------------
    scope = request.args.get('scope', 'all').strip().lower()  # all|upcoming|past
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    location = request.args.get('location', '').strip()
    event_type = request.args.get('event_type', '').strip()

    # -------------------- Base SQL (with my status joins) --------------------
    sql = """
        SELECT
            e.event_id, e.event_name, e.location, e.event_type, e.event_date,
            e.start_time, e.end_time, e.duration,

            -- Event status: upcoming if start datetime > NOW()
            ((e.event_date::timestamp + e.start_time) > NOW()) AS is_upcoming,

            -- My registration status (NULL if not registered)
            r.attendance AS my_attendance,

            -- My feedback existence (NULL if not submitted)
            f.feedback_id AS my_feedback_id

        FROM events e
        LEFT JOIN eventregistrations r
            ON r.event_id = e.event_id
           AND r.volunteer_id = %s
        LEFT JOIN feedback f
            ON f.event_id = e.event_id
           AND f.volunteer_id = %s
        WHERE 1=1
    """
    params = [user_id, user_id]

    # -------------------- Scope filter (start datetime based) --------------------
    if scope == 'upcoming':
        sql += " AND (e.event_date::timestamp + e.start_time) > NOW()"
    elif scope == 'past':
        sql += " AND (e.event_date::timestamp + e.start_time) <= NOW()"

    # -------------------- Date range filter (date-only) --------------------
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

    sql += " ORDER BY e.event_date ASC, e.start_time ASC;"

    with db.get_cursor() as cursor:
        # Events list
        cursor.execute(sql, tuple(params))
        events = cursor.fetchall()

        # Dropdown options: types
        cursor.execute("""
            SELECT DISTINCT event_type
            FROM events
            WHERE event_type IS NOT NULL
            ORDER BY event_type;
        """)
        types = cursor.fetchall()

        # Dropdown options: locations
        cursor.execute("""
            SELECT DISTINCT location
            FROM events
            WHERE location IS NOT NULL AND TRIM(location) <> ''
            ORDER BY location;
        """)
        locations = cursor.fetchall()

    return render_template(
        'volunteer/events_list.html',
        events=events,
        types=types,
        locations=locations,
        scope=scope,
        date_from=date_from,
        date_to=date_to,
        location=location,
        event_type=event_type)


# ============================================================
# Volunteer: Event Details
# ============================================================
@app.route('/volunteer/events/<int:event_id>')
def volunteer_event_detail(event_id):
    """
    View full details of a single event.
    Includes:
    - is_upcoming (start datetime > NOW())
    - is_registered (this volunteer already registered)
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT
                e.event_id, e.event_name, e.location, e.event_type, e.event_date,
                e.start_time, e.end_time, e.duration, e.description, e.supplies, e.safety_instructions,

                -- Event status: upcoming if start datetime > NOW()
                ((e.event_date::timestamp + e.start_time) > NOW()) AS is_upcoming,

                -- My registration status for this event
                EXISTS (
                    SELECT 1
                    FROM eventregistrations r
                    WHERE r.event_id = e.event_id
                      AND r.volunteer_id = %s
                      AND r.attendance IN ('registered', 'attended')
                ) AS is_registered
            FROM events e
            WHERE e.event_id = %s;
        """, (user_id, event_id))
        event = cursor.fetchone()

    if event is None:
        flash("Event not found.", "warning")
        return redirect(url_for('volunteer_events'))

    return render_template('volunteer/event_detail.html', event=event)


# ============================================================
# Volunteer: Register for an event (reject time conflicts)
# ============================================================
@app.route('/volunteer/events/<int:event_id>/register', methods=['POST'])
def volunteer_register_event(event_id):
    """
    Register volunteer for an event.
    Rules:
    - Prevent duplicate registration.
    - Only allow registration for upcoming events (start datetime > NOW()).
    - Reject scheduling conflicts on the same date (overlapping times).
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        # 1) Reject if already registered/attended this event
        cursor.execute("""
            SELECT 1
            FROM eventregistrations
            WHERE event_id = %s AND volunteer_id = %s
              AND attendance IN ('registered', 'attended');
        """, (event_id, user_id))
        if cursor.fetchone() is not None:
            flash("You are already registered for this event.", "warning")
            return redirect(url_for('volunteer_event_detail', event_id=event_id))

        # 2) Load target event datetime and validate upcoming
        cursor.execute("""
            SELECT event_date, start_time, end_time,
                   ((event_date::timestamp + start_time) > NOW()) AS is_upcoming
            FROM events
            WHERE event_id = %s;
        """, (event_id,))
        target = cursor.fetchone()

        if target is None:
            flash("Event not found.", "warning")
            return redirect(url_for('volunteer_events'))

        if not target['is_upcoming']:
            flash("You can only register for upcoming events.", "warning")
            return redirect(url_for('volunteer_event_detail', event_id=event_id))

        t_date = target['event_date']
        t_start = target['start_time']
        t_end = target['end_time']

        # 3) Time conflict check: same date + overlapping time
        cursor.execute("""
            SELECT e.event_name
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND r.attendance IN ('registered','attended')
              AND e.event_date = %s
              AND (%s < e.end_time AND %s > e.start_time)
            LIMIT 1;
        """, (user_id, t_date, t_start, t_end))
        conflict = cursor.fetchone()

        if conflict is not None:
            flash(f"Registration declined: time conflict with '{conflict['event_name']}'.", "warning")
            return redirect(url_for('volunteer_event_detail', event_id=event_id))

        # 4) Insert registration
        cursor.execute("""
            INSERT INTO eventregistrations (event_id, volunteer_id, attendance, reminder_flag, reminder_message)
            VALUES (%s, %s, 'registered', TRUE, 'Upcoming event reminder');
        """, (event_id, user_id))

    flash("Registration successful!", "success")
    return redirect(url_for('volunteer_home'))


# ============================================================
# Volunteer: Participation History (past events + attendance)
# ============================================================
@app.route('/volunteer/history')
def volunteer_history():
    """
    Show past events the volunteer participated in.
    Also passes feedback_event_ids so UI can show "View feedback" for submitted items.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.event_name, e.location, e.event_type,
                   e.event_date, e.start_time, e.end_time,
                   r.attendance
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND e.event_date < CURRENT_DATE
            ORDER BY e.event_date DESC, e.start_time DESC;
        """, (user_id,))
        rows = cursor.fetchall()

        cursor.execute("""
            SELECT event_id
            FROM feedback
            WHERE volunteer_id = %s;
        """, (user_id,))
        fb_rows = cursor.fetchall()

    feedback_event_ids = {x['event_id'] for x in fb_rows}
    return render_template('volunteer/history.html', rows=rows, feedback_event_ids=feedback_event_ids)


# ============================================================
# Volunteer: Feedback (rating 1-5 + comments)
# ============================================================
@app.route('/volunteer/events/<int:event_id>/feedback', methods=['GET', 'POST'])
def volunteer_feedback(event_id):
    """
    Feedback page (view or submit):
    - Only available for past events the volunteer attended (attendance='attended').
    - If feedback already exists: show read-only view.
    - If feedback does not exist: show submission form.
    - One feedback per volunteer per event (DB UNIQUE constraint).
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'volunteer':
        return render_template('access_denied.html'), 403

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        # 1) Must be past event AND attended by this volunteer (assignment rule)
        cursor.execute("""
            SELECT e.event_name, e.event_date, e.start_time, e.end_time, e.location
            FROM eventregistrations r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.volunteer_id = %s
              AND r.event_id = %s
              AND r.attendance = 'attended'
              AND e.event_date < CURRENT_DATE;
        """, (user_id, event_id))
        event_row = cursor.fetchone()

        if event_row is None:
            flash("Feedback is only available for past events you attended.", "warning")
            return redirect(url_for('volunteer_history'))

        event_name = event_row['event_name']
        event_date = event_row['event_date']
        start_time = event_row['start_time']
        end_time = event_row['end_time']
        location = event_row['location']

        # 2) Check if feedback already exists (view mode)
        cursor.execute("""
            SELECT rating, comments
            FROM feedback
            WHERE event_id = %s AND volunteer_id = %s;
        """, (event_id, user_id))
        existing = cursor.fetchone()

    # -------------------- Read-only view (already submitted) --------------------
    if existing is not None:
        return render_template(
            'volunteer/feedback.html',
            event_id=event_id,
            event_name=event_name,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            existing_feedback=existing
        )

    # -------------------- Submission (POST) --------------------
    if request.method == 'POST':
        rating = request.form.get('rating', '').strip()
        comments = request.form.get('comments', '').strip()

        try:
            rating_int = int(rating)
        except Exception:
            rating_int = 0

        if rating_int < 1 or rating_int > 5:
            flash("Rating must be between 1 and 5.", "warning")
            return redirect(url_for('volunteer_feedback', event_id=event_id))

        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO feedback (event_id, volunteer_id, rating, comments)
                    VALUES (%s, %s, %s, %s);
                """, (event_id, user_id, rating_int, comments))
        except Exception:
            # Duplicate insert / race condition safety
            flash("You already submitted feedback for this event.", "warning")
            return redirect(url_for('volunteer_history'))

        flash("Feedback submitted. Thank you!", "success")
        return redirect(url_for('volunteer_history'))

    # -------------------- First-time GET (show form) --------------------
    return render_template(
        'volunteer/feedback.html',
        event_id=event_id,
        event_name=event_name,
        event_date=event_date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        existing_feedback=None)