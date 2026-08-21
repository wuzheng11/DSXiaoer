import uuid
from dataclasses import dataclass, field
from typing import Any

from atguigu.domain.message import UserMessage, BotMessage
from atguigu.task.lifecycle.models import TaskRef, TaskEvent, TaskStarted, TaskSwitched, TaskCanceled, TaskResumed


@dataclass
class Turn:
    """一轮对话"""
    #一个turn对应一次用户输入和由这次输入产生的全部客服回复
    turn_id: str
    user_message: UserMessage
    bot_messages: list[BotMessage] = field(default_factory=list)


@dataclass
class Session:
    """会话"""
    #表示一段连续的对话
    session_id: str
    started_at: float
    last_activity_at: float
    closed_at: float | None = None
    turns: list[Turn] = field(default_factory=list)  #当前会话包含的全部对话轮次


@dataclass
class FocusedObject:
    """聚焦对象"""
    #用户当前关注的业务对象
    type: str #类型，如order/product等
    id: str
    title: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class SharedState:
    #保存任务型对话、知识检索型对话和闲聊型对话共同使用的状态
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(default_factory=list)
    def current_session(self)->Session:
        return self.sessions[-1]


@dataclass
class TaskInstance:
    """任务实例"""
    #表示某条任务流程的一次具体执行
    flow_id: str
    step_id: str | None = None
    slots: dict[str, Any] = field(default_factory=dict)

    # 使用lambda的形式定义复杂函数的匿名引用
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    def to_ref(self)->TaskRef:
        """将TaskInstance对象转换成TaskRef对象"""
        return TaskRef(task_id=self.task_id,flow_id=self.flow_id)


@dataclass
class TaskState:
    """任务相关的状态信息"""
    active: TaskInstance | None = None #当前正在执行的任务
    paused: list[TaskInstance] = field(default_factory=list) #已经暂停，后续可恢复的任务

    def start(self,task: TaskInstance)->TaskEvent:
        #当active中没有活跃任务时，直接将要开启的新任务存储在active里
        if self.active is None:
            self.active=task
            return TaskStarted(task=task.to_ref())
        #当active里有任务，需要将正在执行的任务暂停，并将新任务放入active中
        previous=self.active
        self.paused.append(previous)
        self.active=task
        return TaskSwitched(previous=previous.to_ref(),current=task.to_ref())

    def cancel(self, task_id: str) -> TaskCanceled:

        # 要取消的任务就是当前正在执行的任务（active），直接将active置空，表示现在没有正在执行的任务了
        if self.active is not None and self.active.task_id == task_id:
            canceled = self.active
            self.active = None  # 取消任务
            return TaskCanceled(task=canceled.to_ref())

        # 要取消的是暂停列表中的任务（paused），去暂停列表中找对应的任务，如果找到怎就将这个任务记录下来
        canceled = None
        for task in self.paused:
            if task.task_id == task_id:
                canceled = task
                break

        # 如果找到任务则将其从列表中移除，表示这个任务被取消了
        if canceled is not None:
            self.paused.remove(canceled)
            return TaskCanceled(task=canceled.to_ref())

        raise ValueError(f"Task {task_id} not found")

    def resumed(self, task_id: str) -> TaskEvent:

        # 第一步：从paused中找到要回复的那个任务
        target = next(task for task in self.paused if task.task_id == task_id)
        self.paused.remove(target)

        # 当前没有任务在执行（active是空的），将恢复的任务直接放入active
        if self.active is None:
            self.active = target
            return TaskResumed(task=target.to_ref())

        # 当前有任务在执行（active不是空的），将正在执行的任务放入暂停任务列表
        previous = self.active
        self.paused.append(previous)
        # 将要恢复的任务放入active
        self.active = target
        return TaskSwitched(
            previous=previous.to_ref(),
            current=target.to_ref()
        )

    def set_slots(self, slots: dict[str, Any]) -> None:
        self.active.slots.update(slots)

    def complete_active(self)->None:
        self.active=None


@dataclass
class DialogueState:
    """会话上下文的状态信息"""
    #保存某个用户的完整的对话状态

    sender_id: str
    shared: SharedState = field(default_factory=SharedState)
    tasks: TaskState = field(default_factory=TaskState)


if __name__ == '__main__':
    ti = TaskInstance("a", "start")
    print(ti)

    # uuid = str(uuid.uuid4())
    # print(type(uuid))

    ll = []
    ll1 = list()
