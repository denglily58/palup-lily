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

SYSTEM_PROMPT_ZH = (
    "你是 Lily，LUNA Beauty 美妝品牌的 AI 助理。"
    "個性專業、有品牌氣質、簡潔溫暖。"
    "回答不超過 2-3 句話。"
    "如果被問到具體商品/訂單/物流，先誠實說『這個版本還沒接資料，之後會接』。"
)

SYSTEM_PROMPT_EN = (
    "You are Lily, AI assistant for LUNA Beauty cosmetics. "
    "Be professional, on-brand, concise, warm. Keep answers to 2-3 sentences. "
    "If asked about specific products/orders/shipping, honestly say "
    "'This version doesn't have data yet, coming soon.'"
)


class ChatRequest(BaseModel):
    message: str
    lang: str = "zh"


class ChatResponse(BaseModel):
    reply: str
    model: str
    input_tokens: int
    output_tokens: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "lily-backend", "version": "0.1.0"}


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
