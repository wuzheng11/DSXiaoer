from atguigu.task.action.base import Action
from atguigu.task.action.custom.lookup_logistics import LookupLogisticsAction
from atguigu.task.action.custom.lookup_order_status_action import LookupOrderStatusAction
from atguigu.task.action.custom.recommend_similar_products import RecommendSimilarProductsAction


class ActionRegistry:

    def __init__(self):
        """初始化注册表"""
        self._actions:dict[str, Action] = {}

    def register(self,action:Action)->None:
        """注册Action"""
        self._actions[action.name] = action

    def get(self,name:str)->Action:
        """根据Action名字获取对象"""
        return self._actions[name]

if __name__ == '__main__':
    # 创建注册表实例(手动注册)
    registry = ActionRegistry()
    registry.register(LookupOrderStatusAction())
    registry.register(LookupLogisticsAction())
    registry.register(RecommendSimilarProductsAction())

    print(registry)