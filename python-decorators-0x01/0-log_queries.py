import mysql.connector
import functools
import time

# --- decorator to log SQL queries ---
def log_queries(func):
    "Logs SQL queries and execution time."
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        start = time.perf_counter()
        print(f"[LOG] Executing SQL Query: {query}")
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            print(f"[LOG] Query executed successfully in {duration:.4f}s")
            return result
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
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
