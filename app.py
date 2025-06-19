from flask import Flask, request, jsonify, render_template
from utils import generate_activation_key
from db import init_db, store_key, check_key, mark_key_used

app = Flask(__name__, static_folder='static', static_url_path='')

init_db()

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    key = generate_activation_key()
    store_key(email, key)
    return jsonify({'activation_key': key})

@app.route('/api/verify_key', methods=['POST'])
def verify():
    data = request.json
    key = data.get('key')
    result = check_key(key)
    if not result:
        return jsonify({'status': 'invalid'}), 404
    elif result[0] == 1:
        return jsonify({'status': 'already_used'}), 403
    else:
        mark_key_used(key)
        return jsonify({'status': 'valid'}), 200

if __name__ == '__main__':
    app.run(debug=True)
