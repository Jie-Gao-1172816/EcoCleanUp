# EcoCleanUp (COMP639 S1 2026)

EcoCleanUp is my individual COMP639 web application.
It is a Flask web app with a PostgreSQL database.
It supports three roles: **Volunteer**, **Event Leader**, and **Admin**.

This repository is a  GitHub repository named **EcoCleanUp** and includes everything needed for deployment.

---

## 1) What this app does 


### 1) Site Entry (Landing Page)
- The system shall provide a **Landing / Home page** as the first page of the app.
- The Landing page shall display:
  - The project title (EcoCleanUp)
  - Student information (e.g., **name + student ID**)
  - Two main actions:
    - **Login**
    - **Register**

---

### 2) Register (Volunteer Only)
- The system shall allow **self-registration for Volunteer accounts only**.
- The Register page shall create a new user with role = **Volunteer**.
- The system shall **not** allow self-registration as **Event Leader** or **Admin**.
- After successful registration, the system shall show a success message and redirect the user to the Login page (or log them in automatically, depending on implementation).

---

### 3) Shared Login/Logout (All Roles)
- The system shall provide a **single shared Login page** for all roles.
- The Login page shall authenticate users and redirect them to the correct dashboard based on role:
  - Volunteer → Volunteer Dashboard
  - Event Leader → Leader Dashboard
  - Admin → Admin Dashboard
- The system shall provide a **Logout** function that ends the session and returns the user to the Landing/Login page.
- The system shall protect all role pages so that:
  - Unauthenticated users are redirected to Login.
  - Logged-in users cannot access other roles’ pages (Access Denied 403).

---

# Volunteer

## Volunteer Navigation Structure 
- Volunteer
  - 1) Dashboard (My Upcoming Events)
    - Upcoming Events List (cards)
      - View Details → Event Detail
        - Actions/Links:
          - **Back to My Upcoming Events** 
          - **Back to Events** 
  - 2) Browse Events
    - Filters (Date / Location / Type)
    - Events List (cards)
      - View Details → Event Detail
      - Register (upcoming only)
  - 3) Participation History
    - Past Events List 
      - View Details 
      - View Feedback 

---

### 4) Volunteer Dashboard (My Upcoming Events)
- After a Volunteer logs in successfully, the system shall display the **Volunteer Dashboard**.
- The Volunteer Dashboard shall show:
  - A list of the volunteer’s **upcoming registered events**.
  - Each event shall include a **View Details** action to open the event detail page.
- The system should support clear navigation from event detail:
  - A link/button to return to **My Upcoming Events**.
  - A link/button to return to the general events list (**Back to Events**).

---

### 5) Browse Events (Volunteer)
- The system shall allow volunteers to browse available events.
- The Browse Events page shall provide filters:
  - **Date**
  - **Location**
  - **Type**
- The filters shall be optional and should support:
  - Apply filters
  - Reset filters
- Each event in the list shall provide:
  - **View Details** (always available)
  - **Register** (upcoming events only)

---

### 6) Volunteer Event Detail (View Details)
- The system shall display the main event information on the event detail page, including (at minimum):
  - Event name
  - Date
  - Start time and end time (or duration)
  - Location
  - Type (if used)
  - Description / notes (if used)
- The event detail page shall provide clear navigation links:
  - Back to Browse Events
  - Back to My Upcoming Events (if accessed from dashboard)

---

### 7) Register for an Event (Volunteer)
- The system shall allow volunteers to register for an **upcoming** event.
- The system shall prevent:
  - **Duplicate registration** for the same event.
  - **Time conflicts**: if a volunteer is already registered for another event that overlaps in time on the same date.
- If a conflict is detected:
  - The system shall show a warning message.
  - The registration shall be declined (no new record created).

---

### 8) Participation History (Volunteer)
- The system shall provide a **Participation History** page for volunteers.
- The Participation History page shall display:
  - A list of past events the volunteer participated in (or registered for, depending on your rule)
  - Attendance status (e.g., registered / attended / removed / no-show — based on your design)
