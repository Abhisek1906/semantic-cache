import redis
import json
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import REDIS_HOST, REDIS_PORT, SIMILARITY_THRESHOLD

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def store_entry(key, prompt, embedding, response, metadata):
    entry = {
        "prompt": prompt,
        "embedding": embedding,
        "response": response,
        "metadata": metadata
    }

    r.rpush(key, json.dumps(entry))


def find_similar(key, query_embedding):
    entries = r.lrange(key, 0, -1)

    if not entries:
        return None

    valid_entries = []
    embeddings = []

    current_time = int(time.time())

    for entry in entries:
        obj = json.loads(entry)

        # TTL check
        age = current_time - obj["metadata"]["timestamp"]
        if age > obj["metadata"]["ttl"]:
            continue

        valid_entries.append(obj)
        embeddings.append(obj["embedding"])

    if not valid_entries:
        return None

    similarities = cosine_similarity(
        [query_embedding],
        embeddings
    )[0]

    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    print(f"Best similarity score: {best_score}")

    if best_score >= SIMILARITY_THRESHOLD:
        valid_entries[best_idx]["metadata"]["hit_count"] += 1
        return valid_entries[best_idx]["response"]

    return None