import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


def stream_users():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, CAST(age AS UNSIGNED) AS age FROM user_data")

        for row in cursor:
            yield row
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    for user in stream_users():
        print(user)
