"""
auth_routes.py - Authentication-related Flask routes

Contains user registration, login, and logout endpoints.

Dependencies:
- Flask
- Flask-Login
- SQLAlchemy
- WTForms
- models.py
- forms.py
- app.py

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
import logging
import traceback

# ================================
# Third-party imports
# ================================
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError

# ================================
# Project imports
# ================================
from models import User
from forms import RegistrationForm, LoginForm
from app import db

# ================================
# Blueprint setup
# ================================
auth = Blueprint('auth', __name__)

# ================================
# Routes
# ================================
@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    GET: Render registration form.
    POST: Validate form and create user.

    Returns:
        Rendered template or redirect
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.wallet'))

    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(email=email)
        new_user.set_password(password)
        # Optionally: make first user admin
        if User.query.count() == 0:
            new_user.is_admin = True
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in an existing user.

    GET: Render login form.
    POST: Validate credentials and log in user.

    Returns:
        Rendered template or redirect
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.wallet'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                # Optionally: pass is_admin to frontend via session or API if needed
                return redirect(url_for('main.wallet'))
            else:
                flash('Invalid email or password.', 'danger')
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during login: {str(e)}")
            flash('An error occurred while processing your request. Please try again later.', 'danger')
        except Exception as e:
            current_app.logger.error(f"Unexpected error during login: {str(e)}")
            flash('An unexpected error occurred. Please try again later.', 'danger')

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Returns:
        Redirect to landing page
    """
    try:
        logout_user()
        flash('You have been logged out successfully.', 'success')
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error during logout: {str(e)}")
        flash('An error occurred during logout. Please try again.', 'danger')
    except Exception as e:
        current_app.logger.error(f"Unexpected error during logout: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'danger')
    return redirect(url_for('main.index'))
