from hashlib import sha256
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login requests by validating email and password, checking the
    user's password hash, and flashing error or success messages accordingly. Upon
    successful login, it logs the user in and redirects them to the `checking` page.

    Returns:
        Union[str,redirect_to,Response]: Either a redirect to the 'checking' view,
        or a rendered 'login.html' template with the current user.

    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully! Welcome back, ' + user.first_name +"!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.checking'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Handles user logout by calling the `logout_user` function to end the user's
    session and redirects the user to the login page after successful logout.

    Returns:
        Response: Redirecting the user to the login page.

    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Processes user sign-up requests by validating input data, checking for existing
    email addresses, and creating a new user account upon successful validation.

    Returns:
        Union[str,RedirectResponse]: Either a rendered HTML template of the
        'sign_up.html' page or a redirect to the 'checking' page.

    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        ssn = request.form.get('ssn')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'), ssn = generate_password_hash(ssn,'sha256'), address=address, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.checking'))

    return render_template("sign_up.html", user=current_user,)
