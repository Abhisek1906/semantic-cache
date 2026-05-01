import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.95))
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))