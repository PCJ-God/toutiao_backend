from typing import Any 
import json

import redis.asyncio as redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


redis_client = redis.Redis(
    host=REDIS_HOST, # redis 服务器主机地址
    port=REDIS_PORT, # redis 服务器端口号
    db=REDIS_DB,     # redis 数据库编号0——15
    decode_responses=True # 是否将字节数据解码为字符串
)


# 设置 和 读取 缓存

# 读取 ： 字符串
async def get_cache(key: str):
    # return await redis_client.get(key)
    try :
        return await redis_client.get(key)
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None


# 读取 ： 字典/列表
async def get_json_cache(key: str):
    try : 
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    except Exception as e:
        print(f"Error getting JSON cache: {e}")
        return None


# 设置缓存 key , expire(s) , value
async def set_cache(key : str , value : Any , expire : int = 3600):
    try:
        if isinstance(value , (dict , list)):
            # 转字符串，在存
            value = json.dumps(value , ensure_ascii= False) # 中文正常保存
        
        await redis_client.set(key, value, ex=expire)
        return True
        
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False
