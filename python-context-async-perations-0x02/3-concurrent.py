import asyncio
import aiosqlite

# Database initialization (this would typically be done separately)
DATABASE = "users.db"

async def setup_database():
    """Set up the database with a sample users table."""
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        await db.execute("DELETE FROM users")  # Clear existing data
        users = [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 25),
            ("Diana", 50)
        ]
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        await db.commit()

async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    """Run both fetch operations concurrently."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", results[0])
    print("Users Older Than 40:", results[1])

if __name__ == "__main__":
    asyncio.run(setup_database())  # Set up the database
    asyncio.run(fetch_concurrently())  # Run concurrent fetch
