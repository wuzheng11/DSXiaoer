from atguigu.domain.message import UserMessage, ProcessResult
from atguigu.domain.state import DialogueState


class DialogueEngine:
    """
    1. 准备当前会话和本轮对话记录。
    2. 区分文本消息和对象消息。
    3. 理解文本消息，形成当前轮次的处理计划。
    4. 检查处理计划是否明确、完整并且可以执行。
    5. 将消息交给任务、知识检索、闲聊或澄清模块。
    6. 汇总本轮产生的客服回复。
    7. 将完整轮次写入会话历史。
    """
    async def process_message(self, state:DialogueState,user_message:UserMessage)->ProcessResult:
        """
        1. 使用 `sender_id` 加载当前用户的 `DialogueState`。
        2. 调用 `DialogueEngine` 处理用户消息。
        3. 保存已经更新的 `DialogueState`。
        4. 返回 `ProcessResult`。
        :param state:
        :param user_message:
        :return:
        """
        pass