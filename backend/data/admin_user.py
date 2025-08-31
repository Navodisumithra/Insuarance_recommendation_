from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import bcrypt, jwt, datetime
from db_connector import get_connection  # use your existing connector

app = Flask(__name__)

# CORS: allow all origins during dev; refine for prod
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

app.config['SECRET_KEY'] = '12336547896655'


# --- Register Admin ---
@app.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()  # ensure preflight handled for this route
def register():
    if request.method == 'OPTIONS':
        return ('', 204)

    data = request.get_json(force=True)  # safer parsing
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    raw_password = data.get('password', '')

    if not username or not email or not raw_password:
        return jsonify({'error': 'username, email, and password are required'}), 400

    # bcrypt hash as UTF-8 STRING (not bytes) so it fits VARCHAR
    hashed_pw = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_connection()
    if not conn:
        return jsonify({'error': 'DB connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO admin_users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        return jsonify({'message': 'Admin registered successfully'}), 201
    except Exception as e:
        # e.g., duplicate email/username
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# --- Login Admin ---
@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    if request.method == 'OPTIONS':
        return ('', 204)

    data = request.get_json(force=True)
    email = data.get('email', '').strip()
    raw_password = data.get('password', '')

    if not email or not raw_password:
        return jsonify({'error': 'email and password are required'}), 400

    conn = get_connection()
    if not conn:
        return jsonify({'error': 'DB connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM admin_users WHERE email=%s", (email,))
        user = cursor.fetchone()

        # if user exists, user['password'] should be the stored bcrypt hash as str
        if user:
            stored_hash_str = user['password'] if isinstance(user['password'], str) else user['password'].decode('utf-8')
            if bcrypt.checkpw(raw_password.encode('utf-8'), stored_hash_str.encode('utf-8')):
                token = jwt.encode(
                    {'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
                    app.config['SECRET_KEY'],
                    algorithm='HS256'
                )
                return jsonify({'token': token, 'message': 'Login successful'})
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()


# --- Protected Route Example ---
@app.route('/dashboard', methods=['GET', 'OPTIONS'])
@cross_origin()
def dashboard():
    if request.method == 'OPTIONS':
        return ('', 204)

    auth = request.headers.get('Authorization')
    if not auth or ' ' not in auth:
        return jsonify({'error': 'Token missing'}), 401

    try:
        token = auth.split(" ")[1]  # "Bearer <token>"
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f"Welcome Admin ID {decoded['id']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


if __name__ == '__main__':
    # You can also set a fixed port if needed: app.run(debug=True, port=5000)
    app.run(debug=True)
