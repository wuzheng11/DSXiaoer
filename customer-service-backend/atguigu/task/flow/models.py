from dataclasses import dataclass, field

from atguigu.task.flow.steps import FlowStep, FlowStepType


@dataclass
class FlowSlot:
    #flow可以使用的一个业务字段
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
    def get_start_step(self):
        for step in self.steps:
            if step.type is FlowStepType.START:
                return step
        raise Exception("no start step found")

    def get_step(self,step_id:str)->FlowStep:
        """获取步骤对象"""
        for step in self.steps:
            if step.id==step_id:
                return step
        raise Exception("no step found")


@dataclass
class FlowCatalog:
    flows: dict[str,Flow] = field(default_factory=dict)
    slots: dict[str,FlowSlot] =field(default_factory=dict)
    def get_flow(self,flow_id:str)->Flow:
        return self.flows[flow_id]

