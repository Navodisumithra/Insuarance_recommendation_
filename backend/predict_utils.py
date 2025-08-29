import joblib, pandas as pd, os

def load_model_artifacts(model_dir='backend/models'):
    artifacts = {}
    artifacts['model'] = joblib.load(os.path.join(model_dir, 'xgboost_insurance_model.pkl'))
    artifacts['le'] = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
    artifacts['columns'] = joblib.load(os.path.join(model_dir, 'X_encoded_columns.pkl'))
    return artifacts

def predict_single(input_dict, artifacts):
    df = pd.DataFrame([input_dict])
    categorical_cols = ['Occupation', 'PreferredPaymentMode']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    for col in artifacts['columns']:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[artifacts['columns']]
    pred = artifacts['model'].predict(df_encoded)[0]
    plan = artifacts['le'].inverse_transform([pred])[0]
    return int(plan)

if __name__ == '__main__':
    print('This module provides helper functions to load model artifacts and predict a single user.')    
