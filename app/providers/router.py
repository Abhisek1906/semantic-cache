from app.providers.ollama_provider import OllamaProvider


def get_provider(model: str):
    if "llama" in model:
        return OllamaProvider()

    raise ValueError(f"Unsupported model: {model}")