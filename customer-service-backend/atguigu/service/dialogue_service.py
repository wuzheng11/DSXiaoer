from atguigu.domain.message import UserMessage, ProcessResult
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_state_repository import DialogueStateRepository
from atguigu.domain.state import DialogueState

class DialogueService:
    def __init__(self,dialogue_state_repository:DialogueStateRepository,dialogue_engine:DialogueEngine)->None:
        self.dialogue_state_repository = dialogue_state_repository
        self.dialogue_engine = dialogue_engine

    async def process_message(self, user_message:UserMessage)->ProcessResult:
        #利用持久层组件加载state
        state: DialogueState=await self.dialogue_state_repository.load_state(user_message.sender_id)
        #利用引擎计算
        process_result: ProcessResult = await self.dialogue_engine.process_message(state,user_message)
        #调用持久层存储state
        await self.dialogue_state_repository.save_state(state)

        return process_result