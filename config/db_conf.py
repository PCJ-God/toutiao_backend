import os
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker , create_async_engine


# 数据库配置：支持通过环境变量覆盖（CloudBase MySQL / 本地开发）
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ilya050322")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "news_app")

# URL 编码密码中的特殊字符（如 @, !, # 等）
ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://{quote_plus(MYSQL_USER)}:{quote_plus(MYSQL_PASSWORD)}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
)

# CloudBase MySQL 内网地址会通过环境变量注入
echo_sql = os.getenv("SQL_ECHO", "false").lower() == "true"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=echo_sql, 
    pool_size=10,
    max_overflow=20
)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)




async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
