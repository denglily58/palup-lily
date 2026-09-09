"""LUNA × Lily — FastAPI backend entry point."""
import os
from pathlib import Path
from time import monotonic
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel

from tools.catalog import full_context
from tools.metrics import aggregate, log_chat
from db.supabase_client import log_event, recent_events

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(title="LUNA × Lily Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.6-flash"

# In-memory session store (demo only; production uses Supabase)
_sessions: dict = {}
MAX_HISTORY = 10  # last N messages per session
MAX_SESSION_LEN = 20  # cap to avoid memory bloat


def get_history(session_id: Optional[str]) -> list:
    if not session_id:
        return []
    return _sessions.get(session_id, [])[-MAX_HISTORY:]


def append_to_session(session_id: Optional[str], role: str, content: str) -> None:
    if not session_id:
        return
    _sessions.setdefault(session_id, []).append({"role": role, "content": content})
    if len(_sessions[session_id]) > MAX_SESSION_LEN:
        _sessions[session_id] = _sessions[session_id][-MAX_SESSION_LEN:]


def format_history(history: list) -> str:
    if not history:
        return ""
    lines = ["## Recent Conversation"]
    for m in history:
        role = "User" if m["role"] == "user" else "Lily"
        lines.append(f"{role}: {m['content']}")
    return "\n".join(lines) + "\n"

SYSTEM_PROMPT_EN = (
    "You are Lily, AI beauty consultant for LUNA Beauty, a vegan cruelty-free "
    "cosmetics brand based in LA serving North America. "
    "Voice: warm, professional, inclusive, brand-forward — never pushy. "
    "Keep answers to 2-3 sentences unless the user asks for detail. "
    "Recommend based on undertone, occasion, and reviews. "
    "If asked about products/orders/shipping specifics not yet connected, "
    "honestly say 'This is still being wired up — I'll have full data soon.' "
    "Never make up product names, prices, or reviews."
)

SYSTEM_PROMPT_ZH = (
    "你是 Lily，LUNA Beauty 純素美妝品牌（總部洛杉磯，主打北美）的 AI 顧問。"
    "語氣：溫暖、專業、包容、有品牌感，不推銷。"
    "回覆 2-3 句為主，除非客人要細節。"
    "根據膚色底調、場合、評論做推薦。"
    "若被問到具體商品/訂單/物流資料還沒接上，就誠實說『這部分還在串接、之後會全部通』。"
    "絕對不編商品名、價格、或評論。"
)


class ChatRequest(BaseModel):
    message: str
    lang: str = "en"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


@app.get("/health")
def health():
    return {"status": "ok", "service": "lily-backend", "version": "0.2.0"}


@app.get("/metrics")
def metrics():
    """Aggregate token/cost/latency stats — used by B端 AI usage widget."""
    return aggregate()


@app.post("/reset")
def reset_session(session_id: str):
    """Clear a session's memory. Used by 'Reset conversation' demo button."""
    _sessions.pop(session_id, None)
    return {"status": "reset", "session_id": session_id}


class EventPayload(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    action: str
    target: Optional[str] = None
    metadata: Optional[dict] = None


@app.post("/events")
def post_event(payload: EventPayload):
    """Log an event (login, logout, pin, etc) to event_logs table."""
    log_event(
        user_id=payload.user_id,
        user_email=payload.user_email,
        action=payload.action,
        target=payload.target,
        metadata=payload.metadata,
    )
    return {"status": "logged"}


@app.get("/events")
def get_events(limit: int = 50):
    """Fetch recent events for B端 activity log tab."""
    return {"events": recent_events(limit=limit)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    system = SYSTEM_PROMPT_ZH if req.lang == "zh" else SYSTEM_PROMPT_EN
    catalog = full_context(req.lang)
    history = get_history(req.session_id)
    history_text = format_history(history)
    full_prompt = f"{system}\n\n{catalog}\n\n{history_text}User: {req.message}"

    start = monotonic()
    try:
        response = gemini.models.generate_content(
            model=MODEL,
            contents=full_prompt,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}")

    latency_ms = int((monotonic() - start) * 1000)
    usage = response.usage_metadata
    input_tokens = (usage.prompt_token_count if usage else 0) or 0
    output_tokens = (usage.candidates_token_count if usage else 0) or 0

    from tools.metrics import estimate_cost
    cost = estimate_cost(input_tokens, output_tokens, MODEL)

    reply_text = response.text or ""

    # Append this turn to session memory for future context
    append_to_session(req.session_id, "user", req.message)
    append_to_session(req.session_id, "assistant", reply_text)

    # Local JSONL for Q7 token/cost aggregation
    log_chat(
        session_id=req.session_id,
        endpoint="/chat",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        model=MODEL,
        lang=req.lang,
        user_msg_preview=req.message,
    )

    # Also write to Supabase event_logs so B端 activity log sees it
    log_event(
        user_id=None,  # buyer is anonymous
        user_email="buyer (anonymous)",
        action="chat_query",
        target=req.session_id,
        metadata={
            "message_preview": req.message[:100],
            "lang": req.lang,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        },
    )

    return ChatResponse(
        reply=reply_text,
        model=MODEL,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=round(cost, 6),
    )