- Each past event entry shall provide:
  - **View Feedback** to see feedback submitted by the volunteer (if feedback exists).

---

### 9) View Feedback (Volunteer)
- The system shall allow volunteers to view their own submitted feedback for past events.
- If no feedback exists for that event, the UI should clearly indicate that feedback has not been submitted.


# Admin

## Admin Navigation Structure
- Admin
  - 1) Dashboard (Platform Overview + Quick Actions)
    - Overview Metrics Cards
    - Quick Actions (Row 1): Manage Users / Manage Events / Participation History
    - Quick Actions (Row 2): Platform Report / Event Report
  - 2) Manage Users
    - User Filters
    - Quick Link: Participation History
    - Users List (status + contact + update)
  - 3) Participation History (Admin)
    - Search by Volunteer Name / Username
    - Participation Results List
    - View Participation Detail
    - Navigation: Back to Users / Back to Dashboard
  - 4) Manage Events
    - Event Filters (Scope/Date/Type/Location/Leader)
    - Events List (cards)
      - Actions per event: Volunteers / Report / Edit / Cancel
    - Navigation: Back to Dashboard
  - 5) Platform Report
    - Platform Summary Metrics
    - Quick Link: View Event Report
  - 6) Event Report
    - Event Filters
    - All Events List
    - View Details → attendance summary + volunteers + feedback

---

### 2) Admin Dashboard (Platform Overview)
- After an Admin logs in, the system shall display the **Admin Dashboard**.
- The Admin Dashboard shall show a **platform overview summary**, including:
  - Total events
  - Total volunteers
  - Total event leaders
  - Total admins
  - Total feedback submissions
  - Average rating (overall)

---

### 3) Admin Dashboard — Quick Actions (Entry Cards)
- The Admin Dashboard shall provide quick entry cards/buttons in two rows:

#### Row 1
- **Manage Users**
- **Manage Events**
- **Participation History**

#### Row 2
- **Platform Report**
- **Event Report**

---

###  4) Manage Users (Admin)
- The system shall provide a **Manage Users** page for Admin.
- The Manage Users page shall include:
  - A **filter/search section** to find users (e.g., by name / role / status — based on your implementation).
  - A **Users list** showing (at minimum):
    - User identity (name / username)
    - Role
    - Contact details (as stored)
    - Current status (Active / Inactive)
- The Admin shall be able to:
  - Change a user’s status between **Active** and **Inactive**
  - Click an **Update** action to apply the change
- The system shall show success/warning messages after status updates.

#### Manage Users — Quick Link
- Between the filter section and the user list, the page shall provide a quick entry to:
  - **Participation History**

---

###  5) Participation History (Admin)
- The system shall provide a **Participation History** page accessible from:
  - Admin Dashboard (quick action card)
  - Manage Users page (quick link)
- The Participation History page shall support:
  - Search by **volunteer name** and/or **username**
- The system shall display a list of matching volunteers and their participation summary.
- For each volunteer, the Admin shall be able to click **View** to open detailed participation information.

#### Participation History — View Detail
- The Participation Detail view shall show:
  - Whether the volunteer has participated in any events
  - Which events they registered/attended
  - Basic event information for each participation record

#### Participation History — Navigation
- The Participation History page shall provide navigation buttons:
  - **Back to Users**
  - **Back to Dashboard**

---

###  6) Manage Events (Admin)
- The system shall provide a **Manage Events** page for Admin.
- The Manage Events page shall include filters, including (as implemented):
  - Scope
  - Date
  - Type
  - Location
  - Leader
- The Admin shall be able to apply filters to view a targeted event list.

#### Manage Events — Event List Actions
- Each event in the admin list shall provide four actions:
  1. **Volunteers** — view volunteers registered for the event
  2. **Report** — open the event report detail (attendance summary + volunteers + feedback)
  3. **Edit** — update event information (then Save/Cancel)
  4. **Cancel** — cancel the event

#### Manage Events — Navigation
- The Manage Events page shall provide a **Back to Dashboard** button.

---

