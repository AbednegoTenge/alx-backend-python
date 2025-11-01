import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def paginate_users(page_size, offset):
    """
    Generator that streams rows from 'users' table in pages.
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
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")

        while True:
            page = cursor.fetchmany(page_size)
            if not page:
                break
            for row in page:
                yield row

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()


def lazypaginate(page_size):
    """
    Processes users in pages and yields only those over age 25.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
    

if __name__ == "__main__":
    for page in lazypaginate(page_size=3):
        for user in page:
            print(f"  - {user['name']} {user['email']}, age {user['age']})")
        print("-" * 40)
