
from httpx import AsyncClient


# 声明全局变量
http_client: AsyncClient | None = None

# 初始化http客户端
def init_http_client():
    global http_client
    http_client = AsyncClient()

# 关闭http客户端
async def close_http_client():
    if http_client is not None:
        await http_client.aclose()

if __name__ == '__main__':
    init_http_client()

    async def test():
        response = await http_client.get("http://127.0.0.1:18081/users/u1001/orders")
        print(response.json())

        await close_http_client()

    import asyncio
    asyncio.run(test())
