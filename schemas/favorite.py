from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from schemas.base import NewsItemBase

class FavoriteBaseResponse(BaseModel):
    is_favorite: bool = Field(... , alias = 'isFavorite')


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(... , alias = 'newsId')

class FavoriteRemoveRequest(BaseModel):
    news_id: int = Field(... , alias = 'newsId')


class FavoriteItemResponse(NewsItemBase):
    favorite_id: int = Field(alias='favoriteId')

    favorite_time: datetime = Field(alias='favoriteTime')

    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容
        from_attributes=True # 从属性名获取别名
    )

class FavoriteListResponse(BaseModel):
    favorite_list : list[FavoriteItemResponse]
    total : int 
    has_more : bool = Field(alias='hasMore')

    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容
        from_attributes=True # 从属性名获取别名
    )
