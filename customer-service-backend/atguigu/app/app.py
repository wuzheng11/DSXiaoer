from fastapi import FastAPI

from atguigu.app.chat_router import chat_router


#创建fastapi实例，挂载路由对象
app=FastAPI()
app.include_router(chat_router)