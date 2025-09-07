# Insurance Recommender System

## Overview
The **Insurance Recommender System** is a web-based application designed to recommend personalized insurance plans using a machine learning model, facilitate user registration, process insurance claims, and provide admin management capabilities. Built with a **Flask** backend, **MySQL** database, and **XGBoost** for predictions, it features a user-friendly frontend for seamless interaction. Key functionalities include:

- **User and Admin Authentication**: Secure login/registration with JWT and bcrypt.
- **Insurance Plan Prediction**: Recommends plans based on user inputs using a trained XGBoost model.
- **Claim Submission**: Validates and processes insurance claims against registered plans.
- **Admin Dashboard**: Manages users, admins, and prediction data.
- **File Uploads**: Supports digital signature uploads for insurance registration.

This project is ideal for insurance providers seeking an automated, data-driven solution for plan recommendations and claim management.

## Project Structure
```
INSURANCE_RECOMMENDER_SYSTEM/
├── backend/
│   ├── data/
│   │   ├── insurancePlan_data.csv        # Training data for ML model
│   │   ├── policy_details.json           # Policy details for plans
│   ├── models/
│   │   ├── xgboost_insurance_model.pkl   # Trained XGBoost model
│   │   ├── label_encoder.pkl             # Label encoder for PlanID
│   │   ├── encoded_columns.pkl           # Encoded feature columns
│   ├── uploads/                          # Directory for signature uploads
│   ├── app.py                            # Main Flask application
│   ├── db_connector.py                   # Database connection and queries
│   ├── predict_utils.py                  # ML prediction utilities
│   ├── train_models.py                   # Model training script
│   ├── requirements.txt                  # Python dependencies
├── frontend/
│   ├── templates/
│   │   ├── admin_dashboard.html          # Admin management interface
│   │   ├── claim.html                    # Insurance claim form
│   │   ├── index.html                    # Login/registration page
│   │   ├── register.html                 # Insurance registration form
│   │   ├── user_dashboard.html           # User prediction interface
├── tests/
│   ├── test_model_artifact_failure.py     # Test suite for TC-AI-004
├── .gitignore                            # Git ignore file
├── README.md                             # This file
```

## Prerequisites
- **Python**: Version 3.8 or higher
- **MySQL**: Version 8.0 or higher
- **Dependencies**: Listed in `backend/requirements.txt`
- **Optional (for Testing)**: pytest, pytest-mock

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd INSURANCE_RECOMMENDER_SYSTEM
   ```

2. **Set Up Python Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
   For testing, install additional packages:
   ```bash
   pip install pytest pytest-mock
   ```

4. **Set Up MySQL Database**:
   - Install MySQL and start the server.
   - Create the database:
     ```sql
     CREATE DATABASE insurance_db;
     ```
   - Create tables (`users`, `admin_users`, `user_inputs`, `insurance_register`, `insurance_plans`, `insurance_claims`) using the schema provided in the codebase or a setup script (e.g., `schema.sql` if available).
   - Update `db_connector.py` with your MySQL credentials (default: `host=localhost`, `user=root`, `password=1234`, `database=insurance_db`).

5. **Train the ML Model**:
   - Ensure `backend/data/insurancePlan_data.csv` exists.
   - Run:
     ```bash
     python backend/train_models.py
     ```
   - This generates `xgboost_insurance_model.pkl`, `label_encoder.pkl`, and `encoded_columns.pkl` in `backend/models/`.

6. **Configure Uploads**:
   - Ensure `backend/uploads/` exists and is writable for signature file uploads.

## Configuration
- **Environment Variables** (Recommended):
  - Create a `.env` file in `backend/`:
    ```
    SECRET_KEY=your-secret-key
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=1234
    MYSQL_DB=insurance_db
    ```
  - Update `app.py` and `db_connector.py` to use `os.environ`:
    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    ```
- **CORS**: The app uses `CORS(app, resources={r"/*": {"origins": "*"}})`. For production, restrict origins (e.g., `origins="http://localhost:3000"`).
- **Upload Limits**: Signature uploads are limited to 2MB (PNG/SVG). Adjust in `app.py` if needed.

## Running the Application
1. **Start the Flask Server**:
   ```bash
   cd backend
   python app.py
   ```
   The app runs on `http://localhost:5000` in debug mode.

2. **Access the Frontend**:
   - Open `http://localhost:5000` in a browser to access `index.html` (login/registration page).
   - After login, users are redirected to `user_dashboard.html` (predictions/claims) or `admin_dashboard.html` (management).