### 7) Platform Report (Admin)
- The system shall provide a **Platform Report** page for Admin.
- The Platform Report page shall present a platform-wide summary (similar to the dashboard metrics).
- The Platform Report page shall include a quick entry to:
  - **View Event Report**

---

### 8) Event Report (Admin)
- The system shall provide an **Event Report** page for Admin.
- The Event Report page shall include:
  - Filters to search and narrow down events (as implemented)
  - A list of events matching the filters
- Each event shall provide a **View Details** action.

#### Event Report — Detail View
- The Event Report detail view shall show:
  - Attendance summary
  - Volunteer list (engagement details)
  - Feedback list/summary for the event


# Event Leader

## Event Leader Navigation Structure (Structure Tree)
- Event Leader
  - 1) Dashboard
    - Quick Actions (Row 1): Create New Event / Browse Events / My Events / Report
    - Quick Actions (Row 2): Participation History / Review Feedback
    - Upcoming Events List
      - Actions per event: Manage Event / Edit Event / Cancel Event
  - 2) Manage Event (Event Management Hub)
    - Event Detail
    - Send a Reminder (message box → send to volunteers)
    - Registered Volunteers (list + remove)
    - Attendance (list + update status)
    - Outcomes (edit + update)
    - Feedback (list)
    - Summary Panel (Participation Summary)
    - Bottom Actions: Edit / Cancel
    - Top-right Navigation: My Events / Browse Events / Back to Dashboard
  - 3) Create New Event
    - Event Form
    - Create Event
    - Navigation: Back to Dashboard
  - 4) Browse Events
    - Filters
    - Events List
      - Own events: Manage / Edit / Cancel
      - Other leaders’ events: view-only (no cancel/edit)
  - 5) My Events
    - List of events created by this leader
    - Actions: Manage / Edit / Cancel
  - 6) Report (Leader Reports)
    - Filters
    - Events Report List
    - View Detail → report detail page
  - 7) Participation History (Leader View)
    - Search volunteers
    - Volunteer list + View
    - Volunteer history detail
  - 8) Review Feedback
    - Feedback list for leader’s events

---

### 2) Leader Dashboard
- After a Leader logs in, the system shall display the **Leader Dashboard**.
- The Leader Dashboard shall provide quick actions:

#### Dashboard Quick Actions (Row 1)
- **Create New Event**
- **Browse Events**
- **My Events**
- **Report**

#### Dashboard Quick Actions (Row 2)
- **Participation History**
- **Review Feedback**

#### Dashboard Upcoming Events List
- The dashboard shall display an **Upcoming Events** list.
- Each upcoming event shall provide these actions:
  - **Manage Event**
  - **Edit Event**
  - **Cancel Event**

---

### 3) Manage Event (Event Management Hub)
- The system shall provide a **Manage Event** page as the main hub to manage a specific event owned by the leader.
- The Manage Event page shall display **event details**, including (at minimum):
  - Event name
  - Date
  - Start/end time (or duration)
  - Location
  - Type (if used)
  - Description / supplies / safety notes (as stored)

#### 3.1 Send a Reminder
- The Manage Event page shall include a **Send a Reminder** section.
- The leader shall be able to:
  - Write/edit a reminder message
  - Send the reminder to volunteers registered for the event

#### 3.2 Registered Volunteers List
- The Manage Event page shall display a **Registered Volunteers** list.
- For each volunteer, the leader shall be able to:
  - View the volunteer’s basic identity (name/username as stored)
  - **Remove** the volunteer from the event when needed

#### 3.3 Attendance Management
- The Manage Event page shall include an **Attendance** section.
- The leader shall be able to update attendance status per volunteer.
- Attendance status shall support (based on your design):
  - **Registered**
  - **Attended**
  - **Absent**
- Each row shall provide an **Update** action to save the changed status.

#### 3.4 Event Outcomes
- The Manage Event page shall include an **Outcomes** section.
- The leader shall be able to record and update outcomes for the event, including:
  - Number of attendees
  - Rubbish bags collected
  - Recyclables sorted
  - Other achievements (if used)
