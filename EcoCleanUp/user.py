from tkinter import INSERT
from EcoCleanUp import app
from EcoCleanUp import db
from flask import redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
import re
# user.py
# Core routes for:
# - Public home page
# - Login / Logout (single login form for all roles)
# - Volunteer registration (volunteer-only)
# - Profile view & edit (all roles)
# - Change password (all roles)
#
# Tech stack: Flask + PostgreSQL + Bootstrap + flask_bcrypt

from EcoCleanUp import app, db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import re

# Bcrypt instance used for hashing passwords and verifying login credentials.
flask_bcrypt = Bcrypt(app)

# New registrations must always create "volunteer" users (per project rules).
DEFAULT_USER_ROLE = 'volunteer'

# Profile images are stored as static files (NOT in the database).
# The users.profile_image field stores the filename only.
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')

# Whitelist allowed image extensions for safety.
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Ensure upload folder exists so saving files won't fail.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Return True if the file extension is allowed for profile image uploads."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_password(pw: str) -> str | None:
    """
    Validate password complexity (assignment requirement).
    Returns an error message string if invalid, otherwise None.
    Rules:
    - At least 8 characters
    - Contains uppercase, lowercase, number, special character
    """
    if len(pw) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", pw):
        return "Password must include at least one uppercase letter."
    if not re.search(r"[a-z]", pw):
        return "Password must include at least one lowercase letter."
    if not re.search(r"\d", pw):
        return "Password must include at least one number."
    if not re.search(r"[^\w\s]", pw):
        return "Password must include at least one special character."
    return None


def user_home_url():
    """
    Decide where to redirect a logged-in user based on their role.
    We store role in the Flask session after login.

    If session data is missing or role is invalid, redirect to logout
    to clear the session cookie safely.
    """
    if session.get('loggedin'):
        role = session.get('role')
        if role == 'volunteer':
            return url_for('volunteer_home')
        if role == 'event_leader':
            return url_for('leader_home')
        if role == 'admin':
            return url_for('admin_home')
        return url_for('logout')
    return url_for('login')


# ============================================================
# Public Home Page
# ============================================================

@app.route('/')
def home():
    """
    Public home page (required by assignment).
    - Guests see Home with login/registration links.
    - Logged-in users are redirected to their role-specific homepage.
    """
    if session.get('loggedin'):
        return redirect(user_home_url())
    return render_template('home.html')


# ============================================================
# Login / Logout
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Single login form for all roles (volunteer, event leader, admin).
    - On POST: verify username exists, status is active, and password matches hash.
    - On success: store user_id, username, role in session.
    - On failure: re-render login page with error flags for Bootstrap validation.
    """
    if session.get('loggedin'):
        return redirect(user_home_url())

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Read credentials from the login form.
        username = request.form['username'].strip()
        password = request.form['password']

        # Retrieve account information from the database.
        # NOTE: we also fetch status so we can block inactive users.
        with db.get_cursor() as cursor:
            cursor.execute('''
                SELECT user_id, username, password_hash, role, status
                FROM users
                WHERE username = %s;
            ''', (username,))
            account = cursor.fetchone()

        # If username doesn't exist, show a username error.
        if account is None:
            return render_template('login.html', username=username, username_invalid=True)

        # Block inactive accounts (admin can deactivate users).
        if account.get('status') != 'active':
            return render_template('login.html', username=username, account_inactive=True)

        # Verify password using bcrypt (hash stored in DB, not plaintext).
        password_hash = account['password_hash']
        if flask_bcrypt.check_password_hash(password_hash, password):
            # Save minimal identity details in session for access control.
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            session['role'] = account['role']
            return redirect(user_home_url())

        # Password incorrect
        return render_template('login.html', username=username, password_invalid=True)

    # GET request (or invalid POST) just renders the login form.
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logout: clear session cookie and redirect back to login.
    """
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))


