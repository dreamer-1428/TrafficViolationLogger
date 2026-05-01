import sqlite3
import qrcode
import io
import base64
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('traffic_violations.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    search_query = request.args.get('search')
    conn = get_db_connection()
    if search_query:
        violations = conn.execute("SELECT * FROM violation WHERE vehicle LIKE ?",
                                  ('%' + search_query + '%',)).fetchall()
    else:
        violations = conn.execute('SELECT * FROM violation').fetchall()
    conn.close()
    return render_template('index.html', violations=violations)


@app.route('/add', methods=['GET', 'POST'])
def add_violation():
    if request.method == 'POST':
        vehicle = request.form['vehicle']
        vtype = request.form['vtype']
        location = request.form['location']
        fine = request.form['fine']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO violation (vehicle, vtype, location, fine, status, issued_on) VALUES (?, ?, ?, ?, 'Unpaid', DATE('now'))",
            (vehicle, vtype, location, fine))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/view_challan/<int:id>')
def view_challan(id):
    conn = get_db_connection()
    violation = conn.execute('SELECT * FROM violation WHERE id = ?', (id,)).fetchone()
    conn.close()

    # Generate QR Code dynamically
    qr_data = f"Vehicle: {violation['vehicle']} | Fine: {violation['fine']} | Status: {violation['status']}"
    qr = qrcode.make(qr_data)
    buf = io.BytesIO()
    qr.save(buf)
    qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('challan.html', violation=violation, qr_code=qr_b64)


@app.route('/pay_challan/<int:id>')
def pay_challan(id):
    conn = get_db_connection()
    conn.execute("UPDATE violation SET status = 'Paid', paid_on = DATE('now') WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_challan', id=id))


if __name__ == '__main__':
    app.run(debug=True)