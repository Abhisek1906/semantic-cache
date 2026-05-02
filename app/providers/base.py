from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    async def generate(self, prompt: str):
        pass

    @abstractmethod
    async def generate_stream(self, prompt: str):
        pass