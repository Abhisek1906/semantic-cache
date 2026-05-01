import hashlib
import json

def generate_cache_key(system_prompt, model, temperature, max_tokens):
    key_data = {
        "system_prompt": system_prompt,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    key_string = json.dumps(key_data, sort_keys=True)
    return "cache:" + hashlib.sha256(key_string.encode()).hexdigest()


def hash_system_prompt(system_prompt):
    return hashlib.sha256(system_prompt.encode()).hexdigest()