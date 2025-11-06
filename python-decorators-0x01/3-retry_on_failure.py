import sqlite3
import time
import functools


def with_db_connection(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    con = sqlite3.connect('users.db')
    try:
      result = func(con, *args, **kwargs)
      return result
    finally:
      con.close()
  return wrapper

def retry_on_failure(retries=3, delay=2):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(con, *args, **kwargs):
      last_exception = None
      for attempt in range(retries):
        try:
          result = func(con, *args, **kwargs)
          return result
        except Exception as e:
          last_exception = e
          print(f"You have {attempt + 1}s remaining")
          if attempt < retries - 1:
            time.sleep(delay)
    raise last_exception

            
@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(con):
  cursor = con.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

users = fetch_users_with_retry()
print(users)
    
