import aiosqlite
import asyncio

async def async_fetch_users(query):
    async with aiosqlite.connect("app.db") as conn:
        async with conn.execute(query) as cursor:
            results = await cursor.fetchall()
            return results

async def async_fetch_older_users(query):
    async with aiosqlite.connect("app.db") as conn:
        async with conn.execute(query) as cursor:
            results = await cursor.fetchall()
            return results

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users("SELECT * FROM users"),
        async_fetch_older_users("SELECT * FROM users WHERE age > 40")
    )

    print("📋 All Users:")
    for row in results[0]:
        print(row)

    print("\n👴 Users older than 40:")
    for row in results[1]:
        print(row)

asyncio.run(fetch_concurrently())