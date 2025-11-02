import mysql.connector

# Generator that streams user ages one by one
def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="yourdatabase"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    # Yield each age one by one without loading all into memory
    for (age,) in cursor:
        yield age

    cursor.close()
    conn.close()


# Function to calculate the average using at most two loops
def calculate_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
