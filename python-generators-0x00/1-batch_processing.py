import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from 'users' table in batches.
    Each row is yielded one by one to save memory.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, CAST(age AS UNSIGNED) AS age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            for row in batch:
                yield row

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and yields only those over age 25.
    """
    for user in stream_users_in_batches(batch_size):
        if user["age"] > 25:
            yield user


# Run when script is executed directly
if __name__ == "__main__":
    print("Users over 25:\n")
    for user in batch_processing(batch_size=10):
        print(user)
