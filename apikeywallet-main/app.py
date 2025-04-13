"""
app.py - Flask application factory and setup

This file initializes the Flask app, configures extensions, sets up the database,
login manager, and registers blueprints.

Dependencies:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- SQLAlchemy
- python-dotenv

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
import os
import logging
from urllib.parse import urlparse

# ================================
# Third-party imports
# ================================
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from dotenv import load_dotenv

# ================================
# Environment setup
# ================================
load_dotenv()

# ================================
# Logging configuration
# ================================
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ================================
# Initialize extensions
# ================================
db = SQLAlchemy()
migrate = None
login_manager = LoginManager()

# ================================
# Flask app factory
# ================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQLAlchemy echo mode for debugging

parsed_url = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
logger.info(f"Database URL: {parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}")

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# ================================
# User loader
# ================================
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by ID for Flask-Login session management.

    Args:
        user_id (int): User ID

    Returns:
        User instance or None
    """
    from models import User
    return User.query.get(int(user_id))

# ================================
# Database session management
# ================================
def get_db_session():
    """
    Create a new scoped SQLAlchemy session.

    Returns:
        scoped_session: SQLAlchemy session
    """
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True, pool_recycle=3600)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return db_session

@app.before_request
def before_request():
    """
    Attach a new database session to Flask's `g` before each request.
    """
    g.db = get_db_session()

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Close the database session at the end of the request/app context.

    Args:
        exception (Exception, optional): Exception if any
    """
    db_session = g.pop('db', None)
    if db_session is not None:
        db_session.close()

# ================================
# Import models
# ================================
from models import User, APIKey, Category

# ================================
# Create tables
# ================================
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {str(e)}")

# ================================
# Register blueprints
# ================================
from wallet_routes import main as wallet_blueprint
app.register_blueprint(wallet_blueprint)

from auth_routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from category_routes import categories as category_blueprint
app.register_blueprint(category_blueprint)

# ================================
# Run the app
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
