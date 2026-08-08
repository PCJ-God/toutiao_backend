from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

from agent.ai import stream_chat
from schemas.ai import ChatRequest


router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat")
async def chat(req: ChatRequest):
    async def event_stream():
        async for token in stream_chat(req.messages):
            chunk = {"choices": [{"delta": {"content": token}, "index": 0}]}
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
