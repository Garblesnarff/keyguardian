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
from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Namespace, Resource
from api_models import category_model

# ================================
# Project imports
# ================================
from models import Category, APIKey
from forms import AddCategoryForm
from extensions import db

# ================================
# Blueprint setup
# ================================
category_ns = Namespace('categories', description='Category related operations')

@category_ns.route('/add_category')
class AddCategory(Resource):
    @login_required
    def get(self):
        """Render the add category form."""
        form = AddCategoryForm()
        return render_template('add_category.html', form=form)

    @login_required
    @category_ns.doc('add_category')
    @category_ns.expect(category_model)
    @category_ns.marshal_with(category_model)
    def post(self):
        """Add a new category."""
        form = AddCategoryForm()
        if form.validate_on_submit():
            try:
                new_category = Category(name=form.name.data, user_id=current_user.id)
                db.session.add(new_category)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Category added successfully.',
                    'category': {
                        'id': new_category.id,
                        'name': new_category.name,
                    }
                }), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                current_app.logger.error(f'Database error in add_category route: {str(e)}')
                return jsonify({'success': False, 'error': 'An error occurred while adding the category.'}), 500
        return jsonify({'success': False, 'errors': form.errors}), 400

@category_ns.route('/update_key_category/<int:key_id>')
class UpdateKeyCategory(Resource):
    @login_required
    @category_ns.doc('update_key_category')
    def post(self, key_id):
        """Update the category of an API key."""
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

@category_ns.route('/manage_categories')
class ManageCategories(Resource):
    @login_required
    def get(self):
        """Display all categories for the current user."""
        categories = Category.query.filter_by(user_id=current_user.id).all()
        return render_template('manage_categories.html', categories=categories)

@category_ns.route('/edit_category/<int:category_id>')
class EditCategory(Resource):
    @login_required
    def get(self, category_id):
        """Render the edit category form."""
        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
        form = AddCategoryForm(obj=category)
        return render_template('edit_category.html', form=form, category=category)

    @login_required
    @category_ns.doc('edit_category')
    @category_ns.expect(category_model)
    @category_ns.marshal_with(category_model)
    def post(self, category_id):
        """Edit a category's name."""
        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
        form = AddCategoryForm(obj=category)
        if form.validate_on_submit():
            try:
                category.name = form.name.data
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Category updated successfully.',
                    'category': {
                        'id': category.id,
                        'name': category.name,
                    }
                }), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                current_app.logger.error(f'Database error in edit_category route: {str(e)}')
                return jsonify({'success': False, 'error': 'An error occurred while updating the category.'}), 500
        return jsonify({'success': False, 'errors': form.errors}), 400

@category_ns.route('/delete_category/<int:category_id>')
class DeleteCategory(Resource):
    @login_required
    @category_ns.doc('delete_category')
    def post(self, category_id):
        """Delete a category."""
        try:
            category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
            db.session.delete(category)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Category deleted successfully.'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f'Database error in delete_category route: {str(e)}')
            return jsonify({'success': False, 'error': 'An error occurred while deleting the category.'}), 500
