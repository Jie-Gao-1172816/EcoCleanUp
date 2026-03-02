# EcoCleanUp (COMP639 S1 2026)

EcoCleanUp is my individual COMP639 web application.
It is a Flask web app with a PostgreSQL database.
It supports three roles: **Volunteer**, **Event Leader**, and **Admin**.

This repository is a **private** GitHub repository named **EcoCleanUp** and includes everything needed for marking and deployment.

---

## 1) What this app does (simple overview)

## What this app can do (by role)

### Volunteer
- Register a new account (**Volunteer only**). Users cannot self-register as Event Leader or Admin.
- Registration collects: username (unique), email, password (min 8 chars + mixed types), optional profile image, full name, home address, contact number, environmental interests.
- Login and logout using the shared login system (same login page for all roles).
- View and edit my profile (name, address, contact number, interests, profile image).
- Change my password (new password validated; cannot reuse current password).
- Browse upcoming cleanup events and filter by **date / location / type**.
- Register for an event.
  - If I am already registered for another event at the same time, the system shows a warning and declines registration.
- See reminders on login for upcoming registered events (popup notification).
- View my participation history (past events + attendance status).
- Submit feedback after an event (rating **1–5** + comment).
- View my submitted feedback for past events.

### Event Leader
- Login and logout using the shared login system.
- View and edit my profile; change my password (same rules as above).
- Browse upcoming cleanup events and filter by **date / location / type**.
- Create new cleanup events with required details (event name, location, date, time, duration, supplies, safety instructions).
- Manage events I created (view, edit, cancel).
- View the list of registered volunteers for my events.
- Remove volunteers from my events when needed.
- Track volunteer attendance during each event.
- Record event outcomes (number of attendees, rubbish bags collected, recyclables sorted, other achievements if used).
- Review volunteer feedback for my events.
- View reports for events I manage.

### Admin
- Login and logout using the shared login system.
- View and edit my profile; change my password (same rules as above).
- Browse upcoming cleanup events and filter by **date / location / type**.
- Manage events across the platform (view all events, edit, cancel).
- View registered volunteer lists for events.
- View all users with role and status; search/filter by full name, role, status.
- Change user status (active/inactive).
- View platform-wide reports (total events, total volunteers, total event leaders, total feedback submissions, average event rating).
- View event reports summarising attendance and volunteer engagement (admin sees all events; leaders see their own).


## 2) Repository requirements (what is included)

This repository includes:

- All Python files, templates (HTML), static files (CSS/images), and any other needed files.
- `requirements.txt` (pip packages).
- Two PostgreSQL scripts:
  - Database creation script (tables/structure)
  - Database population script (seed records)
- `.gitignore` (excludes my virtual environment and `connect.py`)
- This `README.md` (includes GenAI Acknowledgement)

Required collaborator added:

- GitHub user **lincolnmac** (computing@lincoln.ac.nz)

---

## 3) Security note (connect.py is NOT in GitHub)

My database connection details are stored in a file called `connect.py`.
This file is excluded by `.gitignore` and is not committed to GitHub.

I create a different `connect.py` for:

- local computer
- PythonAnywhere

---

## 4) Local setup (run on your computer)

### 4.1 Create a virtual environment

```bash
python -m venv venv
```

### 4.2 Activate it

**Windows (PowerShell)**
venv\Scripts\Activate.ps1

**macOS / Linux**
source venv/bin/activate

### 4.3 Install required packages

pip install -r requirements.txt

### 4.4 Create the database and tables

Make sure PostgreSQL is installed and running.

Run the creation script:

psql -U postgres -f create_database.sql

Run the population script:
psql -U postgres -d ecocleanup -f populate_database.sql

Note:

* If your database name is different, use the database name created in `create_database.sql`.

### 4.5 Create `connect.py` (local)

Create a `connect.py` file in the project root.

Example (adjust to your own settings):

#connect.py (DO NOT COMMIT)

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "ecocleanup"
DB_USER = "postgres"
DB_PASSWORD = "your_password"

### 4.6 Run the app

Option A:
python run.py

Option B:
flask run

Then open:

* [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 5) Login and test accounts

Test accounts are inserted by:

* `populate_database.sql`

For marking, the marker can log in using:

* volunteer accounts
* leader accounts
* admin accounts

Passwords are stored as bcrypt hashes, not plain text.

---

## 6) Deployment to PythonAnywhere (Flask + PostgreSQL)

### 6.1 Clone the private GitHub repo on PythonAnywhere

Open a PythonAnywhere Bash console:
cd ~
git clone <your_private_repo_url>
cd EcoCleanUp

### 6.2 Create a virtual environment and install packages

mkvirtualenv --python=/usr/bin/python3.10 ecoccleanup-venv
pip install -r requirements.txt

### 6.3 Connect to the COMP639 PostgreSQL database and run scripts

In Bash:
export PGPASSWORD='YOUR_PASSWORD_HERE'

Run the creation script:
psql -h YOUR_HOST -p YOUR_PORT -U YOUR_USER -d YOUR_DB -f /home/<your_username>/EcoCleanUp/create_database.sql

Run the population script:
psql -h YOUR_HOST -p YOUR_PORT -U YOUR_USER -d YOUR_DB -f /home/<your_username>/EcoCleanUp/populate_database.sql

### 6.4 Create `connect.py` on PythonAnywhere

Create a `connect.py` in the project root using the course database credentials.

Example format:

#connect.py (DO NOT COMMIT)

DB_HOST = "YOUR_HOST"
DB_PORT = 15080
DB_NAME = "YOUR_DB"
DB_USER = "YOUR_USER"
DB_PASSWORD = "YOUR_PASSWORD"

