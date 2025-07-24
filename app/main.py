from flask import Flask, jsonify, request, redirect
import string, random
from app.models import URLMapping
from urllib.parse import urlparse

app = Flask(__name__)

url_store = {}
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in url_store:
            return code

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
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400
    code = generate_short_code()
    url_store[code] = URLMapping(long_url)
    short_url = request.host_url.rstrip('/') + '/' + code
    return jsonify({"short_code": code, "short_url": short_url}), 201

@app.route('/<short_code>')
def redirect_short_url(short_code):
    mapping = url_store.get(short_code)
    if mapping is None:
        return jsonify({"error": "Short code not found"}), 404
    mapping.click_count += 1
    return redirect(mapping.original_url)

@app.route('/api/stats/<short_code>')
def analytics(short_code):
    mapping = url_store.get(short_code)
    if mapping is None:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": mapping.original_url,
        "clicks": mapping.click_count,
        "created_at": mapping.created_at.isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)