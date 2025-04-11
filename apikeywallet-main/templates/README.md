# Templates Directory

This directory contains all Jinja2 HTML templates used to render the web application's frontend.

## Purpose
- Define the structure and layout of web pages
- Dynamically generate HTML content based on backend data

## Important Files
- `base.html` — Base template with common layout (header, footer)
- `landing.html` — Landing page for the app
- `login.html` — User login page
- `register.html` — User registration page
- `wallet.html` — Main wallet/dashboard view
- `add_key.html` — Form to add a new API key
- `add_category.html` — Form to add a new category
- `edit_category.html` — Form to edit a category
- `manage_categories.html` — Manage categories page
- `edit_key.html` — (if exists) Edit API key page

## How Components Interact
- Templates extend `base.html` for consistent layout
- Use Jinja2 syntax to insert dynamic data from Flask
- Reference static assets (CSS, JS, images) via `url_for('static', filename=...)`

## Usage Example

```html
{% extends 'base.html' %}

{% block content %}
<h1>Welcome to KeyGuardian</h1>
{% endblock %}
