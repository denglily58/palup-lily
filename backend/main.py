"""LUNA × Lily — FastAPI backend entry point."""
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel

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


class ChatResponse(BaseModel):
    reply: str
    model: str
    input_tokens: int
    output_tokens: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "lily-backend", "version": "0.2.0"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    system = SYSTEM_PROMPT_ZH if req.lang == "zh" else SYSTEM_PROMPT_EN
    try:
        response = gemini.models.generate_content(
            model=MODEL,
            contents=f"{system}\n\nUser: {req.message}",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}")

    usage = response.usage_metadata
    return ChatResponse(
        reply=response.text or "",
        model=MODEL,
        input_tokens=(usage.prompt_token_count if usage else 0) or 0,
        output_tokens=(usage.candidates_token_count if usage else 0) or 0,
    )
