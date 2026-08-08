from pydantic import BaseModel
from typing import Annotated, TypedDict

from langgraph.graph import add_messages


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


# LangGraph 内部状态，不用于 FastAPI 请求校验
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
    response: str
