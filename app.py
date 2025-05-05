
from flask import Flask, render_template, request, redirect, url_for, flash
import json, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_FILE = "license_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    db = load_db()
    return render_template("index.html", db=db)

@app.route("/add", methods=["POST"])
def add():
    key = request.form["key"]
    days = int(request.form["days"])
    db = load_db()
    db[key] = {
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=days)).isoformat()
    }
    save_db(db)
    flash("Lisensi berhasil ditambahkan!", "success")
    return redirect(url_for("index"))

@app.route("/delete/<key>")
def delete(key):
    db = load_db()
    if key in db:
        db.pop(key)
        save_db(db)
        flash("Lisensi dihapus.", "info")
    return redirect(url_for("index"))

@app.route("/verify/<key>")
def verify(key):
    db = load_db()
    data = db.get(key)
    if not data:
        return {"status": "invalid"}, 404
    if datetime.fromisoformat(data["expires_at"]) < datetime.now():
        return {"status": "expired"}
    return {"status": "valid"}

if __name__ == "__main__":
    app.run(debug=True)
