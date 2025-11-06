import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class ExecuteQuery():
    
    def __init__(self, query, param):
        self.connection = None
        self.query = query
        self.param = param

    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv('DB_HOST'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = "ALX_prodev"
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(self.query, self.param)
                return cursor.fetchall()
        except Error as e:
            print(e)
            return None
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()



if __name__ == '__main__':
    query = "SELECT * FROM users WHERE age > %s"
    param = (20,)
    with ExecuteQuery(query, param) as result:
        for row in result:
            print(row)