import httpx


# 使用异步连接
async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get('http://127.0.0.1:18081/users/u1001/orders')
        print(type(r.json())) # dic
        print(type(r.text)) # str

        data = r.json()
        print(data.get("data").get("orders"))

if __name__ == '__main__':

    import asyncio
    asyncio.run(main())
