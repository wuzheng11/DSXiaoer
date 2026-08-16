from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 指向根目录项的 .env 文件
ENV_FILE = Path(__file__).parents[2] / '.env'

class Settings(BaseSettings):

    # LLM
    # 配置优先（环境变量、.env配置）
    llm_model: str

    # Settings中有，配置中没有，则会读取这里的默认值，如果没有默认值，则会报错
    llm_base_url: str = "https://ws-030ava7nvqx6kfb9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    llm_api_key: str

    # 数据库
    database_url: str

    # 商城 API
    commerce_api_base_url: str

    # 服务器
    app_host: str
    app_port: int

    # 从 .env 文件中读取配置信息
    # 如果读取的是真实的系统环境变量，则不写这句话
    # extra="ignore"： 表示忽略 .env中有，但是Settings中没有的配置项，不会报错
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

settings = Settings()

if __name__ == '__main__':

    print(type(settings.app_port))

    print(Path(__file__).parents[2] / '.env')

    print(settings.llm_base_url)