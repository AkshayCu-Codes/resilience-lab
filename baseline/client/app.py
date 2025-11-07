from flask import Flask, jsonify
import requests, os

app = Flask(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://baseline-backend:5000/account/123")

@app.route("/fetch")
def fetch():
    try:
        resp = requests.get(BACKEND_URL, timeout=2)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
