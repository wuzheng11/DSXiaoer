from atguigu.domain.message import BotMessage, UserMessage
from atguigu.domain.state import DialogueState
from atguigu.task.flow.conditions import ConditionEvaluator
from atguigu.task.flow.links import StaticLink, FallbackLink, ConditionalLink
from atguigu.task.flow.models import FlowCatalog
from atguigu.task.flow.steps import StartFlowStep, ResponseFlowStep, CollectSlotStep, ActionFlowStep, EndFlowStep, \
    FlowStep


class FlowExecutor:

    def __init__(
            self,
            condition_evaluator: ConditionEvaluator,
            max_steps_per_turn: int = 100) -> None:

        self.condition_evaluator = condition_evaluator
        self.max_steps_per_turn = max_steps_per_turn

    async def run_task(self, state: DialogueState, flows: FlowCatalog, user_message: UserMessage) -> list[BotMessage]|None:
        """按步骤推进流程的执行，并返回机器人回复结果列表"""

        messages: list[BotMessage] = []

        for _ in range(self.max_steps_per_turn):

            # 获取当前活跃任务
            task = state.tasks.active

            # 情况1：如果不存在活跃任务，则返回messages
            if task is None:
                return messages

            # 情况2：如果存在活跃任务，则根据当前活跃任务推进流程(执行每一个步骤，每个步骤执行策略不同，分别处理)
            # 获取流程
            flow = flows.get_flow(task.flow_id)
            # 获取步骤
            step = flow.get_step(task.step_id)

            if isinstance(step, StartFlowStep):
                self._advance(step, state)
                continue

            if isinstance(step, ResponseFlowStep):
                pass

            if isinstance(step, CollectSlotStep):
                pass

            if isinstance(step, ActionFlowStep):
                pass

            if isinstance(step, EndFlowStep):
                pass

    def _advance(self, step: FlowStep, state: DialogueState) -> None:

        for link in step.next:
            if isinstance(link, StaticLink):
                state.tasks.active.step_id = link.target
                return
            if isinstance(link, FallbackLink):
                state.tasks.active.step_id = link.target
                return
            if isinstance(link, ConditionalLink):
                if self.condition_evaluator.evaluate(link.condition, {"slots": state.tasks.active.slots}):
                    state.tasks.active.step_id = link.target
                return
