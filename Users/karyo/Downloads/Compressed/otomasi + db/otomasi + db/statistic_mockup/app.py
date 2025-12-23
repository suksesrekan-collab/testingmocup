from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy instance without app
db = SQLAlchemy()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-for-statistics-mockup'
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