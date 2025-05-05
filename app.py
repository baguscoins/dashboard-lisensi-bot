from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('license_db.json', 'r') as file:
            data = json.load(file)
        return render_template('index.html', data=data)
    except Exception as e:
        return f"Error loading data: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
