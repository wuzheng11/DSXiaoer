from pydantic import BaseModel


class ChatObject(BaseModel):
    """对象消息"""
    type: str #必填项
    id: str
    title: str |None =None
    attributes: dict={}

class ChatRequest(BaseModel):
    """聊天请求对象"""
    sender_id: str
    text: str | None = None
    object: ChatObject |None = None
    message_id: str | None = None

class ChatMessage(BaseModel):
    """"聊天消息响应对象"""
    text: str | None = None # 聊天消息
    object: ChatObject |None = None # 对象消息

class ChatResponse(BaseModel):
    """聊天响应对象"""
    sender_id: str # 发送者id
    message_id: str # 消息id
    messages: list[ChatMessage] # 客服返回的消息列表

class HistoryMessage(BaseModel):
    """聊天历史消息对象"""
    role : str
    text: str | None = None
    object: ChatObject |None = None

class HistoryResponse(BaseModel):
    """聊天历史响应对象"""
    sender_id :str
    messages: list[HistoryMessage]

if __name__=="__main__":
    c=ChatObject(type="1",id="2")