- The leader shall be able to **update outcomes multiple times** (overwrite/update existing outcome record).

#### 3.5 Feedback List
- The Manage Event page shall include a **Feedback** section showing feedback submitted for that event.

#### 3.6 Participation Summary Panel
- The Manage Event page shall display a summary panel showing (for this event):
  - Total Registered
  - Total Attended
  - Total Absent
  - Average Rating (if feedback exists)

#### 3.7 Manage Event — Main Actions
- At the bottom of the Manage Event page, the system shall provide:
  - **Edit** (go to edit page)
  - **Cancel** (cancel the event)

#### 3.8 Manage Event — Navigation Shortcuts
- The top-right area shall provide navigation shortcuts:
  - **My Events**
  - **Browse Events**
  - **Back to Dashboard**

---

### 4) Create New Event
- The system shall allow leaders to create new events from **Create New Event**.
- The Create Event form shall collect (as implemented):
  - Event name
  - Location
  - Type
  - Date
  - Time / Duration
  - Description (and/or supplies/safety instructions)
- The form shall provide a **Create** action to save the new event.
- The page shall provide a **Back to Dashboard** navigation shortcut.

---

### 5) Browse Events (Leader)
- The system shall provide a **Browse Events** page for leaders.
- The page shall include filters (as implemented) to search events.
- The page shall show a list of events.
- Leaders shall be allowed to manage only their own events:
  - For events owned by the current leader:
    - **Manage**
    - **Edit**
    - **Cancel**
  - For events owned by other leaders:
    - view-only (no manage/edit/cancel)

---

### 6) My Events (Leader)
- The system shall provide a **My Events** page showing only events created by the current leader.
- Each event shall provide actions:
  - **Manage**
  - **Edit**
  - **Cancel**

---

### 7) Report (Leader Reports)
- The system shall provide a **Report** page for leaders.
- The Report page shall include filters to find events managed by the leader.
- Each event report card/row shall include a **View Detail** action.

#### Report — Detail View
- The report detail view shall show:
  - Attendance summary
  - Volunteer engagement list (registered/attended/absent)
  - Volunteer feedback (ratings + comments)

---

### 8) Participation History (Leader View)
- The system shall provide a **Participation History** page for leaders.
- The page shall allow searching volunteers (as implemented).
- The results list shall provide a **View** action for each volunteer.

#### Participation History — Detail View
- The system shall display that volunteer’s event participation details, including:
  - Dates and events joined
  - Attendance status for each event

---

### 9) Review Feedback (Leader)
- The system shall provide a **Review Feedback** page for leaders.
- The page shall display feedback entries related to the leader’s events.
- The feedback list shall include (at minimum):
  - Event name
  - Volunteer identity (name/username)
  - Rating
  - Comment
  - Date/time (if stored)




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

# 10) GenAI Usage Acknowledgement 

I used GenAI tools during development, and I acknowledge it here.

## 10.1 Tools used

* ChatGPT (OpenAI)

## 10.2 How I used it 

* I used it to troubleshoot Flask route errors and redirect issues.
* I used it to check session role logic (volunteer/leader/admin).
* I used it to improve SQL queries and database scripts.
* I used it to fix PythonAnywhere deployment issues.
* I used it to improve Bootstrap layout for mobile screens.
* For some difficult parts, I used suggested code patterns and then edited and tested them in my own project.

## 10.3 Prompt 

## GenAI Prompt  (COMP639 EcoCleanUp)

1. **2026-02-23** — I clicked **“Register”** but nothing happened. How can I check the form `action`, `method="POST"`, and confirm the request is reaching the correct Flask route?

2. **2026-02-23** — I was unsure which route should handle registration. What is a clean pattern for a **POST register route** (validate → save → flash → redirect) and where should success/warning messages be flashed?

3. **2026-02-23** — My event browsing page needed filters (date/location/type). How can I build a simple filter query with optional inputs without making the SQL hard to read?

4. **2026-02-23** — My location filter returned wrong results. How do I debug optional `WHERE` conditions and avoid common mistakes when some filters are blank?

