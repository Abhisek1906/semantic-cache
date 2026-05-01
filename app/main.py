from app.embeddings import get_embedding, normalize
from app.cache import find_similar, store_entry
from app.utils import generate_cache_key, hash_system_prompt
from app.models import build_metadata
from app.config import CACHE_TTL


def simulate_request(prompt, system_prompt, model, temperature, max_tokens):
    key = generate_cache_key(system_prompt, model, temperature, max_tokens)

    embedding = get_embedding(normalize(prompt))

    cached_response = find_similar(key, embedding)

    if cached_response:
        print("\n✅ Cache Hit:")
        print(cached_response)
        return

    print("\n❌ Cache Miss → Generating response...")

    # Fake LLM response (Phase 1)
    response = f"[LLM RESPONSE] {prompt} -> This is a simulated answer."

    metadata = build_metadata(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt_hash=hash_system_prompt(system_prompt),
        ttl=CACHE_TTL
    )

    store_entry(key, prompt, embedding, response, metadata)

    print("\nStored response:")
    print(response)


if __name__ == "__main__":
    # First call
    simulate_request(
        prompt="What is Python?",
        system_prompt="You are a helpful assistant",
        model="test-model",
        temperature=0.7,
        max_tokens=200
    )

    print("\n--------------------------\n")

    # Similar call (should hit cache)
    simulate_request(
        prompt="Explain Python to me",
        system_prompt="You are a helpful assistant",
        model="test-model",
        temperature=0.7,
        max_tokens=200
    )

    print("\n--------------------------\n")

    # Different system prompt (should MISS)
    simulate_request(
        prompt="Explain Python to me",
        system_prompt="You are a sarcastic assistant",
        model="test-model",
        temperature=0.7,
        max_tokens=200
    )