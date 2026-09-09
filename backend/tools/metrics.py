"""Metrics tool — token/cost/latency logging for Q7 evidence.

Simple v0: append JSONL to backend/logs/chat_logs.jsonl
Later: migrate to Supabase chat_logs table (Task #17 timeframe).
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "chat_logs.jsonl"

# Gemini 3.6 Flash pricing per 1M tokens (from Google AI Studio 2026-09)
# Free tier: within 15 req/min, 1500 req/day, 1M tokens/min
# Paid tier (if exceeded):
COST_PER_1M_INPUT = 0.075   # USD
COST_PER_1M_OUTPUT = 0.30   # USD


def estimate_cost(input_tokens: int, output_tokens: int, model: str = "gemini-3.6-flash") -> float:
    """Return USD cost estimate (as-if paid tier, even if we're free)."""
    if "flash" in model:
        return (input_tokens / 1_000_000) * COST_PER_1M_INPUT + \
               (output_tokens / 1_000_000) * COST_PER_1M_OUTPUT
    return 0.0


def log_chat(
    session_id: Optional[str],
    endpoint: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    model: str,
    lang: str,
    user_msg_preview: str = "",
) -> None:
    """Append one JSONL row per /chat call."""
    LOG_DIR.mkdir(exist_ok=True)
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "endpoint": endpoint,
        "model": model,
        "lang": lang,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "latency_ms": latency_ms,
        "cost_usd": round(estimate_cost(input_tokens, output_tokens, model), 6),
        "user_msg_preview": user_msg_preview[:100],
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_all_logs() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE) as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate() -> dict:
    """Return aggregate metrics for /metrics endpoint and B端 dashboard widget."""
    logs = read_all_logs()
    if not logs:
        return {
            "total_conversations": 0,
            "total_tokens": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost_usd": 0.0,
            "avg_latency_ms": 0,
            "by_model": {},
            "by_lang": {},
        }

    total_in = sum(r["input_tokens"] for r in logs)
    total_out = sum(r["output_tokens"] for r in logs)
    total_cost = sum(r["cost_usd"] for r in logs)
    avg_latency = sum(r["latency_ms"] for r in logs) // len(logs)

    by_model = {}
    by_lang = {}
    for r in logs:
        by_model[r["model"]] = by_model.get(r["model"], 0) + 1
        by_lang[r["lang"]] = by_lang.get(r["lang"], 0) + 1

    return {
        "total_conversations": len(logs),
        "total_tokens": total_in + total_out,
        "total_input_tokens": total_in,
        "total_output_tokens": total_out,
        "total_cost_usd": round(total_cost, 6),
        "avg_latency_ms": avg_latency,
        "by_model": by_model,
        "by_lang": by_lang,
    }
