import asyncio
import aiosqlite

DB_PATH = "ALX_prodev.db"  # path to your SQLite database


async def async_fetch_users():
    """Fetch all users from the user_data table."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM user_data") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)


async def async_fetch_older_users():
    """Fetch users older than 40."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM user_data WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)


async def fetch_concurrently():
    # Run both tasks concurrently
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
