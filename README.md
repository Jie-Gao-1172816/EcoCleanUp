# Login Example v3.0 (11 February 2026)

# EcoCleanUp (COMP639 S1 2026)

EcoCleanUp is my COMP639 web application for managing community clean-up events.  
It is built with **Flask + PostgreSQL + Bootstrap**.  
This app supports **3 roles**: **Volunteer**, **Event Leader**, **Admin**.

This README explains how to set up, run, and deploy the app, and what files are included for marking.

---

## 1) What this app does (features by role)

### 1.1 Shared features (all roles)
- One login system (same login page for all users).
- Session-based login and role-based access control.
- Logout.
- Profile page (view/update personal details and profile image).
- Change password:
  - password must match validation rules
  - cannot reuse the current password
- Password security:
  - passwords are stored as **bcrypt hashes** (not plain text)

### 1.2 Volunteer features
- Register a new account (registration always creates a **Volunteer**).
- Browse events with filters:
  - date
  - location
  - event type
- Register for an upcoming event.
- Time-conflict rule:
  - if the volunteer is already registered for another event that overlaps in time, registration is declined and a warning message is shown.
- Volunteer dashboard:
  - shows reminders for upcoming registered events.
- Participation history:
  - shows events I registered for / attended.
- Feedback after event:
  - rating (1–5 stars) + comment
  - past events still show the feedback I already submitted (not hidden).

### 1.3 Event Leader features
- Leader dashboard:
  - reminders for upcoming events
  - quick actions (Create / My Events / Reports)
- Create event (with required event details).
- Manage “My Events” (events created by this leader):
  - manage
  - edit
  - cancel
- View registered volunteers list for each event.
- Remove a volunteer from an event (keeps history consistent).
- Attendance tracking (mark registered/attended/no-show etc. depending on my design).
- Record event outcomes:
  - number of attendees
  - rubbish bags collected
  - recyclables sorted
  - other achievement (optional text)
- View feedback submitted for the leader’s events.
- Leader reports (events owned by leader only).

### 1.4 Admin features
- Admin dashboard (platform overview).
- User management:
  - view all users
  - search/filter by name, role, status
  - set status active/inactive
- Event management:
  - view all events
  - edit / cancel as needed
- Reports:
  - platform summary (counts and averages)
  - event reports (attendance/outcomes/feedback summary)

---

## 2) Repository requirements (what is included)

This GitHub repo contains:
- All Python files for the Flask app.
- All HTML templates (Jinja), CSS, JS, and images in `static/`.
- `requirements.txt` (all pip packages).
- Two PostgreSQL scripts:
  - `sql/01_create_database.sql` (database + tables)
  - `sql/02_populate_records.sql` (seed data)
- `.gitignore` (excludes virtual environment and `connect.py`)
- This `README.md` (includes GenAI acknowledgement)

### 2.1 Seed data requirement
My population script contains (at minimum):
- 20 volunteers
- 5 event leaders
- 2 admins
- 20 events
- 20 registrations
- password hashes are bcrypt hashes (not plain passwords)

---

## 3) Project structure (typical layout)

Your folders may look like this:

- `EcoCleanUp/` (Flask app package or main module)
- `templates/` (Jinja templates)
- `static/` (css, images, js)
- `sql/`
  - `01_create_database.sql`
  - `02_populate_records.sql`
- `requirements.txt`
- `.gitignore`
- `run.py` (or `app.py` / main entry)
- `connect.py` (NOT included in GitHub)

---

## 4) Local setup (run on your computer)

### 4.1 Create a virtual environment
```bash
 python -m venv venv
**Windows (PowerShell)**
```bash
venv\Scripts\Activate.ps1
**Mac/Linux**
```bash
source venv/bin/activate

### 4.1 Create a virtual environment