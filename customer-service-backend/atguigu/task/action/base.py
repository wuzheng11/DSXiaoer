from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any

from atguigu.domain.state import DialogueState


@dataclass
class ActionResult:
    #每个action的统一返回结果
    slot_updates: dict[str, Any] = field(default_factory=dict)


class Action:
    #每个自定义action的唯一标识
    name: str

    @abstractmethod
    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        """从 `DialogueState` 读取当前任务数据，通过 `action_kwargs` 接收 Flow 中配置的固定参数，
           再使用 `ActionResult.slot_updates` 返回需要写回任务的数据。
        """
        #action入口
        pass