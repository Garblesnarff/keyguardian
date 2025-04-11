# CSS Stylesheets Directory

This directory contains all CSS files used to style the web application's frontend.

## Purpose
- Define the visual appearance of the app
- Control layout, typography, colors, and responsiveness

## Important Files
- `styles.css` — Main stylesheet for the entire application

## How Components Interact
- Linked in HTML templates via `<link>` tags
- Works with static images and fonts to create the UI design
- Can be extended with additional CSS files if needed

## Usage Example

In a Jinja2 template:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
