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
from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Namespace, Resource
from api_models import user_model

# ================================
# Project imports
# ================================
from models import User
from forms import RegistrationForm, LoginForm
from extensions import db

# ================================
# Blueprint setup
# ================================
auth_ns = Namespace('auth', description='Authentication related operations')

@auth_ns.route('/register')
class Register(Resource):
    def get(self):
        """Render the registration form."""
        form = RegistrationForm()
        return render_template('register.html', form=form)

    @auth_ns.doc('register_user')
    @auth_ns.expect(user_model)
    @auth_ns.marshal_with(user_model)
    def post(self):
        """Register a new user."""
        if current_user.is_authenticated:
            return redirect(url_for('main.wallet'))

        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                email = form.email.data
                password = form.password.data

                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Email already exists.', 'danger')
                    return redirect(url_for('auth.register'))

                new_user = User(email=email)
                new_user.set_password(password)
                if User.query.count() == 0:
                    new_user.is_admin = True
                db.session.add(new_user)
                db.session.commit()

                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except SQLAlchemyError as e:
                db.session.rollback()
                current_app.logger.error(f"Database error during registration: {str(e)}")
                flash('An error occurred while processing your request. Please try again later.', 'danger')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Unexpected error during registration: {str(e)}")
                flash('An unexpected error occurred. Please try again later.', 'danger')
        return render_template('register.html', form=form)

@auth_ns.route('/login')
class Login(Resource):
    def get(self):
        """Render the login form."""
        form = LoginForm()
        return render_template('login.html', form=form)

    @auth_ns.doc('login_user')
    @auth_ns.expect(user_model)
    def post(self):
        """Log in an existing user."""
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

@auth_ns.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        """Log out the current user."""
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
