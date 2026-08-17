from dataclasses import dataclass, field
from enum import Enum

@dataclass
class MessageObject:
    type: str
    id: str
    title: str | None=None
    attributes: dict=field(default_factory=dict)

@dataclass
class MessageType(Enum):
    TEXT ="text"
    OBJECT ="object"

@dataclass
class UserMessage:
    sender_id: str
    message_id: str
    type: MessageType
    text: str |None=None
    object: MessageObject |None=None

@dataclass
class BotMessage:
    """业务层使用的机器人消息对象"""
    #表示一条客服消息
    text: str |None=None
    object: MessageObject |None=None # 可以回复文本，也可以返回订单或商品等对象

@dataclass
class ProcessResult:
    """表示service返回的一次处理结果"""
    sender_id: str
    message_id: str
    messages: list[BotMessage]

if __name__=="__main__":
    user_message=UserMessage(
        sender_id="123",
        message_id="456",
        type=MessageType.TEXT,
        text="Hello World"
    )