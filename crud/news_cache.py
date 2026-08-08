from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from cache.news_cache import cache_news_detail, cache_related_news, get_cached_categories, get_cached_news_detail, get_cached_news_list, get_cached_related_news, set_cached_categories, set_cached_news_list
from models.news import Category, News
from schemas.base import NewsItemBase , NewsDetailResponse
from schemas.news import RelatedNewsResponse


async def get_categories(db : AsyncSession , skip : int = 0 , limit : int = 100):

    #  先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()

    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all() # ORM

    # 写入缓存
    if categories:
        categories =jsonable_encoder(categories) # 将对象转换为可序列化的格式
        await set_cached_categories(categories)

    # 返回数据

    return categories

async def get_news_list(db : AsyncSession , category_id : int , skip : int = 0 , limit : int = 10):

    # 先尝试从缓存获取新闻列表
    # skip = (page - 1) * size -> page = skip // size + 1
    page = skip // limit + 1
    cached_news_list = await get_cached_news_list(category_id, page, limit)
    if cached_news_list:
        return [News(**Item) for Item in cached_news_list] # 将字典转换为对象

    # 查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把ORM数据 转换成为字典才能写入缓存
        # ORM 转成Pydantic模型 -> 转成字典 -> 写入缓存 
        # by_alias=False 表示不使用别名，使用原始字段名 ， 因为Redis数据是给后端用的 
        news_data = [NewsItemBase.model_validate(item).model_dump(mode='json' , by_alias=False) for item in news_list]
        await set_cached_news_list(category_id, page, limit, news_data)

    return news_list

async def get_news_count(db : AsyncSession , category_id : int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错


async def get_news_detail(db : AsyncSession , news_id : int):

    # 先查询缓存是否有数据
    cache_detail = await get_cached_news_detail(news_id)
    if cache_detail:
        cache_detail = NewsDetailResponse.model_validate(cache_detail)
        return News(**cache_detail.model_dump())

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()

    # 写入缓存
    if news_detail:
        # 用 Pydantic 序列化，确保类型正确
        news_data = NewsDetailResponse.model_validate(news_detail).model_dump(mode='json')
        await cache_news_detail(news_id , news_data)

    return news_detail


async def increase_news_views(db : AsyncSession , news_id : int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新之后 -> 检查数据库是否真的命中了数据 -> 命中返回True
    return result.rowcount > 0 


async def get_related_news(db : AsyncSession , news_id : int , category_id : int , limit : int = 5):

    # 先查缓存
    cached_related = await get_cached_related_news(news_id, category_id)
    if cached_related:
        return cached_related

    # 查询指定分类下的所有新闻
    # order_by 排序 -> 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),  # 默认是升序，desc 表示降序
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    related_news = result.scalars().all()

    # 写入缓存
    if related_news:
        related_data = [RelatedNewsResponse.model_validate(item).model_dump(mode='json', by_alias=True) for item in related_news]
        await cache_related_news(news_id, category_id, related_data)
        return related_data

    return []

