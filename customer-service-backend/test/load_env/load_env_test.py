import os

from dotenv import load_dotenv

load_dotenv(override=True)
print(type(int(os.getenv("APP_PORT"))))