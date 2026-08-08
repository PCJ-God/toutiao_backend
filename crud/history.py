from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_news_history(
        db: AsyncSession, 
        user_id: int, 
        news_id: int
):
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    if history:
        # 如果已经存在浏览记录，则更新浏览时间
        history.view_time = datetime.now()
        await db.commit()
        await db.refresh(history)
        return history
    else:
        new_history = History(user_id=user_id, news_id=news_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        return new_history


async def get_history_list(
        db : AsyncSession,
        user_id : int,
        page : int,
        page_size : int
):

    query = select(News , History.view_time.label('view_time') , History.id.label('history_id')).join(History, News.id == History.news_id).where(History.user_id == user_id).order_by(History.view_time.desc()).offset((page - 1) * page_size).limit(page_size)
    reslut = await db.execute(query)
    rows = reslut.all()

    return rows , len(rows)


async def delete_news_history(
        db : AsyncSession,
        user_id : int,
        news_id : int
):
    query = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)

    return result.rowcount > 0 # type: ignore


async def clear_history_list(
        db : AsyncSession,
        user_id : int
):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    
    return result.rowcount > 0 # type: ignore