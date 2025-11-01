import mysql.connector
import uuid
import csv
import os
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables from .env file (DB credentials, etc.)
load_dotenv()

# -------------------------------------------------------------
# 1️⃣ CONNECT TO MYSQL SERVER (without selecting a database)
# -------------------------------------------------------------
def connect_db():
    """Connects to the MySQL server using environment variables."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        if connection.is_connected():
            print("MYSQL Server connection successful")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    

# -------------------------------------------------------------
# 2️⃣ CREATE DATABASE IF NOT EXISTS
# -------------------------------------------------------------
def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


# -------------------------------------------------------------
# 3️⃣ CONNECT TO THE 'ALX_prodev' DATABASE
# -------------------------------------------------------------
def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to 'ALX_prodev' database.")
            return connection
    except Error as e:
        print(f"Error connecting to 'ALX_prodev' database: {e}")
        return None
    

# -------------------------------------------------------------
# 4️⃣ CREATE TABLE IF NOT EXISTS
# -------------------------------------------------------------
def create_table(connection):
    """Creates a table named 'user_data' if it does not already exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,     
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'users' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


# -------------------------------------------------------------
# 5️⃣ INSERT DATA INTO TABLE
# -------------------------------------------------------------
def insert_data(connection, data): 
    """Inserts a single record into the 'users' table."""
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        # Execute the query using data tuple (user_id, name, email, age)
        cursor.execute(insert_query, data)
        connection.commit()
        print(f"Data inserted successfully for {data[1]}")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()


# -------------------------------------------------------------
# 6️⃣ READ DATA FROM CSV FILE
# -------------------------------------------------------------
def read_csv(file_path):
    """Reads user data from a CSV file and returns a list of tuples."""
    data = []
    try:
        with open(file_path, 'r') as file:
            file = csv.DictReader(file)
            for row in file:
                # Generate a unique UUID for each user
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                # Append as a tuple to the data list
                data.append((user_id, name, email, age))
        print(f"Loaded {len(data)} records from '{file_path}'.")
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return []


# -------------------------------------------------------------
# 7️⃣ MAIN EXECUTION LOGIC
# -------------------------------------------------------------
if __name__ == "__main__":
    # Connect to the MySQL server
    db_connection = connect_db()
    if db_connection:
        # Create the database if it doesn't exist
        create_database(db_connection)
        db_connection.close()

    # Connect to the ALX_prodev database
    prodev_connection = connect_to_prodev()
    if prodev_connection:
        # Create the users table if it doesn't exist
        create_table(prodev_connection)
        # Load user data from the CSV file
        user_data = read_csv('user_data.csv')

        # Step 6: Insert each record into the users table
        for record in user_data:
            insert_data(prodev_connection, record)
        # Close the connection
        prodev_connection.close()
