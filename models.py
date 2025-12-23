from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a global db instance that will be initialized in app.py
db = SQLAlchemy()


class Contract(db.Model):
    """Model for storing contract information"""
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(50), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(50), nullable=False)
    contract_date = db.Column(db.String(20), nullable=False)  # Format: DD/MM/YYYY
    document_status = db.Column(db.String(10), default='N')  # 'Y' for uploaded, 'N' for not uploaded
    contract_status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contract {self.contract_number}>'

    def to_dict(self):
        return {
            'id': self.contract_number,
            'customer': self.customer_name,
            'office': self.office,
            'contract_date': self.contract_date,
            'doc_status': self.document_status,
            'contract_status': self.contract_status
        }


class Document(db.Model):
    """Model for storing document information"""
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False)
    document_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='missing')  # 'uploaded' or 'missing'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contract = db.relationship('Contract', backref=db.backref('documents', lazy=True))
    
    def __repr__(self):
        return f'<Document {self.document_name} for Contract {self.contract_id}>'

    def to_dict(self):
        return {
            'name': self.document_name,
            'status': self.status
        }


class Collateral(db.Model):
    """Model for storing collateral information"""
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    engine_number = db.Column(db.String(50), nullable=False)
    chassis_number = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contract = db.relationship('Contract', backref=db.backref('collaterals', lazy=True))
    
    def __repr__(self):
        return f'<Collateral {self.category} for Contract {self.contract_id}>'

    def to_dict(self):
        return {
            'category': self.category,
            'engine_number': self.engine_number,
            'chassis_number': self.chassis_number,
            'color': self.color
        }