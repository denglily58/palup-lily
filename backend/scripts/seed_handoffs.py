"""Seed 10 fake handoffs with mixed SLA status for the demo.

Runs after Supabase tables exist. Idempotent-ish (won't clean prior test data).

Run: cd backend && source venv/bin/activate && python scripts/seed_handoffs.py
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from db.supabase_client import get_supabase

# 10 handoffs: 8 on-time, 2 overdue (< 4hr for high, < 12hr for normal weekend)
NOW = datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


HANDOFFS = [
    # 8 on-time resolved handoffs
    {
        "session_id": None,
        "status": "resolved",
        "urgency": "normal",
        "transcript": {"type": "human_request", "handoff_id": f"H-SEED-{i:03d}", "reason": r},
        "created_at": _iso(NOW - timedelta(hours=hours)),
        "resolved_at": _iso(NOW - timedelta(hours=hours - resolve_in)),
    }
    for i, (hours, resolve_in, r) in enumerate([
        (72, 2, "Asked about shade recommendation for redhead"),
        (60, 1, "Wanted to change shipping address"),
        (48, 3, "Question about vegan certification"),
        (36, 2, "Bulk order for wedding party"),
        (24, 1, "Loyalty program upgrade question"),
        (18, 2, "Product allergen check"),
        (12, 1, "International shipping question"),
        (6, 2, "Gift wrapping request"),
    ], start=1)
] + [
    # 2 overdue
    {
        "session_id": None,
        "status": "resolved",
        "urgency": "high",
        "transcript": {"type": "human_request", "handoff_id": f"H-SEED-OVERDUE-{i:03d}", "reason": r},
        "created_at": _iso(NOW - timedelta(hours=hours)),
        "resolved_at": _iso(NOW - timedelta(hours=hours - resolve_in)),
    }
    for i, (hours, resolve_in, r) in enumerate([
        (48, 8, "Package delivered damaged, angry customer"),  # 8hr resolve vs 1hr high SLA
        (24, 15, "Wrong shade sent twice, escalated"),  # 15hr resolve vs 1hr high SLA
    ], start=1)
]


def main():
    supabase = get_supabase()
    for h in HANDOFFS:
        try:
            supabase.table("handoff_inbox").insert(h).execute()
            print(f"✅ {h['transcript']['handoff_id']} — {h['urgency']} — {h['status']}")
        except Exception as exc:
            print(f"❌ {h['transcript']['handoff_id']}: {exc}")


if __name__ == "__main__":
    main()
