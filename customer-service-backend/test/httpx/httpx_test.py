import httpx


# 用法1：入门  同步方式 直接使用httpx访问远程资源
# 使用顶层API发送请求，HTTPX 必须为每个请求建立新的连接（连接不会被重复使用）
# r = httpx.get('http://127.0.0.1:18081/users/u1001/orders')
# print(r.status_code)
# print(r.headers['content-type'])
# print(r.text)

# 用法2： 使用client  with
# with httpx.Client() as client:
#     r = client.get('http://127.0.0.1:18081/users/u1001/orders')
#     print(type(r.json())) # dic
#     print(type(r.text)) # str
#
#     data = r.json()
#     print(data.get("data").get("orders"))

# 用法3： 使用client  close
client = httpx.Client()
try:
    r = client.get('http://127.0.0.1:18081/users/u1001/orders')
    print(type(r.json())) # dic
    print(type(r.text)) # str

    data = r.json()
    print(data.get("data").get("orders"))
finally:
    client.close()