from flask import Flask
from models import db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-for-statistics-mockup')
    
    # Use external database if DATABASE_URL is set and not a placeholder, otherwise use SQLite
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url != 'your_hostinger_database_url_here':
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    # Import routes after initializing db to avoid circular imports
    from routes import register_routes
    register_routes(app)  # Register routes with the app
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)