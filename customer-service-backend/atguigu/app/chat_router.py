import uuid

from fastapi import APIRouter

from atguigu.app.schemas import ChatObject, ChatResponse, ChatMessage, HistoryResponse, HistoryMessage

#声明路由对象
chat_router=APIRouter()

@chat_router.post("/api/chat")
async def chat(chat_request: ChatObject)->ChatResponse:
    #调用业务层


    return ChatResponse(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id if chat_request.message_id else str(uuid.uuid4()),
        messages=[ChatMessage(text="11111")]
    )

@chat_router.get("/api/chat/history")
async def history(sender_id: str)->HistoryResponse:

    return HistoryResponse(
        sender_id=sender_id,
        messages=[
            HistoryMessage(role="user",text="222222"),
            HistoryMessage(role="bot",text="333333")
        ]
    )