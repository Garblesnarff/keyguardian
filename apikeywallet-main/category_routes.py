"""
category_routes.py - Category management routes

Contains routes for adding, updating, managing, editing, and deleting categories.

Dependencies:
- Flask
- Flask-Login
- SQLAlchemy
- models.py
- forms.py
- app.py

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
# None

# ================================
# Third-party imports
# ================================
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

# ================================
# Project imports
# ================================
from models import Category, APIKey
from forms import AddCategoryForm
from app import db

# ================================
# Blueprint setup
# ================================
categories = Blueprint('categories', __name__)

# ================================
# Routes
# ================================
@categories.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    """
    Add a new category.

    GET: Render add category form.
    POST: Validate form and save new category.

    Returns:
        Rendered template or redirect
    """
    form = AddCategoryForm()
    if form.validate_on_submit():
        try:
            new_category = Category(name=form.name.data, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully.', 'success')
            return redirect(url_for('main.wallet'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f'Database error in add_category route: {str(e)}')
            flash('An error occurred while adding the category. Please try again later.', 'danger')
    return render_template('add_category.html', form=form)

@categories.route('/update_key_category/<int:key_id>', methods=['POST'])
@login_required
def update_key_category(key_id):
    """
    Update the category of an API key.

    Args:
        key_id (int): API key ID

    Returns:
        JSON response indicating success or error
    """
    try:
        category_id = request.json.get('category_id')
        api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
        if api_key:
            if category_id == 0:
                api_key.category_id = None
                category_name = 'Uncategorized'
            else:
                category = Category.query.get(category_id)
                if not category:
                    return jsonify({'success': False, 'error': 'Category not found.'}), 404
                api_key.category_id = category_id
                category_name = category.name
            db.session.commit()
            return jsonify({'success': True, 'message': 'Category updated successfully.', 'category_name': category_name}), 200
        return jsonify({'success': False, 'error': 'API Key not found or unauthorized.'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Database error in update_key_category route: {str(e)}')
        return jsonify({'success': False, 'error': 'An error occurred while updating the category.'}), 500

@categories.route('/manage_categories')
@login_required
def manage_categories():
    """
    Display all categories for the current user.

    Returns:
        Rendered manage categories template
    """
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_categories.html', categories=categories)

@categories.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """
    Edit a category's name.

    Args:
        category_id (int): Category ID

    Returns:
        Rendered template or redirect
    """
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    form = AddCategoryForm(obj=category)
    if form.validate_on_submit():
        try:
            category.name = form.name.data
            db.session.commit()
            flash('Category updated successfully.', 'success')
            return redirect(url_for('categories.manage_categories'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f'Database error in edit_category route: {str(e)}')
            flash('An error occurred while updating the category. Please try again later.', 'danger')
    return render_template('edit_category.html', form=form, category=category)

@categories.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """
    Delete a category.

    Args:
        category_id (int): Category ID

    Returns:
        Redirect to manage categories page
    """
    try:
        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully.', 'success')
        return redirect(url_for('categories.manage_categories'))
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Database error in delete_category route: {str(e)}')
        flash('An error occurred while deleting the category. Please try again later.', 'danger')
        return redirect(url_for('main.manage_categories'))
