import asyncio
import aiosqlite

DB_PATH = "ALX_prodev.db"  # Path to your SQLite database


async def async_fetch_users():
    """Fetch all users from the user_data table and return them."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM user_data") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 and return them."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM user_data WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    # Run both tasks concurrently
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for user in users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
