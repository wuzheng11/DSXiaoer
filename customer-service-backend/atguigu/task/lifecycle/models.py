from dataclasses import dataclass
from typing import TypeAlias

"""
TaskEvent用于记录任务生命周期的变化
"""
@dataclass
class TaskRef:
    task_id: str
    flow_id: str

@dataclass
class TaskStarted:
    task: TaskRef

@dataclass
class TaskSwitched:
    previous: TaskRef
    current: TaskRef

@dataclass
class TaskResumed:
    task: TaskRef

@dataclass
class TaskCanceled:
    task: TaskRef

TaskEvent: TypeAlias=(
    TaskStarted
    | TaskSwitched
    | TaskResumed
    | TaskCanceled
)