import asyncio
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

async def connect_to_database():
    """Establish a connection to the MySQL database asynchronously."""
    return await aiomysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db="ALX_prodev"
    )


async def fetch_users():
    """Fetch all users using its own connection."""
    conn = await connect_to_database()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM user_data")
        rows = await cursor.fetchall()
        print("All Users:")
        for row in rows:
            print(row)
    conn.close()


async def fetch_older_users():
    """Fetch users older than 40 using a separate connection."""
    conn = await connect_to_database()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM user_data WHERE age > 40")
        rows = await cursor.fetchall()
        print("\nUsers older than 40:")
        for row in rows:
            print(row)
    conn.close()


async def fetch_concurrently():
    await asyncio.gather(
        fetch_users(),
        fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
