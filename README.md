# testinguistatistic
pake db sqlite buat mockup

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

2. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env .env
   # Edit .env to add your database configuration (optional)
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Visit `http://localhost:5001` in your browser

## Database Configuration

By default, the application uses a local SQLite database. To use an external database (like Hostinger):

1. Set the `DATABASE_URL` environment variable in your `.env` file
2. The application will automatically use the external database when this variable is set

## Data Migration

To migrate data from the local SQLite database to an external database (like Hostinger), use the migration script:

```bash
python migrate_data.py
```

See `README_MIGRATION.md` for detailed instructions on database migration.

## Structure

- `app.py`: Main Flask application
- `routes.py`: Route definitions with hardcoded data
- `models.py`: Database models
- `migrate_data.py`: Data migration script
- `templates/`: HTML templates
  - `_layout.html`: Base template with sidebar
  - `dashboard.html`: Main dashboard page
  - `statistics.html`: Detailed statistics page
  - `recipients.html`: Recipients management page
  - `uploadlist.html`: Upload list page
  - `aktapage.html`: Document details page

## Data

All data in this mockup is generated randomly for demonstration purposes. In a real application, this would be replaced with actual database queries.

## Customization

You can easily extend this mockup by:
- Adding more routes in `routes.py`
- Creating additional templates in the `templates/` directory
- Modifying the sidebar in `_layout.html`
- Adding more detailed statistics or charts