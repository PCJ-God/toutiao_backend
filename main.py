from fastapi import FastAPI
from routers import history, news , users , favorite , ai

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


# 异常处理
from utils.exception_handle import register_exception_handlers

register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 允许所有来源的请求
    allow_credentials=True, # 允许携带认证信息cookie
    allow_methods=["*"],# 允许所有请求方法get, post, put, delete等
    allow_headers=["*"],# 允许所有请求头
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Toutiao API"}


app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
app.include_router(ai.router)