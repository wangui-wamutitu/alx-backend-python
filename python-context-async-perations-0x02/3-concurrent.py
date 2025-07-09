import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("app.db") as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results

async def async_fetch_older_users():
    async with aiosqlite.connect("app.db") as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            return results

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for row in results[0]:
        print(row)

    print("Users older than 40:")
    for row in results[1]:
        print(row)

asyncio.run(fetch_concurrently())