# ============================================================
# Volunteer Registration (Signup)
# ============================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Volunteer registration only:
    - New user role is always 'volunteer' (cannot self-register as leader/admin).
    - Required fields: username, email, password, full_name, home_address,
      contact_number, environmental_interests
    - Optional: profile_image upload (filename stored in DB)
    """
    if session.get('loggedin'):
        return redirect(user_home_url())

    if request.method == 'POST':
        # Collect form fields (strip whitespace where appropriate).
        username = request.form.get('username', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        home_address = request.form.get('home_address', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()
        password = request.form.get('password', '')

        # Error messages passed to template for user-friendly feedback.
        username_error = None
        email_error = None
        password_error = None
        full_name_error = None
        contact_error = None
        address_error = None
        interests_error = None
        image_error = None

        # ---------- Username validation ----------
        if not username:
            username_error = "Username is required."
        elif len(username) > 50:
            username_error = "Username cannot exceed 50 characters."
        elif not re.fullmatch(r'[A-Za-z0-9.]+', username):
            username_error = "Username can only contain letters, numbers, and dots."
        else:
            # Enforce uniqueness at app-level (DB also enforces UNIQUE).
            with db.get_cursor() as cursor:
                cursor.execute('SELECT 1 FROM users WHERE username = %s;', (username,))
                if cursor.fetchone() is not None:
                    username_error = "An account already exists with this username."

        # ---------- Full name ----------
        if not full_name:
            full_name_error = "Full name is required."
        elif len(full_name) > 100:
            full_name_error = "Full name cannot exceed 100 characters."

        # ---------- Email ----------
        if not email:
            email_error = "Email is required."
        elif len(email) > 100:
            email_error = "Email cannot exceed 100 characters."
        elif not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = "Invalid email address."

        # ---------- Password rules (assignment requirement) ----------
        password_error = validate_password(password)

        # ---------- Contact / Address / Interests ----------
        if not contact_number:
            contact_error = "Contact number is required."
        elif len(contact_number) > 20:
            contact_error = "Contact number cannot exceed 20 characters."

        if not home_address:
            address_error = "Home address is required."
        elif len(home_address) > 255:
            address_error = "Home address cannot exceed 255 characters."

        if not environmental_interests:
            interests_error = "Environmental interests are required."
        elif len(environmental_interests) > 255:
            interests_error = "Environmental interests cannot exceed 255 characters."

        # ---------- Optional image upload ----------
        # We store image as a static file and save its filename in DB.
        profile_image_filename = None
        file = request.files.get('profile_image')
        if file and file.filename:
            if not allowed_file(file.filename):
                image_error = "Profile image must be png/jpg/jpeg/gif/webp."
            else:
                safe_name = secure_filename(file.filename)
                base, ext = os.path.splitext(safe_name)
                profile_image_filename = f"{username}{ext.lower()}"
                file.save(os.path.join(UPLOAD_FOLDER, profile_image_filename))

        # If any validation error occurred, return user to signup page with messages.
        if (username_error or full_name_error or email_error or password_error or
            contact_error or address_error or interests_error or image_error):
            return render_template(
                'signup.html',
                username=username,
                full_name=full_name,
                email=email,
                contact_number=contact_number,
                home_address=home_address,
                environmental_interests=environmental_interests,
                username_error=username_error,
                full_name_error=full_name_error,
                email_error=email_error,
                password_error=password_error,
                contact_error=contact_error,
                address_error=address_error,
                interests_error=interests_error,
                image_error=image_error
            )

        # Hash password before storing (do NOT store plaintext passwords).
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert account into DB. Role is forced to volunteer; status defaults to active.
        try:
            with db.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (
                        username, password_hash, full_name, email,
                        contact_number, home_address, environmental_interests,
                        profile_image, role, status
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                ''', (
                    username, password_hash, full_name, email,
                    contact_number, home_address, environmental_interests,
                    profile_image_filename,
                    DEFAULT_USER_ROLE, 'active'
                ))
        except Exception:
            # Defensive: handle unexpected failures (e.g. unique constraint race condition).
            username_error = "Could not create account. Please try a different username."
            return render_template('signup.html',
                                   username=username, full_name=full_name, email=email,
                                   contact_number=contact_number, home_address=home_address,
                                   environmental_interests=environmental_interests,
                                   username_error=username_error)

        # Success message displayed on signup page
        return render_template('signup.html', signup_successful=True)

    return render_template('signup.html')


# ============================================================
# Profile View & Edit (All Roles)
# ============================================================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    View and edit profile details (assignment requirement):
    - full_name, home_address, contact_number, environmental_interests
    - optional profile_image upload
    """
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        # Read submitted fields
        full_name = request.form.get('full_name', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        home_address = request.form.get('home_address', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()

        # Basic validation errors dict (passed to template)
        errors = {}
        if not full_name:
            errors['full_name_error'] = "Full name is required."
        if not contact_number:
            errors['contact_error'] = "Contact number is required."
        if not home_address:
            errors['address_error'] = "Home address is required."
        if not environmental_interests:
            errors['interests_error'] = "Environmental interests are required."

        # Optional image upload
        profile_image_filename = None
        file = request.files.get('profile_image')
        if file and file.filename:
            if not allowed_file(file.filename):
                errors['image_error'] = "Profile image must be png/jpg/jpeg/gif/webp."
            else:
                safe_name = secure_filename(file.filename)
                base, ext = os.path.splitext(safe_name)
                # Keep filename consistent per user
                profile_image_filename = f"{session['username']}{ext.lower()}"
                file.save(os.path.join(UPLOAD_FOLDER, profile_image_filename))

        # If errors, re-load profile and re-render with messages
        if errors:
            with db.get_cursor() as cursor:
                cursor.execute('''
                    SELECT username, email, role, status, full_name, contact_number,
                           home_address, environmental_interests, profile_image
                    FROM users
                    WHERE user_id = %s;
                ''', (user_id,))
                profile_data = cursor.fetchone()

            # Keep user input so they don't lose it
            profile_data['full_name'] = full_name
            profile_data['contact_number'] = contact_number
            profile_data['home_address'] = home_address
            profile_data['environmental_interests'] = environmental_interests

            return render_template('profile.html', profile=profile_data, **errors)

        # Update DB (only update profile_image if a new file was uploaded)
        with db.get_cursor() as cursor:
            if profile_image_filename:
                cursor.execute('''
                    UPDATE users
                    SET full_name=%s, contact_number=%s, home_address=%s,
                        environmental_interests=%s, profile_image=%s
                    WHERE user_id=%s;
                ''', (full_name, contact_number, home_address,
                      environmental_interests, profile_image_filename, user_id))
            else:
                cursor.execute('''
                    UPDATE users
                    SET full_name=%s, contact_number=%s, home_address=%s,
                        environmental_interests=%s
                    WHERE user_id=%s;
                ''', (full_name, contact_number, home_address,
                      environmental_interests, user_id))

        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile'))

    # GET request: retrieve existing profile data
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, role, status, full_name, contact_number,
                   home_address, environmental_interests, profile_image
            FROM users
            WHERE user_id = %s;
        ''', (user_id,))
        profile_data = cursor.fetchone()

    return render_template('profile.html', profile=profile_data)


# ============================================================
# Change Password (All Roles)
# ============================================================

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """
    Change password feature (assignment requirement):
    - current password must match
    - new password must be validated
    - current password cannot be reused
    """
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        current_error = None
        new_error = None
        confirm_error = None

        # Fetch current password hash from database
        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id=%s;', (user_id,))
            row = cursor.fetchone()
        current_hash = row['password_hash']

        # Verify current password
        if not flask_bcrypt.check_password_hash(current_hash, current_password):
            current_error = "Current password is incorrect."

        # Validate new password complexity
        new_error = validate_password(new_password)

        # Confirm password match
        if new_password != confirm_password:
            confirm_error = "New password and confirmation do not match."

        # Prevent reuse of current password
        if current_error is None and flask_bcrypt.check_password_hash(current_hash, new_password):
            new_error = "New password cannot be the same as the current password."

        if current_error or new_error or confirm_error:
            return render_template('change_password.html',
                                   current_error=current_error,
                                   new_error=new_error,
                                   confirm_error=confirm_error)

        # Update DB with new bcrypt hash
        new_hash = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
        with db.get_cursor() as cursor:
            cursor.execute('UPDATE users SET password_hash=%s WHERE user_id=%s;',
                           (new_hash, user_id))

        flash("Password updated successfully.", "success")
        return redirect(url_for('profile'))

    return render_template('change_password.html')
