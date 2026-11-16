import os
import httpx
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # GitHub Pages'dan so'rov qabul qilish uchun

# delta-bypass serverga ulanish
BYPASS = os.environ.get("BYPASS_URL", "http://127.0.0.1:2233/delta")

@app.route("/delta")
def delta():
    link = request.args.get("url", "")
    if not link:
        return jsonify({"key": None, "error": "url parametri kerak"}), 400

    try:
        r = httpx.get(BYPASS, params={"url": link}, timeout=90)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"key": None, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
