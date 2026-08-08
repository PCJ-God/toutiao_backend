from fastapi import APIRouter, Depends, HTTPException, Query

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse, HistoryNewsItemResponse
from utils.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from utils.response import success_response

router = APIRouter(
    prefix="/api/history",
    tags=["history"]
)


@router.post('/add')
async def add_history(
    data : HistoryAddRequest,
    user : User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db)
):
    result = await history.add_news_history(db, user.id, data.news_id)
    return success_response(message='添加浏览记录成功' , data=result)



@router.get('/list')
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=10, alias='pageSize'),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows , total = await history.get_history_list(db, user.id, page, page_size)
    has_more = total > page * page_size

    history_list = [HistoryNewsItemResponse.model_validate({
            **news.__dict__,
            "view_time": view_time,
            "history_id": history_id
        }) for news, view_time, history_id in rows]

    data = HistoryListResponse(
        list=history_list,
        total=total,
        hasMore=has_more
    )


    return success_response(message='成功获取浏览记录列表' , data=data)


@router.delete('/delete/{news_id}')
async def delete_history(
    news_id : int,
    user : User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db)
):
    result = await history.delete_news_history(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览记录不存在")
    return success_response(message='删除浏览记录成功')



@router.delete('/clear')
async def clear_history(
    user : User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db)
):
    result = await history.clear_history_list(db, user.id)
    return success_response(message='清空浏览记录成功')