import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import Contract, Document, Collateral

# Load environment variables
load_dotenv()

def create_app_with_db(db_uri):
    """Create a Flask app instance with the specified database URI"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy()
    db.init_app(app)
    
    return app, db

def migrate_data():
    """Migrate data from SQLite database to the Hostinger database"""
    print("Starting data migration...")
    
    # Source database (SQLite)
    source_app, source_db = create_app_with_db('sqlite:///statistics.db')
    
    # Destination database (Hostinger) - using DATABASE_URL from environment
    destination_db_uri = os.getenv('DATABASE_URL')
    if not destination_db_uri or destination_db_uri == 'your_hostinger_database_url_here':
        print("Error: DATABASE_URL environment variable not properly set.")
        print("Please set your Hostinger database URL in the .env file.")
        print("The URL should follow the format: mysql://username:password@hostname:port/database_name")
        return
    
    try:
        destination_app, destination_db = create_app_with_db(destination_db_uri)
    except Exception as e:
        print(f"Error connecting to destination database: {e}")
        print("Please verify your database URL is correct and the database is accessible.")
        return
    
    # Create tables in the destination database
    with destination_app.app_context():
        destination_db.create_all()
        print("Destination database tables created.")
    
    # Copy data from source to destination
    with source_app.app_context():
        # Get all contracts from source
        source_contracts = Contract.query.all()
        print(f"Found {len(source_contracts)} contracts to migrate.")
        
        if not source_contracts:
            print("No contracts found in source database. Creating mock data first...")
            from routes import create_mockup_data
            create_mockup_data()
            source_contracts = Contract.query.all()
            print(f"Created mock data: {len(source_contracts)} contracts available.")
    
    # Process migration in a single transaction in the destination app context
    with destination_app.app_context():
        # Check if destination already has data
        existing_contracts = Contract.query.all()
        if existing_contracts:
            print(f"Destination already has {len(existing_contracts)} contracts. Skipping migration to prevent duplicates.")
            return
        
        # Copy contracts
        for source_contract in source_contracts:
            # Check if contract already exists in destination
            dest_contract = Contract.query.filter_by(contract_number=source_contract.contract_number).first()
            if not dest_contract:
                # Create new contract in destination
                dest_contract = Contract(
                    contract_number=source_contract.contract_number,
                    customer_name=source_contract.customer_name,
                    office=source_contract.office,
                    contract_date=source_contract.contract_date,
                    document_status=source_contract.document_status,
                    contract_status=source_contract.contract_status,
                    created_at=source_contract.created_at
                )
                destination_db.session.add(dest_contract)
        
        # Commit contracts first to generate IDs for relationships
        destination_db.session.commit()
        
        # Copy documents
        with source_app.app_context():
            for source_contract in source_contracts:
                # Get source contract with the same number from destination
                dest_contract = Contract.query.filter_by(contract_number=source_contract.contract_number).first()
                
                # Get source documents
                source_documents = Document.query.filter_by(contract_id=source_contract.id).all()
                
                for source_doc in source_documents:
                    # Create new document in destination
                    dest_doc = Document(
                        contract_id=dest_contract.id,
                        document_name=source_doc.document_name,
                        status=source_doc.status,
                        created_at=source_doc.created_at
                    )
                    destination_db.session.add(dest_doc)
        
        # Commit documents
        destination_db.session.commit()
        
        # Copy collaterals
        with source_app.app_context():
            for source_contract in source_contracts:
                # Get source contract with the same number from destination
                dest_contract = Contract.query.filter_by(contract_number=source_contract.contract_number).first()
                
                # Get source collaterals
                source_collaterals = Collateral.query.filter_by(contract_id=source_contract.id).all()
                
                for source_col in source_collaterals:
                    # Create new collateral in destination
                    dest_col = Collateral(
                        contract_id=dest_contract.id,
                        category=source_col.category,
                        engine_number=source_col.engine_number,
                        chassis_number=source_col.chassis_number,
                        color=source_col.color,
                        created_at=source_col.created_at
                    )
                    destination_db.session.add(dest_col)
        
        # Final commit
        destination_db.session.commit()
        
        print("Data migration completed successfully!")
        print(f"Migrated {len(source_contracts)} contracts, with their documents and collaterals.")

def verify_migration():
    """Verify that the data was migrated correctly"""
    destination_db_uri = os.getenv('DATABASE_URL')
    if not destination_db_uri or destination_db_uri == 'your_hostinger_database_url_here':
        print("Error: DATABASE_URL environment variable not properly set.")
        print("Please set your Hostinger database URL in the .env file.")
        print("The URL should follow the format: mysql://username:password@hostname:port/database_name")
        return
    
    try:
        destination_app, destination_db = create_app_with_db(destination_db_uri)
    except Exception as e:
        print(f"Error connecting to destination database: {e}")
        print("Please verify your database URL is correct and the database is accessible.")
        return
    
    with destination_app.app_context():
        contracts_count = Contract.query.count()
        documents_count = Document.query.count()
        collaterals_count = Collateral.query.count()
        
        print(f"Verification Results:")
        print(f"- Contracts: {contracts_count}")
        print(f"- Documents: {documents_count}")
        print(f"- Collaterals: {collaterals_count}")

if __name__ == "__main__":
    print("Data Migration Tool for Statistic Mockup App")
    print("=============================================")
    
    action = input("Choose an action: (m)igrate or (v)erify: ").lower()
    
    if action.startswith('m'):
        migrate_data()
    elif action.startswith('v'):
        verify_migration()
    else:
        print("Invalid option. Use 'm' to migrate data or 'v' to verify migration.")