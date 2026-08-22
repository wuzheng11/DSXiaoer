from typing import Any

from atguigu.clients import http_client
from atguigu.conf.config import settings
from atguigu.domain.state import DialogueState, TaskState, TaskInstance
from atguigu.task.action.base import Action, ActionResult

"""
自定义一个action的步骤
1. 定义 `Action` 子类。
2. 声明唯一的 `name`。
3. 实现 `run()` 方法。
4. 使用 `ActionResult` 返回业务数据。
"""
class LookupOrderStatusAction(Action):
    name="lookup_order_status_action"

    async def run(self,state:DialogueState,action_kwargs:dict[str,Any])->ActionResult:
        #获取槽位值
        order_number=state.tasks.active.slots.get("order_number")
        #组织远程api调用的url
        url=f"{settings.commerce_api_base_url}/orders/{order_number}"

        #执行远程调用
        response=await http_client.http_client.get(url)
        payload=response.json()["data"]
        include_summary=action_kwargs.get("include_summary",True)

        return ActionResult(
            slot_updates={
                "order_status":payload.get("status_desc") or payload.get("status") or "未知",
                "order_summary": f"订单金额：¥{payload.get('amount')}" if include_summary else ""
            }
        )


if __name__ == '__main__':


    http_client.init_http_client()

    async def test():
        action = LookupOrderStatusAction()


        state = DialogueState(
            sender_id = "u1001",
            tasks=TaskState(
                active=TaskInstance(
                    flow_id="order_status_query",
                    step_id="lookup_order_status",
                    slots={"order_number": "A20260410001"}
                )
            )
        )

        result = await action.run(state, {})
        print(result)

        await http_client.close_http_client()

    import asyncio
    asyncio.run(test())