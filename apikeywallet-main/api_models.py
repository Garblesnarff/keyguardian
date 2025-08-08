from flask_restx import fields
from extensions import api

# ================================
# API Models
# ================================

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email'),
})

category_model = api.model('Category', {
    'id': fields.Integer(readOnly=True, description='The category unique identifier'),
    'name': fields.String(required=True, description='The category name'),
})

api_key_model = api.model('APIKey', {
    'id': fields.Integer(readOnly=True, description='The API key unique identifier'),
    'key_name': fields.String(required=True, description='The API key name'),
    'category_id': fields.Integer(description='The category ID'),
    'date_added': fields.DateTime(readOnly=True, description='The date the API key was added'),
})

grouped_keys_model = api.model('GroupedKeys', {
    'categories': fields.List(fields.Nested(category_model)),
    'grouped_keys': fields.Raw(description='A dictionary of API keys grouped by category name'),
})
