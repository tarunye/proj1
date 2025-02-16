import httpx
from app.config import settings
import json

class LLMService:
    def __init__(self):
        self.base_url = settings.AIPROXY_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.AIPROXY_TOKEN}"
        }

    async def get_completion(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            return response.json()["choices"][0]["message"]["content"]

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/embeddings",
                headers=self.headers,
                json={
                    "model": "text-embedding-3-small",
                    "input": texts
                }
            )
            return [data["embedding"] for data in response.json()["data"]]

llm_service = LLMService()