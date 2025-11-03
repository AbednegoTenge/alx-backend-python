import mysql.connector
import functools
from datetime import datetime

# --- decorator to log SQL queries ---
def log_queries(func):
    "Logs SQL queries with timestamps."
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        start_time = datetime.now()
        print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] [LOG] Executing SQL Query: {query}")
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] [LOG] Query executed successfully in {duration:.4f}s")
            return result
        except Exception as e:
            error_time = datetime.now()
            print(f"[{error_time.strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Query failed: {e}")
            raise
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = mysql.connector.connect(
        host=env('DB_HOST'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD'),
        database=env('DB')
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# --- fetch users while logging the query ---
users = fetch_all_users(query="SELECT * FROM users")
print(users)
