import aiosqlite
import asyncio

DATABASE = 'example.db'  # Replace with your database file

async def async_fetch_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("All Users:")
    for user in users:
        print(user)
    
    print("\nUsers Older Than 40:")
    for older_user in older_users:
        print(older_user)

if __name__ == "__main__":
    # Create a sample database and users table for demonstration
    async def setup_database():
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
            await db.execute('INSERT INTO users (name, age) VALUES ("Alice", 30), ("Bob", 45), ("Carol", 50), ("David", 22)')
            await db.commit()

    asyncio.run(setup_database())  # Set up the database

    # Run the concurrent fetch
    asyncio.run(fetch_concurrently())