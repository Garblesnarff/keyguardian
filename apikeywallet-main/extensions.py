from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restx import Api

db = SQLAlchemy()
login_manager = LoginManager()
api = Api()
