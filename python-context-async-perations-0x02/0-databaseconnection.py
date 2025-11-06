import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConnection:
    def __init__(self, db):
        self.db = db
        self.connection = None

    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv('DB_HOST'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = self.db
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f'Error: {e}')
            return None
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()


with DatabaseConnection('ALX_prodev') as conn:
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)