import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'traffic_violations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    fine_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default='Unpaid')

with app.app_context():
    db.create_all()
    if not Violation.query.first():
        sample = Violation(vehicle_number='TN-45-AT-1234', violation_type='No Helmet',
                           location='Namakkal', date='2026-04-22', fine_amount=500.0)
        db.session.add(sample)
        db.session.commit()

@app.route('/')
def home():
    search_query = request.args.get('search')
    if search_query:
        violations = Violation.query.filter(Violation.vehicle_number.contains(search_query)).all()
    else:
        violations = Violation.query.all()
    return render_template('history.html', violations=violations)

@app.route('/add', methods=['GET', 'POST'])
def add_violation():
    if request.method == 'POST':
        new_entry = Violation(
            vehicle_number=request.form['vehicle_number'],
            violation_type=request.form['violation_type'],
            location=request.form['location'],
            date=request.form['date'],
            fine_amount=request.form['fine_amount']
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_violation.html')

@app.route('/challan/<int:id>')
def view_challan(id):
    violation = Violation.query.get_or_404(id)
    qr_data = f"Vehicle: {violation.vehicle_number} | Status: {violation.status}"
    img = qrcode.make(qr_data)
    qr_filename = f"qr_{id}.png"
    img.save(os.path.join('static', qr_filename))
    return render_template('challan.html', violation=violation, qr_filename=qr_filename)

if __name__ == '__main__':
    app.run(debug=True)