from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load database saat startup
try:
    with open("license_db.json", "r") as file:
        db = json.load(file)
except Exception as e:
    db = None
    print("Failed to load license_db.json:", e)

@app.route("/")
def home():
    if db is None:
        return "Error loading data: 'db' is undefined"
    return jsonify(db)

if __name__ == "__main__":
    app.run(debug=True)
