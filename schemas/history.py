from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase



class HistoryAddRequest(BaseModel):
    """
    添加历史记录请求
    """
    news_id: int = Field(..., alias="newsId")


class HistoryNewsItemResponse(NewsItemBase):
    """
    历史记录新闻项响应
    """
    history_id: int = Field(..., alias="historyId")
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容
        from_attributes=True   # 允许从对象属性中获取数据
    )
    


class HistoryListResponse(BaseModel):
    """
    历史记录列表响应
    """
    history_list: list[HistoryNewsItemResponse] = Field(..., alias="list")
    total: int = Field(..., alias="total")
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容   
        from_attributes=True   # 允许从对象属性中获取数据
    )