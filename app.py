from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_FILE = 'license_db.json'
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

def load_licenses():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_licenses(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cek-lisensi', methods=['GET', 'POST'])
def cek_lisensi():
    if request.method == 'POST':
        kode = request.form['kode'].strip()
        db = load_licenses()
        lisensi = db.get(kode)
        if not lisensi:
            return render_template('hasil_cek.html', status="Tidak Valid", kode=kode)

        expired_date = datetime.strptime(lisensi['expired'], "%Y-%m-%d")
        today = datetime.today()
        if expired_date < today:
            status = "Expired"
        else:
            delta = expired_date - today
            status = f"Aktif ({delta.days} hari tersisa)"

        return render_template('hasil_cek.html', status=status, kode=kode, expired=lisensi['expired'], owner=lisensi['owner'])

    return render_template('cek_lisensi.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    db = load_licenses()
    if request.method == 'POST':
        kode = request.form['kode'].strip()
        owner = request.form['owner'].strip()
        expired = request.form['expired'].strip()
        db[kode] = {"owner": owner, "expired": expired}
        save_licenses(db)
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', licenses=db)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
