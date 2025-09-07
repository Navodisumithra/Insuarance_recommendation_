from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import joblib, os, pandas as pd, json, datetime, re
import bcrypt, jwt
from functools import wraps
from werkzeug.utils import secure_filename

from db_connector import save_user_data, get_connection

# ----------------- Flask setup -----------------
BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "../frontend/templates"))

# Broad CORS support
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config['SECRET_KEY'] = '12336547896655'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, "uploads")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------- Paths -----------------
MODEL_PATH = os.path.join(BASE_DIR, "models")
DATA_FILE = os.path.join(BASE_DIR, "data/insurancePlan_data.csv")
POLICY_FILE = os.path.join(BASE_DIR, "data/policy_details.json")

# ----------------- Globals -----------------
model, le, X_columns, plan_lookup, policy_data = None, None, None, None, None

# ----------------- Load ML artifacts -----------------
def load_artifacts():
    global model, le, X_columns, plan_lookup, policy_data
    try:
        if model is None:
            model = joblib.load(os.path.join(MODEL_PATH, "xgboost_insurance_model.pkl"))
        if le is None:
            le = joblib.load(os.path.join(MODEL_PATH, "label_encoder.pkl"))
        if X_columns is None:
            X_columns = joblib.load(os.path.join(MODEL_PATH, "X_encoded_columns.pkl"))

        if plan_lookup is None:
            df = pd.read_csv(DATA_FILE)
            plan_lookup = df[['PlanID', 'PlanName']].drop_duplicates().set_index('PlanID')['PlanName'].to_dict()

        if policy_data is None:
            with open(POLICY_FILE, "r", encoding="utf-8") as f:
                policy_data = json.load(f)

        print("ML artifacts loaded successfully.")
    except Exception as e:
        print(f"Error loading ML artifacts: {e}")

# Load artifacts at startup
load_artifacts()

