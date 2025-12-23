# Statistics Dashboard Mockup

This is a standalone Flask application that serves as a mockup for a statistics dashboard focused on fiduciary and mortgage contracts. It includes hardcoded data and a sidebar navigation for demonstration purposes.

## Features

- Dashboard with key statistics
- Detailed statistics page with charts visualization area
- Recipients management page
- Responsive design using Tailwind CSS
- Font Awesome icons
- Sidebar navigation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Visit `http://localhost:5001` in your browser

## Structure

- `app.py`: Main Flask application
- `routes.py`: Route definitions with hardcoded data
- `templates/`: HTML templates
  - `_layout.html`: Base template with sidebar
  - `dashboard.html`: Main dashboard page
  - `statistics.html`: Detailed statistics page
  - `recipients.html`: Recipients management page

## Data

All data in this mockup is generated randomly for demonstration purposes. In a real application, this would be replaced with actual database queries.

## Customization

You can easily extend this mockup by:
- Adding more routes in `routes.py`
- Creating additional templates in the `templates/` directory
- Modifying the sidebar in `_layout.html`
- Adding more detailed statistics or charts