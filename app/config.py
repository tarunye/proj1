import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    AIPROXY_TOKEN: str = os.environ.get("AIPROXY_TOKEN")
    AIPROXY_BASE_URL: str = "https://aiproxy.sanand.workers.dev/openai"
    DATA_DIR: str = "/data"
    
    class Config:
        env_file = ".env"

settings = Settings()
