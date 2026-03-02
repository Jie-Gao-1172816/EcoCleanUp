


from EcoCleanUp import app, db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import re
import uuid

# ------------------------------------------------------------
# Config / helpers
# ------------------------------------------------------------

flask_bcrypt = Bcrypt(app)
DEFAULT_USER_ROLE = 'volunteer'

# Store uploaded images as static files; DB stores filename only.
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Return True if the file extension is allowed for profile image uploads."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_password(pw: str):
    """
    Validate password complexity (assignment requirement).
    Returns an error message string if invalid, otherwise None.
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
    """Redirect logged-in users to role-specific home pages."""
    if session.get('loggedin'):
        role = session.get('role')
        if role == 'volunteer':
            return url_for('volunteer_home')
        if role == 'event_leader':
            return url_for('leader_home')
        if role == 'admin':
            return url_for('admin_home')
        # Defensive: invalid role/session -> logout
        return url_for('logout')
    return url_for('login')


# ============================================================
# Public Home Page
# ============================================================


@app.route('/')
def home():
    """ home page; logged-in users go to their dashboard."""
    if session.get('loggedin'):
        return redirect(user_home_url())
    return render_template('home.html')  # should extend base_public.html


# ============================================================
# Login / Logout
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Single login form for all roles (volunteer, event leader, admin).
    Errors are shown on the same page (no extra steps).
    """
    if session.get('loggedin'):
        return redirect(user_home_url())

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Simple guard: show a clear message without redirecting.
        if not username or not password:
            return render_template('login.html', username=username, missing_fields=True)

        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT user_id, username, password_hash, role, status
                FROM users
                WHERE username = %s;
            """, (username,))
            account = cursor.fetchone()

        if account is None:
            # Username not found
            return render_template('login.html', username=username, username_invalid=True)

        if account.get('status') != 'active':
            # User exists but inactive
            return render_template('login.html', username=username, account_inactive=True)

        # Verify bcrypt password
        if flask_bcrypt.check_password_hash(account['password_hash'], password):
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            session['role'] = account['role']
            return redirect(user_home_url())

        # Password incorrect
        return render_template('login.html', username=username, password_invalid=True)

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout: clear session and return to login page."""
    session.clear()
    return redirect(url_for('login'))


# ============================================================
# Volunteer Registration (Signup)
# ============================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Volunteer registration only:
    - Role is always 'volunteer'
    - Useful validation hints and errors shown inline
    - Includes password confirmation (double entry)
    """
    if session.get('loggedin'):
        return redirect(user_home_url())

    if request.method == 'POST':
        # Collect form fields
        username = request.form.get('username', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        home_address = request.form.get('home_address', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Errors passed to template
        username_error = None
        email_error = None
        password_error = None
        confirm_error = None
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
            with db.get_cursor() as cursor:
                cursor.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
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

        # ---------- Password rules ----------
        password_error = validate_password(password)

        # Password confirmation (double entry)
        if password and password != confirm_password:
            confirm_error = "Password and confirmation do not match."

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
        profile_image_filename = None
        file = request.files.get('profile_image')
        if file and file.filename:
            if not allowed_file(file.filename):
                image_error = "Profile image must be png/jpg/jpeg/gif/webp."
            else:
                safe_name = secure_filename(file.filename)
                _, ext = os.path.splitext(safe_name)
                profile_image_filename = f"{username}{ext.lower()}"
                file.save(os.path.join(UPLOAD_FOLDER, profile_image_filename))

        # If any validation error occurred, re-render signup page with hints
        if (username_error or full_name_error or email_error or password_error or confirm_error or
                contact_error or address_error or interests_error or image_error):
            return render_template(
                'signup.html',
                # preserve user input
                username=username,
                full_name=full_name,
                email=email,
                contact_number=contact_number,
                home_address=home_address,
                environmental_interests=environmental_interests,

                # errors
                username_error=username_error,
                full_name_error=full_name_error,
                email_error=email_error,
                password_error=password_error,
                confirm_error=confirm_error,
                contact_error=contact_error,
                address_error=address_error,
                interests_error=interests_error,
                image_error=image_error
            )

        # Hash password before storing (never store plaintext)
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (
                        username, password_hash, full_name, email,
                        contact_number, home_address, environmental_interests,
                        profile_image, role, status
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """, (
                    username, password_hash, full_name, email,
                    contact_number, home_address, environmental_interests,
                    profile_image_filename,
                    DEFAULT_USER_ROLE, 'active'
                ))
        except Exception:
            # Defensive: unexpected failure (e.g. race on unique constraint)
            username_error = "Could not create account. Please try a different username."
            return render_template(
                'signup.html',
                username=username,
                full_name=full_name,
                email=email,
                contact_number=contact_number,
                home_address=home_address,
                environmental_interests=environmental_interests,
                username_error=username_error
            )

        # Show success message on the same page 
        return render_template('signup.html', signup_successful=True)

    return render_template('signup.html')


