from flask import Flask, request, render_template, jsonify
import json
import datetime

app = Flask(__name__)

# Load license data from JSON
def load_license_data():
    try:
        with open('license_db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save license data to JSON
def save_license_data(data):
    with open('license_db.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    key = request.form.get('key')
    data = load_license_data()

    if key in data:
        license_info = data[key]
        expiration_date = datetime.datetime.strptime(license_info['expires'], "%Y-%m-%d")
        if datetime.datetime.now() < expiration_date:
            return jsonify({"status": "valid", "message": "License is active."})
        else:
            return jsonify({"status": "expired", "message": "License has expired."})
    else:
        return jsonify({"status": "invalid", "message": "License key not found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
