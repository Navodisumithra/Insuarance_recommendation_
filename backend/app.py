from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib, os, pandas as pd, json

# Flask setup
BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "../frontend/templates"))
CORS(app)

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "models")
DATA_FILE = os.path.join(BASE_DIR, "data/insurancePlan_data.csv")
POLICY_FILE = os.path.join(BASE_DIR, "data/policy_details.json")

# Globals
model, le, X_columns, plan_lookup, policy_data = None, None, None, None, None

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])
        categorical_cols = ['Occupation', 'PreferredPaymentMode']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        df_encoded = df_encoded.reindex(columns=X_columns, fill_value=0)

        # Predict
        pred_encoded = model.predict(df_encoded)[0]
        plan_id = le.inverse_transform([pred_encoded])[0]
        plan_name = plan_lookup.get(plan_id, "Unknown Plan")

        # Policy details
        policy = policy_data.get(str(plan_id), {})
        
        return jsonify({
            "PredictedPlanID": int(plan_id),
            "PredictedPlanName": plan_name,
            "PolicyDetails": policy
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    load_artifacts()
    app.run(host="0.0.0.0", port=5000, debug=True)
