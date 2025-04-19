"""
models.py - SQLAlchemy ORM models

Defines User, APIKey, and Category database models.

Dependencies:
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug security
- datetime
- logging

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
from datetime import datetime
import logging

# ================================
# Third-party imports
# ================================
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ================================
# Project imports
# ================================
from app import db

# ================================
# Models
# ================================
class User(UserMixin, db.Model):
    """
    User account model.

    Attributes:
        id (int): Primary key
        email (str): User email
        password_hash (str): Hashed password
        date_joined (datetime): Account creation date
        api_keys (list): User's API keys
        categories (list): User's categories
        is_admin (bool): Admin role flag
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    api_keys = db.relationship('APIKey', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        """
        Hash and set the user's password.

        Args:
            password (str): Plaintext password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify a plaintext password against stored hash.

        Args:
            password (str): Plaintext password

        Returns:
            bool: True if password matches
        """
        return check_password_hash(self.password_hash, password)

class APIKey(db.Model):
    """
    API key model.

    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        key_name (str): Name of the API key
        encrypted_key (str): Encrypted API key
        date_added (datetime): When the key was added
        category_id (int): Foreign key to Category
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    key_name = db.Column(db.String(120), nullable=False)
    encrypted_key = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        super(APIKey, self).__init__(*args, **kwargs)
        logging.info(f"Creating new APIKey: user_id={self.user_id}, key_name={self.key_name}, category_id={self.category_id}")

class Category(db.Model):
    """
    Category model for grouping API keys.

    Attributes:
        id (int): Primary key
        name (str): Category name
        user_id (int): Foreign key to User
        api_keys (list): API keys in this category
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    api_keys = db.relationship('APIKey', backref='category', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        logging.info(f"Creating new Category: name={self.name}, user_id={self.user_id}")
