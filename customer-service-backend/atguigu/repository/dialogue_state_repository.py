import asyncio

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.clients import database
from atguigu.clients.database import init_db_engine, close_db_engine
from atguigu.domain.state import DialogueState, SharedState, FocusedObject
from atguigu.models.dialogue_state import DialogueStateRecord, DIALOGUE_STATE_ADAPTER


class DialogueStateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_state(self, sender_id: str) -> DialogueState:
        # 将state存储到数据库
        """
        1. 根据 `sender_id` 查询 `DialogueStateRecord`。
        2. 使用 `scalar_one_or_none()` 取得状态记录。
        3. 如果记录不存在，创建新的 `DialogueState`。
        4. 如果记录存在，使用 `TypeAdapter` 将 `state_json` 还原成 `DialogueState`。
        :param sender_id:
        :return:
        """
        # 定义sql对象
        sql = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        # 执行sql
        result = await self.session.execute(sql)
        # 获取结果
        record = result.scalar_one_or_none()
        if record:
            state = DIALOGUE_STATE_ADAPTER.validate_json(record.state_json)
            return state
        else:
            # 新用户还没有数据库记录
            return DialogueState(sender_id=sender_id)

    async def save_state(self, state: DialogueState) -> None:
        # 将state保存到数据库
        """
        1. 使用 `TypeAdapter` 将 `DialogueState` 转换成 JSON 字符串。
        2. 使用 `sender_id` 和 `state_json` 构造 INSERT 语句。
        3. 如果 `sender_id` 已经存在，则更新原记录的 `state_json`。
        4. 执行 SQL 并提交事务。
        :param sender_id:
        :return:
        """
        # 方案一，根据sender_id查询数据库中是否有当前state记录，有则update，无则insert
        # 方案二，直接insert，成功则直接返回，失败则升级为update
        state_json = DIALOGUE_STATE_ADAPTER.dump_json(state).decode("utf-8")

        # 插入
        statement = insert(DialogueStateRecord).values(sender_id=state.sender_id, state_json=state_json)
        # 当on_duplicate_key_update放生的时候，insert升级为update
        statement = statement.on_duplicate_key_update(state_json=state_json)
        # 执行sql
        await self.session.execute(statement)
        # 提交事务
        await self.session.commit()

if __name__ == '__main__':

    init_db_engine()

    async def test():

        # 当init_db_engine()尚未调用，session_factory还是None的时候就被引入了
        # 之后init_db_engine()被调用，此处的session_factory还是None，并不会被改变，因为他是个副本
        # async with session_factory() as session:

        # 直接引入database，当init_db_engine()被调用，database中的session_factory才会被改变
        # 此时database.session_factory非空，可以使用了
        async with database.session_factory() as session:
            repository = DialogueStateRepository(session)
            await repository.save_state(
                state=DialogueState(
                    sender_id="1",
                    shared=SharedState(
                        focused_object=FocusedObject(type="order", id="abc")
                    )
                ))
            state = await repository.load_state(sender_id="1")
            print(state)

        await close_db_engine()

    asyncio.run(test())