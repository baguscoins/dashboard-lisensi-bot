from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load database
def load_db():
    try:
        with open("license_db.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Gagal load license_db.json:", e)
        return None

db = load_db()

@app.route("/")
def index():
    if db is None:
        return "Error loading data: 'db' is undefined"
    return jsonify(db)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
