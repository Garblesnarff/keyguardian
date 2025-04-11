"""
forms.py - WTForms form classes

Defines forms for user registration, login, API key management, and category management.

Dependencies:
- Flask-WTF
- WTForms

@author KeyGuardian Team
"""

# ================================
# Third-party imports
# ================================
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# ================================
# Forms
# ================================
class RegistrationForm(FlaskForm):
    """
    User registration form.

    Fields:
        email (str): User email
        password (str): Password
        confirm_password (str): Password confirmation
        submit: Submit button
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    User login form.

    Fields:
        email (str): User email
        password (str): Password
        submit: Submit button
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddAPIKeyForm(FlaskForm):
    """
    Form to add a new API key.

    Fields:
        key_name (str): Name of the API key
        api_key (str): API key value
        category (int): Category ID
        submit: Submit button
    """
    key_name = StringField('Key Name', validators=[DataRequired(), Length(max=120)])
    api_key = StringField('API Key', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Add Key')

class AddCategoryForm(FlaskForm):
    """
    Form to add a new category.

    Fields:
        name (str): Category name
        submit: Submit button
    """
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Category')
