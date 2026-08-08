from typing import Optional

from pydantic import BaseModel, ConfigDict, Field



class UserRequest(BaseModel):
    username : str
    password : str



# user_info 数据类型
class UserInfoBase(BaseModel):
    '''
    用户信息基础数据模型
    '''
    nickname : Optional[str] = Field(None , max_length = 50  , description = '用户昵称')
    avatar : Optional[str] = Field(None , max_length = 255 , description = '用户头像URL')
    gender : Optional[str] = Field(None , max_length = 10 , description = '性别')
    bio : Optional[str] = Field(None , max_length = 500 , description = '用户个人简介')


class UserInfoResponse(UserInfoBase):
    '''
    用户信息响应数据模型
    '''
    id : int  
    username : str  

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True # 允许从 ORM 对象属性中取值
    )


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(... , alias='userInfo')

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias/字段名兼容
        from_attributes=True # 允许从 ORM 对象属性中取值
    )


# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname : Optional[str] = None 
    avatar : Optional[str] = None 
    gender : Optional[str] = None 
    bio : Optional[str] = None
    phone : Optional[str] = None 

class UserChangePasswordRequest(BaseModel):
    old_password : str = Field(... , description = '旧密码' , alias='oldPassword') 
    new_password : str = Field(... , description = '新密码' , alias='newPassword' , min_length=6 , max_length=20)