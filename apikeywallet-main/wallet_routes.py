"""
wallet_routes.py - Wallet and API key management routes

Contains routes for viewing wallet, adding, copying, deleting, editing API keys,
and fetching categories and keys.

Dependencies:
- Flask
- Flask-Login
- SQLAlchemy
- models.py
- forms.py
- utils.py
- app.py

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
import traceback

# ================================
# Third-party imports
# ================================
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

# ================================
# Project imports
# ================================
from models import APIKey, Category
from forms import AddAPIKeyForm
from app import db
from utils import encrypt_key, decrypt_key

# ================================
# Blueprint setup
# ================================
main = Blueprint('main', __name__)

# ================================
# Routes
# ================================
@main.route('/wallet')
@main.route('/wallet/<int:category_id>')
@login_required
def wallet(category_id=None):
    """
    Display the user's API keys grouped by category.

    Args:
        category_id (int, optional): Filter by category ID

    Returns:
        Rendered wallet template
    """
    try:
        current_app.logger.info(f"Fetching API keys for user {current_user.id}")
        categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()

        if category_id == 0:
            api_keys = APIKey.query.filter_by(user_id=current_user.id, category_id=None).all()
        elif category_id:
            api_keys = APIKey.query.filter_by(user_id=current_user.id, category_id=category_id).all()
        else:
            api_keys = APIKey.query.filter_by(user_id=current_user.id).all()

        api_keys = sorted(api_keys, key=lambda x: x.key_name.lower())

        grouped_keys = {category.name: [] for category in categories}
        grouped_keys['Uncategorized'] = []

        for key in api_keys:
            if key.category:
                grouped_keys[key.category.name].append(key)
            else:
                grouped_keys['Uncategorized'].append(key)

        for category in grouped_keys:
            grouped_keys[category] = sorted(grouped_keys[category], key=lambda x: x.key_name.lower())

        display_grouped_keys = {k: v for k, v in grouped_keys.items() if v}

        return render_template('wallet.html', grouped_keys=display_grouped_keys, all_categories=categories, current_category_id=category_id, debug=current_app.debug, show_add_key_button=True)
    except Exception as e:
        current_app.logger.error(f"Error in wallet route: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        flash('An error occurred while retrieving your wallet. Please try again later.', 'danger')
        return redirect(url_for('main.index'))

@main.route('/add_key', methods=['GET', 'POST'])
@login_required
def add_key():
    """
    Add a new API key.

    GET: Render add key form.
    POST: Validate form and save new key.

    Returns:
        Rendered template, JSON response, or error
    """
    form = AddAPIKeyForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category.choices = [(0, 'Uncategorized')] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        try:
            encrypted_key = encrypt_key(form.api_key.data)
            new_key = APIKey(
                user_id=current_user.id,
                key_name=form.key_name.data,
                encrypted_key=encrypted_key,
                category_id=form.category.data if form.category.data != 0 else None
            )
            db.session.add(new_key)
            db.session.commit()

            category = Category.query.get(new_key.category_id) if new_key.category_id else None
            return jsonify({
                'success': True,
                'message': 'API Key added successfully.',
                'key': {
                    'id': new_key.id,
                    'key_name': new_key.key_name,
                    'category_id': new_key.category_id,
                    'category_name': category.name if category else 'Uncategorized'
                }
            }), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in add_key route: {str(e)}")
            return jsonify({'success': False, 'error': 'An error occurred while adding the API key. Please try again.'}), 500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error in add_key route: {str(e)}")
            return jsonify({'success': False, 'error': 'An unexpected error occurred. Please try again.'}), 500

    if request.method == 'GET':
        return render_template('add_key.html', form=form)

    return jsonify({'success': False, 'errors': form.errors}), 400

@main.route('/copy_key/<int:key_id>', methods=['POST'])
@login_required
def copy_key(key_id):
    """
    Decrypt and return an API key.

    Args:
        key_id (int): API key ID

    Returns:
        JSON response with decrypted key or error
    """
    try:
        api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if not api_key:
            return jsonify({'error': 'API key not found or unauthorized'}), 403
        decrypted_key = decrypt_key(api_key.encrypted_key)
        return jsonify({'key': decrypted_key})
    except Exception as e:
        current_app.logger.error(f'Error in copy_key route: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred while processing the request'}), 500

@main.route('/delete_key/<int:key_id>', methods=['POST'])
@login_required
def delete_key(key_id):
    """
    Delete an API key.

    Args:
        key_id (int): API key ID

    Returns:
        JSON response indicating success or error
    """
    try:
        api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if api_key:
            db.session.delete(api_key)
            db.session.commit()
            return jsonify({'success': True, 'message': 'API Key deleted successfully.'}), 200
        else:
            return jsonify({'success': False, 'error': 'API Key not found or unauthorized.'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Database error in delete_key route: {str(e)}')
        return jsonify({'success': False, 'error': 'An error occurred while deleting the API key.'}), 500

@main.route('/edit_key/<int:key_id>', methods=['POST'])
@login_required
def edit_key(key_id):
    """
    Edit an API key's name.

    Args:
        key_id (int): API key ID

    Returns:
        JSON response indicating success or error
    """
    try:
        api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if api_key:
            new_name = request.json.get('key_name')
            if new_name:
                api_key.key_name = new_name
                db.session.commit()
                return jsonify({'success': True, 'message': 'API Key name updated successfully.', 'new_name': new_name}), 200
            else:
                return jsonify({'success': False, 'error': 'New key name is required.'}), 400
        else:
            return jsonify({'success': False, 'error': 'API Key not found or unauthorized.'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Database error in edit_key route: {str(e)}')
        return jsonify({'success': False, 'error': 'An error occurred while updating the API key name.'}), 500

@main.route('/get_key/<int:key_id>', methods=['POST'])
@login_required
def get_key(key_id):
    """
    Decrypt and return an API key.

    Args:
        key_id (int): API key ID

    Returns:
        JSON response with decrypted key or error
    """
    try:
        api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if api_key:
            decrypted_key = decrypt_key(api_key.encrypted_key)
            return jsonify({'key': decrypted_key}), 200
        else:
            return jsonify({'error': 'API Key not found or unauthorized.'}), 404
    except Exception as e:
        current_app.logger.error(f'Error in get_key route: {str(e)}')
        return jsonify({'error': 'An error occurred while retrieving the API key.'}), 500

@main.route('/get_categories_and_keys')
@login_required
def get_categories_and_keys():
    """
    Fetch all categories and API keys grouped by category.

    Returns:
        JSON response with categories and grouped keys
    """
    try:
        categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
        api_keys = APIKey.query.filter_by(user_id=current_user.id).order_by(APIKey.key_name).all()

        grouped_keys = {category.name: [] for category in categories}
        grouped_keys['Uncategorized'] = []

        for key in api_keys:
            if key.category:
                grouped_keys[key.category.name].append({
                    'id': key.id,
                    'key_name': key.key_name,
                    'category_id': key.category_id,
                    'date_added': key.date_added.isoformat()
                })
            else:
                grouped_keys['Uncategorized'].append({
                    'id': key.id,
                    'key_name': key.key_name,
                    'category_id': None,
                    'date_added': key.date_added.isoformat()
                })

        return jsonify({
            'categories': [{'id': c.id, 'name': c.name} for c in categories],
            'grouped_keys': grouped_keys
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_categories_and_keys route: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching categories and keys.'}), 500
