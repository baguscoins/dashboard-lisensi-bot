from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

def load_db():
    try:
        with open("license_db.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading license_db.json:", e)
        return None

@app.route("/")
def index():
    db = load_db()
    if db is None:
        return "Error loading data: 'db' is undefined"
    return jsonify(db)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
