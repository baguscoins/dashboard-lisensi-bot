from flask import Flask, render_template
import json, os

app = Flask(__name__)

def load_db():
    try:
        with open("license_db.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Gagal membaca database:", e)
        return {"licenses": []}

@app.route("/")
def index():
    db = load_db()
    return render_template("index.html", licenses=db["licenses"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
