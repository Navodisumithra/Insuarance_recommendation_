import mysql.connector
from mysql.connector import Error
import json


# ----------------- DB Configuration -----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'insurance _db'
}

# ----------------- Connect to MySQL -----------------
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

# ----------------- Save User Prediction/Input -----------------
def save_user_data(data):
    """
    Save user's input data into the user_inputs table
    """
    conn = get_connection()
    if not conn:
        print("Failed to connect to DB. Data not saved.")
        return

    cursor = None
    try:
        cursor = conn.cursor()

        sql = """
        INSERT INTO user_inputs 
        (CustomerID, Age, Gender, MaritalStatus, Occupation, PreferredPaymentMode, 
         MonthlyIncomeLKR, Smoker, Weight, Height, BMI, NumChildren, Benefits)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Convert Benefits list to JSON string
        benefits_json = json.dumps(data.get('Benefits', []))

        values = (
            data.get('CustomerID', 0),
            data.get('Age', 0),
            data.get('Gender', 0),
            data.get('MaritalStatus', 0),
            data.get('Occupation', ''),
            data.get('PreferredPaymentMode', ''),
            data.get('MonthlyIncomeLKR', 0.0), # Use default to prevent NULL error
            data.get('Smoker', 0),
            data.get('Weight', 0.0),
            data.get('Height', 0.0),
            data.get('BMI', 0.0),
            data.get('NumChildren', 0),
            benefits_json
        )

        cursor.execute(sql, values)
        conn.commit()
        print("User data saved to database.")
    
    except Error as e:
        print("Error saving data to MySQL:", e)
    
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

# ----------------- Fetch All Users -----------------
def fetch_all_users():
    conn = get_connection()
    if not conn:
        return []
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users")
        data = cursor.fetchall()
        return data
    except Error as e:
        print("Error fetching users:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

# ----------------- Fetch All Admins -----------------
def fetch_all_admins():
    conn = get_connection()
    if not conn:
        return []
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email FROM admin_users")
        data = cursor.fetchall()
        return data
    except Error as e:
        print("Error fetching admins:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

# ----------------- Fetch All User Predictions -----------------
def fetch_all_predictions():
    conn = get_connection()
    if not conn:
        return []
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_inputs ORDER BY id DESC")
        data = cursor.fetchall()
        return data
    except Error as e:
        print("Error fetching predictions:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()
