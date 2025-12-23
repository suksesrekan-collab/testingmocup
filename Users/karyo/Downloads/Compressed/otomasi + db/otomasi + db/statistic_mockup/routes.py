from flask import render_template, request, redirect, url_for
from app import app
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime, timedelta

# Initialize SQLAlchemy instance without app
db = SQLAlchemy()

# Define models
class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contracts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Recipient {self.name}>'

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
        recipients_list = Recipient.query.all()
        return render_template('recipients.html', recipients=recipients_list)

    @app.route('/recipients/add', methods=['GET', 'POST'])
    def add_recipient():
        if request.method == 'POST':
            name = request.form['name']
            contracts = int(request.form['contracts'])
            recipient = Recipient(name=name, contracts=contracts)
            db.session.add(recipient)
            db.session.commit()
            return redirect(url_for('recipients'))
        return render_template('add_recipient.html')

    @app.route('/recipients/edit/<int:id>', methods=['GET', 'POST'])
    def edit_recipient(id):
        recipient = Recipient.query.get_or_404(id)
        if request.method == 'POST':
            recipient.name = request.form['name']
            recipient.contracts = int(request.form['contracts'])
            db.session.commit()
            return redirect(url_for('recipients'))
        return render_template('edit_recipient.html', recipient=recipient)

    @app.route('/recipients/delete/<int:id>')
    def delete_recipient(id):
        recipient = Recipient.query.get_or_404(id)
        db.session.delete(recipient)
        db.session.commit()
        return redirect(url_for('recipients'))