5. **2026-02-23** — Users could double-click **Register** and create duplicate registrations. How can I block duplicates safely using both server checks and a database rule?

6. **2026-02-23** — I needed the rule “already registered at the same time”. How do I detect **overlapping event times** correctly (including edge cases like end time equals start time)?

7. **2026-02-24** — I repeated role checks in many routes. How can I create helper functions (or decorators) to reduce repeated code but keep it clear?

8. **2026-02-24** — Volunteers could access leader pages by typing the URL. How can I return a consistent **Access Denied (403)** page for all protected routes?

9. **2026-02-24** — I wanted one login form for all roles. How can I redirect users to the right dashboard after login based on their role?

10. **2026-02-24** — Registration must always create a volunteer account. Where should I enforce the default role/status so users cannot register as leader/admin?

11. **2026-02-24** — My password rules were unclear. How can I validate password length and required character types and show clear error messages?

12. **2026-02-24** — I needed bcrypt hashing for registration and login. What is the correct way to store hashed passwords and verify them on login?

13. **2026-02-25** — I wanted volunteer reminders for upcoming events. What SQL join/query should fetch upcoming registrations for the logged-in volunteer?

14. **2026-02-25** — My reminder popup did not show. How can I quickly check whether the issue is the SQL query or the Jinja template block?

15. **2026-02-25** — I needed a participation history list. What route and query should show past events and the volunteer’s attendance/registration status?

16. **2026-02-25** — I designed feedback submission. What fields should I store for rating (1–5) and comment, linked to the event and volunteer?

17. **2026-02-25** — Feedback was showing for future events. How do I restrict feedback so it is only allowed for past events (UI + server checks)?

18. **2026-02-26** — Leader create-event form needed validation. How can I validate start/end times and basic input rules and return friendly messages?

19. **2026-02-26** — Leader “My Events” should show only events the leader created. How should I use `session['user_id']` in the query safely?

20. **2026-02-26** — I wasn’t sure whether to delete events or cancel them. Which approach keeps registrations and reports consistent?

21. **2026-02-26** — I needed a list of registered volunteers for each event. What join query should return volunteer details and registration status?

22. **2026-02-26** — I needed to remove a volunteer but keep history. Should I update an attendance/status field instead of deleting the record?

23. **2026-02-26** — Attendance marking needed batch updates. How can I update many registrations from one form submission safely?

24. **2026-02-27** — I added event outcomes (bags collected, recyclables, etc.). How should I store outcomes per event and support updating them later?

25. **2026-02-27** — I needed leader reports for my events only. How can I combine outcomes with feedback averages and still show events with no feedback?

26. **2026-02-27** — Admin user list needed filters. How can I search by name and filter by role/status together without breaking the SQL?

27. **2026-02-27** — Admin status updates needed safety checks. How can I prevent dangerous changes (like locking out all admins) and show clear messages?

28. **2026-02-28** — I needed a platform summary report. What SQL counts users/events/registrations/feedback and calculates average rating?

29. **2026-02-28** — My event report layout looked bad on mobile. How can I restructure Bootstrap filter rows so the page is responsive?

30. **2026-03-01** — I wanted route naming to be consistent. How can I standardise volunteer/leader/admin route prefixes and endpoint names?

31. **2026-03-01** — PythonAnywhere could not import my app. How can I check the WSGI file, module name, and `sys.path` settings?

32. **2026-03-02** — GitHub and deployment confused me. What is a simple workflow to update PythonAnywhere from GitHub and keep code in sync?

33. **2026-03-02** — I got database column errors on PythonAnywhere. How can I match my SQL queries to the real table columns and avoid schema mismatch?





## Assets & References

### Hero image (landing page)
- Title: *A Man and a Woman Holding Sacks of Garbage*
- Photographer: **Thirdman**
- Source: Pexels (Photo ID: 7656992) — https://www.pexels.com/photo/a-man-and-a-woman-holding-sacks-of-garbage-7656992/
- License: Pexels License (free to use; attribution not required) — https://www.pexels.com/license/