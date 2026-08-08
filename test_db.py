import asyncio
import sys
sys.path.insert(0, '.')

from config.db_conf import engine, DATABASE_URL
print(f"DB URL: {DATABASE_URL[:60]}...")

async def test():
    from sqlalchemy import text
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT VERSION()'))
            ver = result.fetchone()
            print(f"MySQL version: {ver[0]}")
            print("DB connection OK!")
    except Exception as e:
        print(f"DB FAILED: {type(e).__name__}: {e}")

try:
    asyncio.run(asyncio.wait_for(test(), timeout=15))
except asyncio.TimeoutError:
    print("DB FAILED: Connection timeout (15s) - MySQL not running or not reachable")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
