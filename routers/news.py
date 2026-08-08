from fastapi import APIRouter, Depends, HTTPException , Query

from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db

from crud import news
from crud import news_cache
router = APIRouter(prefix="/api/news", tags=["news"])



"""
接口实现流程
1、模块化路由 -> API 接口规范文档
2、定义模型类 -> 数据库表（数据库设计文档）
3、在 crud 文件夹里面创建文件，封装操作数据库的方法
4、在路由处理函数里面调用 crud 封装好的方法，响应结果
"""



@router.get('/categories')
async def get_categories(skip : int = 0 , limit : int = 100 , db : AsyncSession = Depends(get_db)):


    categories = await news_cache.get_categories(db , skip , limit)

    return {
        "code" : 200 , 
        "message" : "获取新闻分类成功" ,
        "data" : categories
    }


@router.get('/list')
async def get_news_list(
    category_id : int = Query(..., alias="categoryId") , 
    page : int = 1 , 
    page_size : int = Query(10, alias="pageSize" , le = 100) , 
    db : AsyncSession = Depends(get_db)
):
    
    offset = (page - 1) * page_size

    news_list = await news_cache.get_news_list(db , category_id , offset , page_size) 

    total = await news.get_news_count(db , category_id)

    has_more = offset + len(news_list) < total

    # 思路： 处理分页规则 ， 查询新闻列表， 计算总量， 计算是否还有更多
    return {
        'code' : 200 ,
        'message' : '获取新闻列表成功' ,
        'data' : {
            'list' : news_list ,
            'total': total ,
            'hasMore' : has_more

        }
    }

@router.get('/detail')
async def get_news_detail(
    news_id : int = Query(..., alias="id") , 
    db : AsyncSession = Depends(get_db)
):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    new_details = await news_cache.get_news_detail(db , news_id)

    if not new_details:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    view_res = await news.increase_news_views(db , new_details.id)
    if not view_res:
        raise HTTPException(status_code=404, detail="新闻不存在")
    

    related_news = await news_cache.get_related_news(db , news_id , new_details.category_id)

    return {
        'code' : 200 ,
        'message' : 'success' ,
        'data' : {
            'id' : new_details.id , 
            'title' : new_details.title ,
            'content' : new_details.content ,
            'image' : new_details.image , 
            'author' : new_details.author ,
            'publishTime' : new_details.publish_time.isoformat(),
            'categoryId' : new_details.category_id,
            'views' : new_details.views ,
            'relatedNews' : related_news
        }
    }