### 6.5 Configure the Web app (WSGI)

PythonAnywhere → Web tab:

* Set **Source code** to `/home/<your_username>/EcoCleanUp`
* Set **Virtualenv** to `/home/<your_username>/.virtualenvs/ecoccleanup-venv`
* Edit the WSGI file and import the Flask app

Example pattern (adjust module name if needed):

import sys

project_path = "/home/<your_username>/EcoCleanUp"
if project_path not in sys.path:
sys.path.append(project_path)

from EcoCleanUp import app as application

### 6.6 Reload

Click **Reload** in the Web tab.



## 7) requirements.txt

If packages change, update:

pip freeze > requirements.txt

## 8) .gitignore (required)

This repo must ignore:

* the virtual environment folder
* `connect.py`

Example `.gitignore`:

---
__pycache__/
*.pyc

venv/
.venv/
.env/

connect.py

.vscode/
.DS_Store
---

## 9) GitHub collaborator (required)

Add GitHub user:

* `lincolnmac` ([computing@lincoln.ac.nz]())

Steps:

* Repo → Settings → Collaborators → Add people → search `lincolnmac`

---

# 10) GenAI Usage Acknowledgement (COMP639 requirement)

I used GenAI tools during development, and I acknowledge it here.

## 10.1 Tools used

* ChatGPT (OpenAI)

## 10.2 How I used it (simple description)

* I used it to troubleshoot Flask route errors and redirect issues.
* I used it to check session role logic (volunteer/leader/admin).
* I used it to improve SQL queries and database scripts.
* I used it to fix PythonAnywhere deployment issues.
* I used it to improve Bootstrap layout for mobile screens.
* For some difficult parts, I used suggested code patterns and then edited and tested them in my own project.

## 10.3 Prompt log (dates only, 34 entries)

1. **2026-02-23** — I clicked “Register” but nothing happened. I asked how to check if the form action and POST route were wired correctly.
2. **2026-02-23** — I got confused about which route should handle registration and where to flash success/warning messages. I asked for a clean route pattern.
3. **2026-02-23** — My event browsing page needed filters. I asked how to build a simple filter query without making the SQL messy.
4. **2026-02-23** — My location filter returned wrong results. I asked how to debug WHERE clauses when filters are optional.
5. **2026-02-23** — Users could double-click register and create duplicates. I asked how to block duplicate registrations safely.
6. **2026-02-23** — I needed the “already registered at the same time” rule. I asked how to detect overlapping event times.
7. **2026-02-24** — I repeated role checks in many routes. I asked how to make helper functions for access control.
8. **2026-02-24** — Volunteers could access leader pages by typing the URL. I asked how to return access denied consistently.
9. **2026-02-24** — I wanted one login form for all roles. I asked how to redirect to different dashboards after login.
10. **2026-02-24** — Registration must always create a volunteer. I asked where to enforce default role and status.
11. **2026-02-24** — My password validation rules were unclear. I asked how to validate length and character types.
12. **2026-02-24** — I needed bcrypt hashing for registration and login. I asked how to check passwords correctly.
13. **2026-02-25** — I wanted volunteer reminders for upcoming events. I asked what SQL join should fetch upcoming registrations.
14. **2026-02-25** — My reminder popup did not show. I asked how to confirm flash/reminder blocks in the Jinja template.
15. **2026-02-25** — I needed a participation history list. I asked what route and query should show past events and attendance.
16. **2026-02-25** — I designed feedback submission. I asked what fields to store rating (1–5) and comment linked to event/user.
17. **2026-02-25** — Feedback was showing for future events. I asked how to restrict feedback to only past events.
18. **2026-02-26** — Leader create-event form needed validation. I asked how to validate start/end times and duration.
19. **2026-02-26** — Leader “My Events” should show only owned events. I asked how to use session user\_id in the query.
20. **2026-02-26** — I wasn’t sure whether to delete events or cancel by status. I asked which approach keeps reports consistent.
21. **2026-02-26** — I needed a list of registered volunteers for each event. I asked for a join query with profile fields.
22. **2026-02-26** — I needed to remove a volunteer but keep history. I asked whether to update attendance instead of delete.
23. **2026-02-26** — Attendance marking needed batch updates. I asked how to update many registrations from one form.
24. **2026-02-27** — I added event outcomes (bags collected etc.). I asked how to store and update outcomes per event.
25. **2026-02-27** — I needed leader reports for my events only. I asked for a query combining outcomes and feedback averages.
26. **2026-02-27** — Admin user list needed filters. I asked how to search by name and filter by role/status together.
27. **2026-02-27** — Admin status update needed safety checks. I asked how to prevent accidental lockout and show messages.
28. **2026-02-28** — I needed a platform summary report. I asked what SQL counts events, users, feedback, and average rating.
29. **2026-02-28** — My event report page layout looked bad on mobile. I asked how to restructure Bootstrap filter rows.
30. **2026-03-01** — I wanted route naming to be consistent. I asked how to standardise volunteer/leader/admin route prefixes.
31. **2026-03-01** — PythonAnywhere could not import my app. I asked how to check WSGI file and sys.path settings.
32. **2026-03-02** — GitHub push/pull and deployment confused me. I asked how to update server code from a private repo.
33. **2026-03-02** — I got database column errors on PythonAnywhere. I asked how to align SQL queries with actual table columns.
34. **2026-03-03** — I needed a final README that meets COMP639 rules. I asked how to describe setup, deployment, and GenAI use clearly.

