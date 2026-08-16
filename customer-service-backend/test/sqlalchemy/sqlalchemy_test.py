from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from atguigu.conf.config import settings

"""
三要素：
1、引擎 engine
2、session工厂 session_factory: 通过sessionmaker创建
3、session对象：通过session工厂创建
"""

async def run_some_sql(
    async_session_factory: async_sessionmaker[AsyncSession],
) -> None:

    # 通过async_session_factory获取session对象
    async with async_session_factory() as session:

        # execute 接收一个SQL对象
        result = await session.execute(text("SELECT 1"))
        data = result.fetchone()
        print(data)
        print(type(data))

        # 显示提交
        await session.commit()

async def main() -> None:

    # 1. 创建异步引擎
    # 自动初始化了一个数据库连接池
    engine = create_async_engine(
        settings.database_url,

        # SQL 日志打印开关，False关闭，True开启。开发时开启，生产时关闭
        echo = True,

        # 默认值False
        # 当设置成 True 时：
        # 每次从数据库连接池中取出连接前，先执行一条SQL语句（SELECT 1，连接探测），探测连接对象是否存活
        # 如果连接已断开，则丢弃这个连接，尝试获取新连接
        pool_pre_ping=True,
        pool_size=5, # 数据库连接池中的常规连接数
        max_overflow=10, # 数据库连接池中最大连接数
        pool_recycle=180, # 数据库连接池中连接的回收时间，单位为秒
    )

    # 2. 创建异步session工厂
    async_session_factory = async_sessionmaker(engine)

    # 3. 执行sql
    await run_some_sql(async_session_factory)

    # 4. 释放数据库引擎和session工厂资源
    await engine.dispose()

if __name__ == '__main__':

    import asyncio
    asyncio.run(main())