# ============================================================
# Profile View & Edit (All Roles)
# ============================================================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and edit profile for all roles; profile image upload/removal."""
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Always fetch current user record (needed for image removal/replacement)
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT user_id, username, email, full_name,
                   contact_number, home_address,
                   profile_image, environmental_interests,
                   role, status
            FROM users
            WHERE user_id=%s;
        """, (user_id,))
        user = cursor.fetchone()

    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Read editable fields
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        home_address = request.form.get('home_address', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()

        # Checkbox for removing current image (from updated profile.html)
        remove_image = request.form.get('remove_image') == '1'

        # -----------------------
        # Validation
        # -----------------------
        if not full_name:
            flash("Full name is required.", "warning")
            return redirect(url_for('profile'))

        if not email:
            flash("Email is required.", "warning")
            return redirect(url_for('profile'))

        if len(email) > 100:
            flash("Email cannot exceed 100 characters.", "warning")
            return redirect(url_for('profile'))

        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address.", "warning")
            return redirect(url_for('profile'))

        # Email uniqueness check (allow keeping current email)
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT 1
                FROM users
                WHERE email = %s AND user_id <> %s;
            """, (email, user_id))
            if cursor.fetchone() is not None:
                flash("That email address is already in use.", "warning")
                return redirect(url_for('profile'))

        # -----------------------
        # Image handling
        # -----------------------
        file = request.files.get('profile_image')
        new_filename = None

        # If user uploads a new image, it replaces the existing one
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Only png/jpg/jpeg/gif/webp images are allowed.", "warning")
                return redirect(url_for('profile'))

            ext = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"user_{user_id}_{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, secure_filename(new_filename))
            file.save(save_path)

            # If a new image is uploaded, ignore remove_image checkbox
            remove_image = False

        # If removing image (and no new upload), set profile_image to NULL
        image_to_delete = None
        if remove_image and user.get('profile_image'):
            image_to_delete = user['profile_image']

        # If replacing image, delete old one after successful update
        if new_filename and user.get('profile_image'):
            image_to_delete = user['profile_image']

        # -----------------------
        # Update DB
        # -----------------------
        with db.get_cursor() as cursor:
            if new_filename:
                cursor.execute("""
                    UPDATE users
                    SET email=%s,
                        full_name=%s,
                        contact_number=%s,
                        home_address=%s,
                        environmental_interests=%s,
                        profile_image=%s
                    WHERE user_id=%s;
                """, (
                    email,
                    full_name,
                    contact_number or None,
                    home_address or None,
                    environmental_interests or None,
                    new_filename,
                    user_id
                ))
            elif remove_image:
                cursor.execute("""
                    UPDATE users
                    SET email=%s,
                        full_name=%s,
                        contact_number=%s,
                        home_address=%s,
                        environmental_interests=%s,
                        profile_image=NULL
                    WHERE user_id=%s;
                """, (
                    email,
                    full_name,
                    contact_number or None,
                    home_address or None,
                    environmental_interests or None,
                    user_id
                ))
            else:
                cursor.execute("""
                    UPDATE users
                    SET email=%s,
                        full_name=%s,
                        contact_number=%s,
                        home_address=%s,
                        environmental_interests=%s
                    WHERE user_id=%s;
                """, (
                    email,
                    full_name,
                    contact_number or None,
                    home_address or None,
                    environmental_interests or None,
                    user_id
                ))

        # Try to remove old image file 
        if image_to_delete:
            try:
                old_path = os.path.join(UPLOAD_FOLDER, image_to_delete)
                if os.path.isfile(old_path):
                    os.remove(old_path)
            except Exception:
                # Ignore file deletion errors (DB update already succeeded)
                pass

        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile'))


    return render_template('profile.html', user=user)


# ============================================================
# Change Password (All Roles)
# ============================================================

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """
    Change password (all roles):
    - Verifies current password
    - Enforces the same complexity rules as registration
    - Requires confirmation (double entry)
    - Prevents reuse of the current password
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

        # Fetch current hash
        with db.get_cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE user_id=%s;", (user_id,))
            row = cursor.fetchone()

        if not row:
            flash("User not found.", "warning")
            return redirect(url_for('logout'))

        current_hash = row['password_hash']

        # Validate current password
        if not flask_bcrypt.check_password_hash(current_hash, current_password):
            current_error = "Current password is incorrect."

        # Validate new password complexity
        new_error = validate_password(new_password)

        # Confirm match
        if new_password != confirm_password:
            confirm_error = "New password and confirmation do not match."

        # Prevent reusing the old password (only if current password was correct)
        if current_error is None and new_password and flask_bcrypt.check_password_hash(current_hash, new_password):
            new_error = "New password cannot be the same as the current password."

        if current_error or new_error or confirm_error:
            return render_template(
                'change_password.html',
                current_error=current_error,
                new_error=new_error,
                confirm_error=confirm_error
            )

        # Save new hash
        new_hash = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
        with db.get_cursor() as cursor:
            cursor.execute(
                "UPDATE users SET password_hash=%s WHERE user_id=%s;",
                (new_hash, user_id)
            )

        flash("Password updated successfully.", "success")
        return redirect(url_for('profile'))

    return render_template('change_password.html')