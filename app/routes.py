from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.schemas import ChatCompletionRequest
from app.embeddings import get_embedding
from app.cache import find_similar, store_entry
from app.utils import generate_cache_key, hash_system_prompt
from app.models import build_metadata
from app.providers.router import get_provider
from app.config import CACHE_TTL

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat(req: ChatCompletionRequest, raw_request: Request):

    # Combine messages → prompt
    prompt = " ".join([m.content for m in req.messages])
    system_prompt = next(
        (m.content for m in req.messages if m.role == "system"),
        ""
    )

    key = generate_cache_key(
        system_prompt,
        req.model,
        req.temperature,
        req.max_tokens
    )

    embedding = get_embedding(prompt)

    cached = find_similar(key, embedding)

    # ✅ CACHE HIT
    if cached:
        return JSONResponse(
            content={
                "id": "cache-hit",
                "object": "chat.completion",
                "choices": [{
                    "message": {"role": "assistant", "content": cached}
                }]
            },
            headers={"X-Cache": "HIT"}
        )

    # ❌ CACHE MISS
    provider = get_provider(req.model)

    # STREAMING CASE
    if req.stream:
        async def stream_response():
            full_response = ""

            async for chunk in provider.generate_stream(prompt):
                full_response += chunk
                yield chunk

            # store after complete
            metadata = build_metadata(
                req.model,
                req.temperature,
                req.max_tokens,
                hash_system_prompt(system_prompt),
                CACHE_TTL
            )

            store_entry(key, prompt, embedding, full_response, metadata)

        return StreamingResponse(stream_response(), headers={"X-Cache": "MISS"})

    # NON-STREAM
    response = await provider.generate(prompt)

    metadata = build_metadata(
        req.model,
        req.temperature,
        req.max_tokens,
        hash_system_prompt(system_prompt),
        CACHE_TTL
    )

    store_entry(key, prompt, embedding, response, metadata)

    return JSONResponse(
        content={
            "id": "chatcmpl-xyz",
            "object": "chat.completion",
            "choices": [{
                "message": {"role": "assistant", "content": response}
            }]
        },
        headers={"X-Cache": "MISS"}
    )