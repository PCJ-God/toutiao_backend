from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsItemBase(BaseModel):
    id : int 
    title : str  
    description : Optional[str] = None
    image : Optional[str] = None
    author : Optional[str] = None
    category_id : int = Field(alias='categoryId')
    views : int
    publish_time : Optional[datetime] = Field(None , alias='publishTime')


    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容
        from_attributes=True # 从属性名获取别名
    )


class NewsDetailResponse(NewsItemBase):
    content : str

    model_config = ConfigDict(
        populate_by_name=True, # 别名与字段名兼容
        from_attributes=True # 从属性名获取别名
    )