def build_metadata(model, temperature, max_tokens, system_prompt_hash, ttl):
    import time
    return {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system_prompt_hash": system_prompt_hash,
        "timestamp": int(time.time()),
        "ttl": ttl,
        "hit_count": 0
    }