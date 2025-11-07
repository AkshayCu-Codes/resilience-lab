from flask import Flask, jsonify
import random, time

app = Flask(__name__)

@app.route("/account/<int:id>")
def account_info(id):
    if random.random() < 0.1:
        return {"error": "Temporary backend failure"}, 500
    if random.random() < 0.1:
        time.sleep(3)
    
    return {"account_id": id, "balance": 1000 + id, "status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