3. **API Endpoints**:
   - **Authentication**:
     - `POST /register`: Admin registration (`{"username": "admin", "email": "admin@test.com", "password": "pass123"}`).
     - `POST /user_register`: User registration (`{"name": "User", "email": "user@test.com", "password": "pass123"}`).
     - `POST /login`: Login for users/admins, returns JWT (`{"email": "user@test.com", "password": "pass123"}`).
   - **Prediction**:
     - `POST /predict` (JWT-protected): Submits user data for plan prediction.
   - **Claims**:
     - `POST /insurance_claim`: Submits claims (`NIC`, `InsurancePlan`, `IncidentDate`, `ClaimAmount`, `Description`).
   - **Admin**:
     - `GET /get_users` (JWT-protected): Fetches all users.
     - `GET /get_admins` (JWT-protected): Fetches all admins.
   - Use Postman or curl to test APIs.

## Usage
1. **User Flow**:
   - Register or log in via `index.html`.
   - On `user_dashboard.html`, input details (e.g., Age, Occupation, Benefits) to get a predicted insurance plan.
   - Submit claims via `claim.html` or register for insurance via `register.html`.

2. **Admin Flow**:
   - Log in as an admin to access `admin_dashboard.html`.
   - View/manage users, admins, and predictions (note: CRUD endpoints like `/update_user/<id>` are referenced but not fully implemented).

3. **Prediction**:
   - The system uses an XGBoost model trained on `insurancePlan_data.csv` to predict plans.
   - Inputs are saved to `user_inputs` table for auditing.

4. **Claims**:
   - Claims are validated against registered plans and coverage limits in `insurance_plans`.
   - Status (`Approved`, `Rejected`, `Under Review`) is set based on claim amount vs. coverage.

## Testing
The project includes a test suite to validate backend functionality, located in `tests/`. Example test case:

- **TC-AI-004: Model Artifact Loading Failure**
  - **Objective**: Verify `/predict` returns HTTP 500 with `{"error": "ML model not loaded"}` when model artifacts are missing.
  - **Implementation**: See `tests/test_model_artifact_failure.py` (uses `pytest` and `pytest-mock`).
  - **Run**:
    ```bash
    pytest tests/test_model_artifact_failure.py -v
    ```
  - **Expected Output**:
    ```
    ============================= test session starts =============================
    tests/test_model_artifact_failure.py::test_model_artifact_loading_failure PASSED [100%]
    ============================= 1 passed in 0.12s =============================
    ```
  - **Screenshots**:
    - **Terminal**: Capture pytest output with Snipping Tool (Windows), Command+Shift+4 (macOS), or Flameshot (Linux).
    - **Postman**: Test `/predict` with a missing model (set `model = None` in `app.py`) and screenshot the 500 response.
    - **IDE**: Use VS Code’s “CodeSnap” extension to screenshot `test_model_artifact_failure.py`.

To expand testing:
- Add more test cases for other endpoints (e.g., `/login`, `/insurance_claim`).
- Use Selenium for UI tests (e.g., form validation in `register.html`).
- Install dependencies:
  ```bash
  pip install pytest pytest-mock selenium
  ```

## Troubleshooting
- **Database Connection Errors**:
  - Ensure MySQL is running and credentials match `db_connector.py`.
  - Use a test database for isolation (`test_insurance_db`).
- **Model Loading Issues**:
  - Run `train_models.py` to generate `models/` files.
  - Check file paths in `app.py` and `predict_utils.py`.
- **JWT Errors**:
  - Verify `SECRET_KEY` consistency across app and tests.
  - Ensure tokens are not expired (12-hour validity).
- **File Uploads**:
  - Confirm `uploads/` directory exists and is writable.
  - Check file size/type restrictions in `/insurance_register`.
- **Test Failures**:
  - Verify test database setup and ML artifacts.
  - Check Flask logs for errors (`python app.py` in debug mode).

## Security Considerations
- **Hardcoded Secrets**: Replace `SECRET_KEY` and DB credentials with environment variables (use `python-dotenv`).
- **CORS**: Restrict origins in production.
- **SQL Injection**: Current queries use placeholders, but add input sanitization (e.g., via `bleach`).
- **Rate Limiting**: Add `flask-limiter` to prevent brute-force attacks on `/login`.

## Future Enhancements
- Implement missing CRUD endpoints (`/update_user/<id>`, `/delete_user/<id>`, etc.).
- Add async support (e.g., `asyncio` for `/predict`) for scalability.
- Integrate a CI/CD pipeline (e.g., GitHub Actions) for automated testing.
- Use SQLAlchemy for ORM and migrations.
- Add logging (`logging` module) for better debugging.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the MIT License.