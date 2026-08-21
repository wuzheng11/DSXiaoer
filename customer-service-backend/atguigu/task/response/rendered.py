from typing import Any

from jinja2 import Template
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from atguigu.domain.message import UserMessage, BotMessage
from atguigu.domain.state import DialogueState
from atguigu.prompts.history_builder import HistoryBuilder
from atguigu.task.response.models import ResponseTemplate, ResponseMode


class ResponseRendered:
    def __init__(self, llm: Any | None) -> None:
        self.llm = llm

    async def render(self,template:ResponseTemplate,state:DialogueState,user_message:UserMessage)->BotMessage:
        """
        - `STATIC`：渲染 `template.text`，再将结果直接包装为 `BotMessage`；
        - `REPHRASE`：渲染 `template.text`，再将结果作为基础回复传给 `_call_llm()`；
        - `GENERATE`：不读取 `template.text`，直接调用 `_call_llm()` 生成回复。
        :param template:
        :param state:
        :param user_message:
        :return:
        """
        """按照模板的三种模式分别渲染回复信息"""
        if template.mode is ResponseMode.STATIC:
            #直接用槽位数据渲染
            slots=state.tasks.active.slots if state.tasks else {}
            rendered_text=Template(template.text).render(slots)
            return BotMessage(text=rendered_text)

        if template.mode is ResponseMode.REPHRASE:
            #将用户输入的文本先进行槽位渲染，再交给大模型
            slots=state.tasks.active.slots if state.tasks else {}
            rendered_text=Template(template.text).render(slots)
            text =await self._call_llm(template.prompt,state,user_message,rendered_text)
            return BotMessage(text=text)

        if template.mode is ResponseMode.GENERATE:
            #直接将prompt交给大模型
            text =self._call_llm(template.prompt,state,user_message)
            return BotMessage(text=text)

    async def _call_llm(self, prompt:str, state:DialogueState, user_message:UserMessage, current_response=""):
        #加载jinja2模板
        PromptTemplate.from_template(prompt,template_format="jinja2")
        #组装链
        chain=prompt | self.llm | StrOutputParser()

        #获取聊天历史
        #获取当前session
        session=state.shared.current_session()
        #获取turns
        turns=session.turns

        #调用大模型
        return await chain.ainvoke({
            "history":HistoryBuilder.build(turns),
            "user_message":HistoryBuilder.render_user_message(user_message),
            "current_response":current_response,
        })