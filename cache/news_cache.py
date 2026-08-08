# 新闻相关的缓存方法： 新闻分类的读取与写入

from typing import Any, Dict , List, Optional

from config.cache_conf import get_json_cache, set_cache


CATEGORIES_KEY = 'news:categories'
NEWS_LIST_PREFIX = 'news:list:'
NEWS_DETAIL_PREFIX = 'news:detail:'
RELATED_NEWS_PREFIX = 'news:related:'


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)
    

# 写入新闻分类缓存 data : 缓存的数据 ， 过期的时间

# 习惯的过期时间   分类、配置（7200s） ， 列表（600s） ， 详情数据（1800s） , 验证码（120s） ————数据越稳定，缓存越久

# 避免所有的key同时过期，造成缓存雪崩

async def set_cached_categories(data : List[Dict[str , Any]] , expire : int = 7200):
    return await set_cache(CATEGORIES_KEY, data , expire)


# 写入缓存的方法（新闻列表）key = news:list:分类id:页码:每页数量  data = 列表数据 expire = 过期时间
async def set_cached_news_list(category_id : Optional[int] , page : int , size : int , news_list : List[Dict[str , Any]] , expire : int = 1800):
    # 调用封装的redis的设置方法，存新闻列表到缓存

    category_part = category_id if category_id is not None else "all"

    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"

    return await set_cache(key , news_list , expire)


# 读取缓存的方法（新闻列表）
async def get_cached_news_list(category_id : Optional[int] , page : int , size : int):

    category_part = category_id if category_id is not None else "all"

    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"

    return await get_json_cache(key)


# 读取新闻详情数据
async def get_cached_news_detail(news_id : int):
    key = f'{NEWS_DETAIL_PREFIX}{news_id}'
    return await get_json_cache(key)


# 写入新闻详情数据
async def cache_news_detail(news_id : int , news_data : Dict[str , Any] , expire : int = 300):
    key = f'{NEWS_DETAIL_PREFIX}{news_id}'
    return await set_cache(key , news_data , expire)


# 读取相关新闻数据
async def get_cached_related_news(news_id : int , category_id : int):
    key = f'{RELATED_NEWS_PREFIX}{news_id}:{category_id}'
    return await get_json_cache(key)

# 写入相关新闻数据
async def cache_related_news(news_id : int ,category_id : int,  related_news : List[Dict[str , Any]] , expire : int = 1800):
    key = f'{RELATED_NEWS_PREFIX}{news_id}:{category_id}'
    return await set_cache(key , related_news , expire)