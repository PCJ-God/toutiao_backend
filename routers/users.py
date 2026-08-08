from re import U

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from crud.users import create_token, create_user, get_user_by_username
from models.users import User
from schemas.users import UserAuthResponse, UserChangePasswordRequest, UserInfoResponse, UserRequest , UserUpdateRequest
from starlette import status

from utils.auth import get_current_user
from utils.response import success_response


router = APIRouter(prefix="/api/user", tags=["users"])


@router.post('/register')
async def register(user_data : UserRequest, db : AsyncSession = Depends(get_db) ):

    '''
    注册逻辑:验证用户输入,检查用户名是否已存在,创建新用户并返回 token,响应结果
    
    '''

    # 获取用户
    existing_user = await get_user_by_username(db, user_data.username)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户名已存在')

    # 创建新用户
    user = await create_user(db, user_data)

    token = await create_token(db, user.id)

    
    # return {
    #     'code' : 200 , 
    #     'message' : '注册成功' ,
    #     'data' : { 
    #         'token' : token , 
    #         'userInfo':{
    #             'id' : user.id , 
    #             'username' : user.username , 
    #             'bio' : user.bio ,
    #             'avatar' : user.avatar

    #         }
    #     }   
    # }

    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user)  # type: ignore
    ) # pyright: ignore[reportCallIssue]
    return success_response(message='注册成功', data=response_data)


@router.post('/login')
async def login(user_data : UserRequest, db : AsyncSession = Depends(get_db) ):


    # 登录逻辑：验证用户是否存在 ， 验证密码  ， 生成token ， 响应结果

    user = await users.authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')
    
    token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user)  # type: ignore
    ) # pyright: ignore[reportCallIssue]
    return success_response(message='登录成功', data=response_data)


# 查token查用户 ， 封装crud ， 功能整合成一个工具函数 ， 路由导入使用 :依赖注入
@router.get('/info')
async def get_user_info(user : User = Depends(get_current_user)):
    return success_response(message='获取用户信息成功' , data = UserInfoResponse.model_validate(user))


# 修改用户信息 ： 验证用户token ， 更新（用户输入数据 put 提交， 请求体参数 ， 定义pydantic模型类） ， 响应结果
@router.put('/update')

# 参数 ： 用户输入的 ， 验证token的 ， db（调用CRUD里面的更新方法）
async def update_user_info(
    user_data : UserUpdateRequest, 
    user : User = Depends(get_current_user), 
    db : AsyncSession = Depends(get_db)
):
    updated_user = await users.update_user(db, user.username, user_data)
    return success_response(message='更新用户信息成功' , data = UserInfoResponse.model_validate(updated_user))


@router.put('/password')
async def update_password(
    password_data : UserChangePasswordRequest, 
    user : User = Depends(get_current_user), 
    db : AsyncSession = Depends(get_db)
):

    success = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='修改密码失败，请稍后再试')
    
    return success_response(message='更新密码成功')