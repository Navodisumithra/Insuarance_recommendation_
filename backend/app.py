from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import joblib, os, pandas as pd, json, datetime
import bcrypt, jwt

from db_connector import save_user_data, get_connection

# Flask setup
BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "../frontend/templates"))
CORS(app)  # allow CORS globally

# Config
app.config['SECRET_KEY'] = '12336547896655'

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "models")
DATA_FILE = os.path.join(BASE_DIR, "data/insurancePlan_data.csv")
POLICY_FILE = os.path.join(BASE_DIR, "data/policy_details.json")

# Globals
model, le, X_columns, plan_lookup, policy_data = None, None, None, None, None


# ----------------- Load ML artifacts -----------------
def load_artifacts():
    global model, le, X_columns, plan_lookup, policy_data
    model = joblib.load(os.path.join(MODEL_PATH, "xgboost_insurance_model.pkl"))
    le = joblib.load(os.path.join(MODEL_PATH, "label_encoder.pkl"))
    X_columns = joblib.load(os.path.join(MODEL_PATH, "X_encoded_columns.pkl"))

    # PlanID → PlanName
    df = pd.read_csv(DATA_FILE)
    plan_lookup = df[['PlanID', 'PlanName']].drop_duplicates().set_index('PlanID')['PlanName'].to_dict()

    # Load policy details JSON
    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        policy_data = json.load(f)


# ----------------- Frontend -----------------
@app.route('/')
def index():
    return render_template('index.html')


# ----------------- Prediction -----------------
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        data = request.json
        print("Request Payload:", data)

        # Save user input to MySQL
        save_user_data(data)

        # Prepare data
        df = pd.DataFrame([data])
        categorical_cols = ['Occupation', 'PreferredPaymentMode']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        df_encoded = df_encoded.reindex(columns=X_columns, fill_value=0)

        # Predict
        pred_encoded = model.predict(df_encoded)[0]
        plan_id = le.inverse_transform([pred_encoded])[0]
        plan_name = plan_lookup.get(plan_id, "Unknown Plan")
        policy = policy_data.get(str(plan_id), {})

        response = {
            "PredictedPlanID": int(plan_id),
            "PredictedPlanName": plan_name,
            "PolicyDetails": policy
        }

        print("Response:", response)
        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400


# ----------------- Admin Auth -----------------
# Register
@app.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    if request.method == 'OPTIONS':
        return ('', 204)

    data = request.get_json(force=True)
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    raw_password = data.get('password', '')

    if not username or not email or not raw_password:
        return jsonify({'error': 'username, email, and password are required'}), 400

    # hash password (store as string)
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
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# Login
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

        if user:
            stored_hash = user['password'] if isinstance(user['password'], str) else user['password'].decode('utf-8')
            if bcrypt.checkpw(raw_password.encode('utf-8'), stored_hash.encode('utf-8')):
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


# Protected Route
@app.route('/dashboard', methods=['GET', 'OPTIONS'])
@cross_origin()
def dashboard():
    if request.method == 'OPTIONS':
        return ('', 204)

    auth = request.headers.get('Authorization')
    if not auth or ' ' not in auth:
        return jsonify({'error': 'Token missing'}), 401

    try:
        token = auth.split(" ")[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f"Welcome Admin ID {decoded['id']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


# ----------------- Run -----------------
if __name__ == "__main__":
    load_artifacts()
    app.run(host="0.0.0.0", port=5000, debug=True)
