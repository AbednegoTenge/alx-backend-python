import sqlite3
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


def transactional(func):
  @functools.wraps(func)
  def wrapper(con, *args, **kwargs):
    try:
      result = func(con, *args, **kwargs)
      con.commit()
      return result
    except Exception as e:
      con.rollback()
      return e
  return wrapper


@with_db_connection
@transactional
def update_user_email(con, user_id, new_email):
  cursor = con.cursor()
  cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
