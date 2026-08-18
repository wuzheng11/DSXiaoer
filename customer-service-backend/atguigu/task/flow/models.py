from dataclasses import dataclass, field

from atguigu.task.flow.steps import FlowStep


@dataclass
class FlowSlot:
    name: str
    type: str ="any"
    label: str =""
    description: str =""

@dataclass
class Flow:
    id: str
    name: str | None=None
    description: str =""
    steps: list[FlowStep] =field(default_factory=list)
    slots: list[FlowSlot] =field(default_factory=list)


@dataclass
class FlowCatalog:
    flows: dict[str,Flow] = field(default_factory=dict)
    slots: dict[str,FlowSlot] =field(default_factory=dict)

