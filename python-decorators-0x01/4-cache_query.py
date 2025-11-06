import sqlite3
import functools
import time

query_cache = {}

def cache_query(func):
  @functools.wraps(func)
  def wrapper(con, query, *args, **kwargs):
    if query in query_cache:
      print("Fetching from cache")
      return query_cache[query]
    result = func(con, query *args, **kwargs)
    query_cache[query] = result
    print("saved to cache")
    return result
  return wrapper
    

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

@with_db_connection
@cache_query
def fetch_users_with_cache(con, query):
  cursor = con.cursor()
  cursor.execute(query)
  return cursor.fetchall()

#Test the caching
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#Fetch from cache
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)
