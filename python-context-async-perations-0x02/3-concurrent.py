import asyncio
import aiosqlite

async def async_fetch_users(db_name):
    """Fetch all users from the database."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users(db_name):
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    """Fetch all users and users older than 40 concurrently."""
    db_name = 'my_database.db'  # Change this to your actual database file
    users, older_users = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )
    return users, older_users

if __name__ == "__main__":
    # Run the concurrent fetch operation
    users, older_users = asyncio.run(fetch_concurrently())
    
    print("All users:")
    for user in users:
        print(user)

    print("\nUsers older than 40:")
    for older_user in older_users:
        print(older_user)