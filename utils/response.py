from typing import Any

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message : str = 'success' , data : Any = None ):
    content={
        'code': 200, 
        'message': message, 
        'data': data
        }
    # 目标：把任何的 FastApi Pydantic , ORM 对象都要正常响应
    return JSONResponse(content=jsonable_encoder(content))
