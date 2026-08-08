import sys, time
sys.path.insert(0, '.')

print("1. Starting...", flush=True)
from config.db_conf import DATABASE_URL
print(f"2. DB URL: {DATABASE_URL[:50]}...", flush=True)

# Test sync connection
import sqlalchemy
print("3. Creating engine...", flush=True)
engine = sqlalchemy.create_engine(DATABASE_URL.replace("+aiomysql", "+pymysql"), connect_args={"connect_timeout": 5})

print("4. Connecting...", flush=True)
try:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT VERSION()"))
        print(f"5. MySQL: {result.fetchone()[0]}", flush=True)
    print("OK!", flush=True)
except Exception as e:
    print(f"5. FAIL: {e}", flush=True)
print("6. Done", flush=True)
