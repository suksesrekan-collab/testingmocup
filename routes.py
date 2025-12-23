from flask import render_template
import random
from datetime import datetime, timedelta
from models import db, Contract as ContractModel, Document as DocumentModel, Collateral as CollateralModel


# Hardcoded statistics data
def get_statistics_data():
    # Generate random statistics data for demonstration
    return {
        'menunggu_validasi': random.randint(5, 25),
        'sudah_validasi': random.randint(50, 150),
        'fiducia_belum_lunas': random.randint(10, 40),
        'fiducia_lunas': random.randint(30, 100),
        'roya_belum_lunas': random.randint(8, 30),
        'roya_lunas': random.randint(20, 80),
        'due_date_count': random.randint(3, 15),
        'total_submissions': random.randint(100, 300),
        'total_contracts': random.randint(80, 250)
    }


def register_routes(app):
    @app.route('/')
    def dashboard():
        stats = get_statistics_data()
        return render_template('dashboard.html', stats=stats)

    @app.route('/statistics')
    def statistics():
        stats = get_statistics_data()
        return render_template('statistics.html', stats=stats)

    @app.route('/recipients')
    def recipients():
        # Sample recipients data
        recipients_list = [
            {'id': 1, 'name': 'PT. Maju Jaya', 'contracts': random.randint(5, 20)},
            {'id': 2, 'name': 'CV. Sejahtera Bersama', 'contracts': random.randint(3, 15)},
            {'id': 3, 'name': 'UD. Sentosa Abadi', 'contracts': random.randint(2, 10)},
            {'id': 4, 'name': 'PD. Makmur Sejati', 'contracts': random.randint(1, 8)},
        ]
        return render_template('recipients.html', recipients=recipients_list)

    @app.route('/uploadlist')
    def uploadlist():
        # Get all contracts from database
        contracts = ContractModel.query.all()
        # If no contracts in DB, create some mockup data
        if not contracts:
            create_mockup_data()
            contracts = ContractModel.query.all()
        
        # Convert to the format expected by the template
        contracts_data = [contract.to_dict() for contract in contracts]
        return render_template('uploadlist.html', contracts=contracts_data)

    @app.route('/aktapage')
    def aktapage():
        # Get first contract for demo purposes
        contract = ContractModel.query.first()
        if not contract:
            create_mockup_data()
            contract = ContractModel.query.first()
        
        # Get documents and collaterals for this contract
        documents = [doc.to_dict() for doc in contract.documents]
        collaterals = [coll.to_dict() for coll in contract.collaterals]
        
        doc_details = {
            'documents': documents,
            'collaterals': collaterals
        }
        return render_template('aktapage.html', doc_details=doc_details)


