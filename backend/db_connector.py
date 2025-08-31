import mysql.connector
from mysql.connector import Error
import json

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'insurance_db'
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

def save_user_data(data):
    conn = get_connection()
    if not conn:
        print("Failed to connect to DB. Data not saved.")
        return

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
            data.get('CustomerID'),
            data.get('Age'),
            data.get('Gender'),
            data.get('MaritalStatus'),
            data.get('Occupation'),
            data.get('PreferredPaymentMode'),
            data.get('MonthlyIncomeLKR'),
            data.get('Smoker'),
            data.get('Weight'),
            data.get('Height'),
            data.get('BMI'),
            data.get('NumChildren'),
            benefits_json
        )

        cursor.execute(sql, values)
        conn.commit()
        print("User data saved to database.")
    
    except Error as e:
        print("Error saving data to MySQL:", e)
    
    finally:
        cursor.close()
        conn.close()
