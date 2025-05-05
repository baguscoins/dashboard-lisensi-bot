
from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'botlisensi_secret_key'
LICENSE_DB = 'license_db.json'
RESELLER_DB = 'reseller_db.json'
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

# === LICENSE FUNCTIONS ===
def load_licenses():
    if not os.path.exists(LICENSE_DB):
        return {}
    with open(LICENSE_DB, 'r') as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_DB, 'w') as f:
        json.dump(data, f, indent=2)

# === RESELLER FUNCTIONS ===
def load_resellers():
    if not os.path.exists(RESELLER_DB):
        return {"resellers": []}
    with open(RESELLER_DB, 'r') as f:
        return json.load(f)

def save_resellers(data):
    with open(RESELLER_DB, 'w') as f:
        json.dump(data, f, indent=2)

# === MAIN HOMEPAGE ===
@app.route('/')
def index():
    return render_template('index.html')

# === LICENSE SYSTEM ===
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

# === RESELLER SYSTEM ===
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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = load_resellers()
        for user in db['resellers']:
            if user['username'] == username or user['email'] == username:
                if check_password_hash(user['password'], password):
                    session['reseller'] = {
                        "nama": user['nama'],
                        "username": user['username'],
                        "email": user['email'],
                        "tanggal_daftar": user['tanggal_daftar']
                    }
                    return redirect(url_for('profil_reseller'))
                else:
                    error = "Password salah."
                    break
        else:
            error = "Akun tidak ditemukan."
    return render_template('login_reseller.html', error=error)

@app.route('/profil-reseller', methods=['GET', 'POST'])
def profil_reseller():
    if 'reseller' not in session:
        return redirect(url_for('login_reseller'))
    db = load_resellers()
    user = session['reseller']
    success, error = None, None
    if request.method == 'POST':
        action = request.form.get('action')
        for r in db['resellers']:
            if r['username'] == user['username']:
                if action == "update":
                    r['nama'] = request.form['nama']
                    r['username'] = request.form['username']
                    r['email'] = request.form['email']
                    success = "Profil berhasil diperbarui."
                    session['reseller'] = r
                elif action == "reset_password":
                    new_pw = request.form['new_password']
                    confirm_pw = request.form['confirm_password']
                    if new_pw == confirm_pw:
                        r['password'] = generate_password_hash(new_pw)
                        success = "Password berhasil diubah."
                    else:
                        error = "Password tidak cocok."
                break
        save_resellers(db)
    return render_template('profil_reseller.html', user=session['reseller'], success=success, error=error)

@app.route('/logout-reseller')
def logout_reseller():
    session.pop('reseller', None)
    return redirect(url_for('login_reseller'))

# === RUN ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
