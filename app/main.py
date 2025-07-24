from flask import Flask, jsonify, request, redirect
from app.utils import generate_short_code, is_valid_url
from app.models import url_db
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while short_code in url_db:
        short_code = generate_short_code()

    url_db[short_code] = {
        "url": long_url,
        "created_at": datetime.utcnow().isoformat(),
        "clicks": 0
    }

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    data = url_db.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    data["clicks"] += 1
    return redirect(data["url"])

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    data = url_db.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": data["url"],
        "clicks": data["clicks"],
        "created_at": data["created_at"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
