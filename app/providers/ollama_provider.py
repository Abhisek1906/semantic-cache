import httpx
from app.providers.base import BaseProvider


class OllamaProvider(BaseProvider):

    async def generate(self, prompt: str):
        """Non-streaming response"""
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            return response.json()["response"]

    async def generate_stream(self, prompt: str):
        """Streaming response"""
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "tinyllama",
            "prompt": prompt,
            "stream": True
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for chunk in response.aiter_text():
                    yield chunk