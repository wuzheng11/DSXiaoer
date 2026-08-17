from atguigu.domain.message import UserMessage
from atguigu.domain.state import DialogueState


class DialogueEngine:
    async def process_message(self, state:DialogueState,user_message:UserMessage):
        pass