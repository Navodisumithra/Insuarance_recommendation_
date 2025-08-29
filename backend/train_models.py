import pandas as pd, joblib, xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "data", "insurancePlan_data.csv")
OUT_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    df = pd.read_csv(DATA_FILE)

    # Target
    target = 'PlanID'
    X = df.drop([target, 'PlanName'], axis=1)
    y = df[target]

    # Encode categorical features
    categorical_cols = ['Occupation', 'PreferredPaymentMode']
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    # Encode target
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y_encoded, test_size=0.2, random_state=42
    )

    # Train model
    model = xgb.XGBClassifier(
        objective='multi:softmax',
        num_class=len(le.classes_),
        eval_metric='mlogloss',
        random_state=42
    )
    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)
    print("Test accuracy:", accuracy_score(y_test, y_pred))

    # Save artifacts
    joblib.dump(model, os.path.join(OUT_DIR, "xgboost_insurance_model.pkl"))
    joblib.dump(le, os.path.join(OUT_DIR, "label_encoder.pkl"))
    joblib.dump(X_encoded.columns.tolist(), os.path.join(OUT_DIR, "X_encoded_columns.pkl"))

    print("Artifacts saved to", OUT_DIR)

if __name__ == "__main__":
    main()
