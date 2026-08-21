from atguigu.domain.message import UserMessage, MessageType, MessageObject, BotMessage
from atguigu.domain.state import Turn


class HistoryBuilder:
    """构建历史对话"""

    @staticmethod
    def build(turns: list[Turn]) -> str:
        """
            将对轮对话渲染成
            USER: xxx
            BOT: xxx
            BOT: xxx
            USER: xxx
            BOT: xxx

            :param turns: 轮次信息
            :return: 组装好的历史记录字符串
        """
        messages: list[str] = []
        for turn in turns:
            user_message = HistoryBuilder.render_usr_message(turn.user_message)
            messages.append(f"USER:{user_message}")

            for bot_message in turn.bot_messages:
                rendered_bot_message=HistoryBuilder._render_bot_message(turn.bot_messages)
                messages.append(f"BOT:{rendered_bot_message}")

        return "\n".join(messages)

    @staticmethod
    def render_user_message(user_message:UserMessage):
        if user_message.type is MessageType.TEXT:
            return HistoryBuilder._render_text(user_message.text)
        return HistoryBuilder._render_object(user_message.object)

    @staticmethod
    def _render_bot_message(bot_messages: BotMessage):
        if bot_messages.text:
            return HistoryBuilder._render_text(bot_messages.text)
        return HistoryBuilder._render_object(bot_messages.object)

    @staticmethod
    def _render_text(text:str)->str:
        return text.strip()

    @staticmethod
    def _render_object(message_object:MessageObject):
        return json.dumps(asdict(message_object),ensure_ascii=False)


if __name__ == '__main__':

    data = {
        "a": 100,
        "b": 200
    }

    result = json.dumps(data)

    print(result)
    print(type(result))