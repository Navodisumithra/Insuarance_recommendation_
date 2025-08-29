# Insurance Recommender - Fullstack Starter Project

**What you get**
- `backend/` : Flask server (`app.py`) and helper modules.
- `backend/models/` : (empty) place your trained artifacts here:
    - `xgboost_insurance_model.pkl`
    - `label_encoder.pkl`
    - `X_encoded_columns.pkl`
- `backend/train_models.py` : Script to retrain on `data/insurancePlan_data.csv` and save artifacts.
- `frontend/` : Simple Bootstrap-based UI (`templates/index.html`) that posts to `/predict`.
- `requirements.txt` : Python dependencies.

**How to run (local)**
1. Put your `insurancePlan_data.csv` into `data/` (project root) OR place existing artifacts in `backend/models/`.
2. Create a virtualenv and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. (Optional) Train and save artifacts:
   ```bash
   python backend/train_models.py
   ```
4. Run the Flask app:
   ```bash
   python backend/app.py
   ```
5. Open `http://127.0.0.1:5000/` to use the UI.

**Notes for your final-year submission**
- This starter packs backend + frontend for demonstration. Expand features: validation, authentication, Dockerfile, extra endpoints (batch predict), API docs, unit tests, and CI/CD for production.
- Replace or extend the frontend with React/Vue if required for your project.

--- Generated for the user by ChatGPT.
