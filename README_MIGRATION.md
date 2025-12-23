# Database Migration Guide

This guide explains how to migrate your local SQLite database to a Hostinger database.

## Prerequisites

1. Make sure you have Python and pip installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   # If python-dotenv is not in requirements.txt, install it separately:
   pip install python-dotenv
   ```

## Setting up Hostinger Database Connection

1. Log into your Hostinger control panel
2. Navigate to the database management section
3. Create a new MySQL database if you haven't already
4. Note down the database hostname, username, password, database name, and port

## Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env .env
   ```

2. Edit the `.env` file and replace the placeholder values:
   - Replace `your_hostinger_database_url_here` with your actual Hostinger database URL
   - The format should be: `mysql://username:password@hostname:port/database_name`

   Example:
   ```
   DATABASE_URL=mysql://your_username:your_password@sql.hostinger.com/your_database_name
   ```

## Running the Migration

1. First, make sure your local database has data:
   ```bash
   python app.py
   ```
   Visit `http://localhost:5001/uploadlist` to trigger the creation of sample data if needed.

2. Run the migration script:
   ```bash
   python migrate_data.py
   ```
   
   When prompted, type `m` to start the migration.

3. After migration, you can verify the data was transferred:
   ```bash
   python migrate_data.py
   ```
   
   When prompted, type `v` to verify the migration.

## Using the Application with Hostinger Database

Once migration is complete, your application will automatically use the Hostinger database when the `DATABASE_URL` environment variable is set.

Start your application normally:
```bash
python app.py
```

## Troubleshooting

- If you get a connection error, verify your Hostinger database credentials
- Make sure your Hostinger database allows external connections
- Check that the database URL format is correct
- Ensure the database tables were created properly

## Reverting Migration

If you need to start fresh, you can clear the Hostinger database tables and run the migration again.