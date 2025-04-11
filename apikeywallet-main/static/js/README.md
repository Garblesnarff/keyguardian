# JavaScript Directory

This directory contains JavaScript files that add interactivity and dynamic behavior to the web application.

## Purpose
- Enhance user experience with client-side scripting
- Handle UI events, AJAX requests, and DOM manipulation

## Important Files
- `main.js` — Main JavaScript file for the application

## How Components Interact
- Included in HTML templates via `<script>` tags
- Can communicate with backend APIs using AJAX/fetch
- Works alongside CSS to provide a responsive, interactive UI

## Usage Example

In a Jinja2 template:

```html
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
