import uuid
from dataclasses import dataclass, field
from typing import Any

from atguigu.domain.message import UserMessage


@dataclass
class Turn:
    """一轮对话"""
    turn_id: str
    user_message: UserMessage
    bot_messages: list[UserMessage] = field(default_factory=list)


@dataclass
class Session:
    """会话"""
    session_id: str
    started_at: float
    last_activity_at: float
    closed_at: float | None = None
    turns: list[Turn] = field(default_factory=list)


@dataclass
class FocusedObject:
    """聚焦对象"""
    type: str
    id: str
    title: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class SharedState:
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(default_factory=list)


@dataclass
class TaskInstance:
    """任务实例"""
    flow_id: str
    step_id: str | None = None
    slots: dict[str, Any] = field(default_factory=dict)

    # 使用lambda的形式定义复杂函数的匿名引用
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class TaskState:
    """任务相关的状态信息"""
    active: TaskInstance | None = None
    paused: list[TaskInstance] = field(default_factory=list)

@dataclass
class DialogueState:
    """会话上下文的状态信息"""

    sender_id: str
    shared: SharedState = field(default_factory=SharedState)
    task: TaskState = field(default_factory=TaskState)


if __name__ == '__main__':
    ti = TaskInstance("a", "start")
    print(ti)

    # uuid = str(uuid.uuid4())
    # print(type(uuid))

    ll = []
    ll1 = list()
