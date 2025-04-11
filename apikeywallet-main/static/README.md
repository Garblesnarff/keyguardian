# Static Assets Directory

This directory contains all static files served directly by the Flask application, including CSS, JavaScript, and images.

## Purpose
- Store frontend assets that do not change dynamically
- Organize stylesheets, scripts, and media files

## Important Subdirectories
- `css/` — Stylesheets for the web app
- `js/` — JavaScript files for client-side interactivity
- `img/` — Images and icons used in the UI

## How Components Interact
- HTML templates reference these static files using Flask's `url_for('static', filename='path/to/file')`
- CSS styles define the look and feel of the app
- JavaScript adds interactivity and dynamic behavior

## Usage Example

In a Jinja2 template:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
<img src="{{ url_for('static', filename='img/keyguardian-logo.webp') }}" alt="Logo">
