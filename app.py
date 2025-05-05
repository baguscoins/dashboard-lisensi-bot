
from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'botlisensi_secret_key'
RESELLER_DB = 'reseller_db.json'

def load_resellers():
    if not os.path.exists(RESELLER_DB):
        return {"resellers": []}
    with open(RESELLER_DB, 'r') as f:
        return json.load(f)

def save_resellers(data):
    with open(RESELLER_DB, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/daftar-reseller', methods=['GET', 'POST'])
def daftar_reseller():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "Password tidak cocok"

        db = load_resellers()
        for user in db['resellers']:
            if user['username'] == username or user['email'] == email:
                return "Username atau Email sudah terdaftar"

        hashed_pw = generate_password_hash(password)
        db['resellers'].append({
            "nama": nama,
            "username": username,
            "email": email,
            "password": hashed_pw,
            "tanggal_daftar": str(datetime.today().date())
        })
        save_resellers(db)
        return redirect(url_for('login_reseller'))

    return render_template('daftar_reseller.html')

@app.route('/login-reseller', methods=['GET', 'POST'])
def login_reseller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = load_resellers()
        for user in db['resellers']:
            if (user['username'] == username or user['email'] == username) and check_password_hash(user['password'], password):
                session['reseller'] = {
                    "nama": user['nama'],
                    "username": user['username'],
                    "email": user['email'],
                    "tanggal_daftar": user['tanggal_daftar']
                }
                return redirect(url_for('profil_reseller'))
        return "Login gagal, periksa kembali akun Anda."
    return render_template('login_reseller.html')

@app.route('/profil-reseller')
def profil_reseller():
    if 'reseller' not in session:
        return redirect(url_for('login_reseller'))
    return render_template('profil_reseller.html', user=session['reseller'])

@app.route('/logout-reseller')
def logout_reseller():
    session.pop('reseller', None)
    return redirect(url_for('login_reseller'))
