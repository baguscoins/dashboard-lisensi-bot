from flask import Flask, render_template
import json
import os

app = Flask(__name__)

LICENSE_DB_FILE = 'license_db.json'

# Pastikan file JSON tidak error saat dibaca
def load_licenses():
    try:
        if not os.path.exists(LICENSE_DB_FILE):
            return {}
        with open(LICENSE_DB_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading license file: {e}")
        return {}

@app.route('/')
def index():
    licenses = load_licenses()
    return render_template('index.html', licenses=licenses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
