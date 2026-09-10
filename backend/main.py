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
from tools.orders import lookup_order_by_email, lookup_order_by_number
from tools.returns import initiate_return
from tools.handoff import request_human_agent, log_demand_gap
from tools.analytics import dashboard_stats
from tools.lily_b_tools import (
    query_recent_chats,
    get_demand_gaps,
    get_handoff_queue,
    get_sales_summary,
)
from db.supabase_client import log_event, recent_events
from agents.loader import get_prompt

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(title="LUNA × Lily Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://palup-lily.vercel.app",
    ],
    allow_origin_regex=r"https://palup-lily-.*\.vercel\.app",   # preview deploys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.5-flash-lite"  # See backend/agents/model_registry.yaml for history

# Prompts loaded from versioned markdown files (see backend/agents/prompts/*_v1.md)
SYSTEM_PROMPT_EN = get_prompt("lily_c", "en")
SYSTEM_PROMPT_ZH = get_prompt("lily_c", "zh")
LILY_B_SYSTEM_PROMPT = get_prompt("lily_b", "en")

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

# Inline prompts removed — now loaded from backend/agents/prompts/*_v1.md via loader
# See constant assignments above.


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


@app.get("/admin/stats")
def admin_stats():
    """Return B端 dashboard 4 starter widget data."""
    return dashboard_stats()


@app.get("/products")
def products():
    """Public product catalog for C端 storefront (simplified fields)."""
    from tools.catalog import load_products, load_reviews
    all_products = load_products()
    all_reviews = load_reviews()

    def _emoji_for(category: str, sub: str) -> str:
        return {
            ("lip", "lipstick"): "💄",
            ("cheek", "blush"): "🌸",
            ("eye", "palette"): "🎨",
            ("eye", "brow"): "🖊",
            ("eye", "mascara"): "👁",
            ("base", "foundation"): "🧴",
            ("base", "cushion"): "☁️",
            ("base", "concealer"): "🎭",
            ("gift", "set"): "✨",
        }.get((category, sub), "💎")

    # Curated Unsplash e-commerce product photos (clean bg) per product_id
    # Fallback to LoremFlickr if not in map
    PRODUCT_IMAGES = {
        "prod_001": "https://images.unsplash.com/photo-1671575212918-0af5f840997a?w=400&auto=format&fit=crop",
        "prod_002": "https://images.unsplash.com/photo-1560130055-e3306e04884b?w=400&auto=format&fit=crop",
        "prod_003": "https://images.unsplash.com/photo-1625094640367-05f84293fe42?w=400&auto=format&fit=crop",
        "prod_004": "https://images.unsplash.com/photo-1533562530973-424ab36f1448?w=400&auto=format&fit=crop",
        "prod_005": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=400&auto=format&fit=crop",
        "prod_006": "https://images.unsplash.com/photo-1512207159096-c2c91b1dfadd?w=400&auto=format&fit=crop",
        "prod_007": "https://images.unsplash.com/photo-1627885793933-584e53987c14?w=400&auto=format&fit=crop",
        "prod_008": "https://images.unsplash.com/photo-1601231592547-d9453cd8b0da?w=400&auto=format&fit=crop",
        "prod_009": "https://images.unsplash.com/photo-1643185450492-6ba77dea00f6?w=400&auto=format&fit=crop",
        "prod_010": "https://images.unsplash.com/photo-1581132578702-92b6d43a9fee?w=400&auto=format&fit=crop",
    }

    def _image_url(product_id: str, sub: str) -> str:
        if product_id in PRODUCT_IMAGES:
            return PRODUCT_IMAGES[product_id]
        # Fallback
        keyword_map = {
            "lipstick": "lipstick,cosmetics",
            "blush": "blush,makeup",
            "palette": "eyeshadow,palette",
            "brow": "eyebrow,pencil",
            "mascara": "mascara,eyelash",
            "foundation": "foundation,bottle",
            "cushion": "cushion,compact",
            "concealer": "concealer,tube",
            "set": "makeup,gift,set",
        }
        kw = keyword_map.get(sub, "cosmetics,beauty")
        lock = sum(ord(c) for c in product_id) % 10000
        return f"https://loremflickr.com/400/400/{kw}?lock={lock}"

    result = []
    for p in all_products:
        pid = p["id"]
        reviews = [r for r in all_reviews if r["product_id"] == pid]
        avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else 0
        result.append({
            "id": p["id"],
            "sku": p["sku"],
            "name_en": p["name_en"],
            "name_zh": p["name_zh"],
            "category": p["category"],
            "subcategory": p["subcategory"],
            "price": p["price"],
            "shade_count": len(p["shades"]),
            "avg_rating": avg_rating,
            "review_count": len(reviews),
            "emoji": _emoji_for(p["category"], p["subcategory"]),
            "image_url": _image_url(p["id"], p["subcategory"]),
            "tags": p["tags"],
        })
    return {"products": result}


class AnalyticsChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


@app.post("/analytics/chat", response_model=ChatResponse)
def analytics_chat(req: AnalyticsChatRequest):
    """Lily-B: analyst persona for merchants."""
    history = get_history(req.session_id)
    history_text = format_history(history)
    full_prompt = f"{LILY_B_SYSTEM_PROMPT}\n\n{history_text}Merchant: {req.message}"

    start = monotonic()
    try:
        response = gemini.models.generate_content(
            model=MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    query_recent_chats,
                    get_demand_gaps,
                    get_handoff_queue,
                    get_sales_summary,
                ],
            ),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}")

    latency_ms = int((monotonic() - start) * 1000)
    usage = response.usage_metadata
    input_tokens = (usage.prompt_token_count if usage else 0) or 0
    output_tokens = (usage.candidates_token_count if usage else 0) or 0
    from tools.metrics import estimate_cost
    cost = estimate_cost(input_tokens, output_tokens, MODEL)

    # Robust text extraction (function calling may leave text empty)
    reply_text = response.text or ""
    if not reply_text and response.candidates:
        parts = response.candidates[0].content.parts if response.candidates[0].content else []
        text_chunks = [p.text for p in parts if getattr(p, "text", None)]
        reply_text = "".join(text_chunks).strip()
    if not reply_text:
        reply_text = "I ran the query — happy to dig deeper."

    append_to_session(req.session_id, "user", req.message)
    append_to_session(req.session_id, "assistant", reply_text)

    log_chat(
        session_id=req.session_id,
        endpoint="/analytics/chat",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        model=MODEL,
        lang="en",
        user_msg_preview=req.message,
    )

    log_event(
        user_id=None,
        user_email="merchant",
        action="analytics_query",
        target=req.session_id,
        metadata={"message_preview": req.message[:100]},
    )

    return ChatResponse(
        reply=reply_text,
        model=MODEL,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=round(cost, 6),
    )


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
            config=types.GenerateContentConfig(
                tools=[
                    lookup_order_by_email,
                    lookup_order_by_number,
                    initiate_return,
                    request_human_agent,
                    log_demand_gap,
                ],
            ),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}")

    latency_ms = int((monotonic() - start) * 1000)
    usage = response.usage_metadata
    input_tokens = (usage.prompt_token_count if usage else 0) or 0
    output_tokens = (usage.candidates_token_count if usage else 0) or 0

    from tools.metrics import estimate_cost
    cost = estimate_cost(input_tokens, output_tokens, MODEL)

    # Robust text extraction — handles thought_signature parts and function call parts
    reply_text = response.text or ""
    if not reply_text and response.candidates:
        parts = response.candidates[0].content.parts if response.candidates[0].content else []
        text_chunks = [p.text for p in parts if getattr(p, "text", None)]
        reply_text = "".join(text_chunks).strip()
    if not reply_text:
        reply_text = "I got your request — let me follow up shortly."

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
