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
from flask import Flask, render_template, request, redirect, session, url_for
from db import init_db, store_user, verify_user, get_or_create_key
from utils import generate_activation_key

app = Flask(__name__)
app.secret_key = 'replace-with-secret-key'

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activation')
def activation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    key = get_or_create_key(session['user_id'])
    return render_template('activation.html', activation_key=key)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = verify_user(request.form['email'], request.form['password'])
        if uid:
            session['user_id'] = uid
            return redirect(url_for('activation'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        store_user(request.form['email'], request.form['password'])
        return redirect(url_for('login'))
    return render_template('register.html')