# ----------------- Token Auth -----------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or ' ' not in auth:
            return jsonify({'error': 'Token missing'}), 401
        token = auth.split(" ")[1]
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(decoded, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    return decorator

# ----------------- Prediction -----------------
@app.route('/predict', methods=['POST', 'OPTIONS'])
@cross_origin()
@token_required
def predict(decoded):
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.json or {}

        # Load artifacts if not already loaded
        load_artifacts()

        if model is None:
            return jsonify({"error": "ML model not loaded"}), 500

        # Save user input
        save_user_data(data)

        # Prepare input for model
        df = pd.DataFrame([data])
        categorical_cols = ['Occupation', 'PreferredPaymentMode']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        df_encoded = df_encoded.reindex(columns=X_columns, fill_value=0)

        # Predict and map plan
        pred_encoded = model.predict(df_encoded)[0]
        plan_id = le.inverse_transform([pred_encoded])[0]
        plan_name = plan_lookup.get(plan_id, "Unknown Plan")
        policy = policy_data.get(str(plan_id), {})

        return jsonify({
            "PredictedPlanID": int(plan_id),
            "PredictedPlanName": plan_name,
            "PolicyDetails": policy
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ----------------- Insurance Claim -----------------
@app.route('/insurance_claim', methods=['POST', 'OPTIONS'])
@cross_origin()
def insurance_claim():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        form = request.form.to_dict()
        required_fields = ['NIC', 'InsurancePlan', 'IncidentDate', 'ClaimAmount', 'Description']
        for field in required_fields:
            if not form.get(field, '').strip():
                return jsonify({"error": f"{field} is required"}), 400

        nic = form['NIC'].strip()
        if not re.match(r'^([0-9]{9}[xXvV]|[0-9]{12})$', nic):
            return jsonify({"error": "Invalid NIC format."}), 400

        try:
            claim_amount = float(form['ClaimAmount'].strip())
            if claim_amount <= 0:
                return jsonify({"error": "Claim Amount must be positive."}), 400
        except ValueError:
            return jsonify({"error": "Claim Amount must be a number."}), 400

        try:
            incident_date = datetime.datetime.strptime(form['IncidentDate'].strip(), '%Y-%m-%d')
            if incident_date.date() > datetime.datetime.now().date():
                return jsonify({"error": "Incident date cannot be in the future."}), 400
        except ValueError:
            return jsonify({"error": "Invalid Incident Date format."}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed."}), 500
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM insurance_register WHERE LOWER(TRIM(nic))=%s AND LOWER(TRIM(insurance_plan))=%s",
            (nic.lower(), form['InsurancePlan'].strip().lower())
        )
        registered_user = cursor.fetchone()
        if not registered_user:
            return jsonify({"error": "No registered insurance found for this NIC and plan."}), 400

        cursor.execute(
            "SELECT CoverageAmount FROM insurance_plans WHERE LOWER(TRIM(PlanName))=%s",
            (form['InsurancePlan'].strip().lower(),)
        )
        plan_info = cursor.fetchone()
        if not plan_info:
            return jsonify({"error": "Insurance plan not found."}), 400

        plan_limit = plan_info['CoverageAmount']

        claim_status, payout_status, reason = "Under Review", None, None
        if plan_limit is None:
            reason = "Plan coverage not specified"
        else:
            if claim_amount <= plan_limit:
                claim_status, payout_status = "Approved", "Paid"
            else:
                claim_status, reason = "Rejected", f"Claim exceeds plan coverage ({plan_limit})"

        cursor.execute("""
            INSERT INTO insurance_claims
            (nic, insurance_plan, incident_date, claim_amount, description, claim_status, payout_status, reason, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            nic, form['InsurancePlan'].strip(), incident_date.strftime('%Y-%m-%d'),
            claim_amount, form['Description'].strip(), claim_status, payout_status, reason
        ))
        conn.commit()

        return jsonify({
            "message": "Claim submitted successfully",
            "claim_status": claim_status,
            "payout_status": payout_status,
            "reason": reason
        }), 201
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- Admin Registration -----------------
@app.route('/admin_register', methods=['POST', 'OPTIONS'])
@cross_origin()
def admin_register():
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.get_json(force=True)
        username, email, raw_password = data.get('username'), data.get('email'), data.get('password')
        hashed_pw = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_pw))
        conn.commit()
        return jsonify({'message': 'Admin registered successfully'}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({'error': 'Email already registered'}), 400
        return jsonify({'error': str(e)}), 400
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- User Registration -----------------
@app.route('/user_register', methods=['POST', 'OPTIONS'])
@cross_origin()
def user_register():
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.get_json(force=True)
        name, email, raw_password = data.get('name'), data.get('email'), data.get('password')
        hashed_pw = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_pw))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({'error': 'Email already registered'}), 400
        return jsonify({'error': str(e)}), 400
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- Login -----------------
@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.get_json(force=True)
        email, raw_password = data.get('email'), data.get('password')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check admin
        cursor.execute("SELECT * FROM admin_users WHERE email=%s", (email,))
        user = cursor.fetchone()
        role = 'admin' if user else None

        # Check normal user
        if not user:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            role = 'user' if user else None

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        stored_hash = user['password'] if isinstance(user['password'], str) else user['password'].decode('utf-8')
        if not bcrypt.checkpw(raw_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = jwt.encode(
            {'id': user['id'], 'role': role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

        return jsonify({'token': token, 'role': role, 'message': 'Login successful'})
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- Admin: Get Users -----------------
@app.route('/get_users', methods=['GET', 'OPTIONS'])
@cross_origin()
@token_required
def get_users(decoded):
    if decoded['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users ORDER BY id DESC")
        return jsonify(cursor.fetchall())
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- Admin: Get Admins -----------------
@app.route('/get_admins', methods=['GET', 'OPTIONS'])
@cross_origin()
@token_required
def get_admins(decoded):
    if decoded['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email FROM admin_users ORDER BY id DESC")
        return jsonify(cursor.fetchall())
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

# ----------------- Run -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
