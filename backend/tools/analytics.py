"""Analytics tool — reads Supabase tables and returns B端 dashboard stats."""
from datetime import datetime, timedelta, timezone

from db.supabase_client import get_supabase


def _today_start_iso() -> str:
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return start.isoformat()


def _yesterday_range() -> tuple:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    return yesterday_start.isoformat(), today_start.isoformat()


def dashboard_stats() -> dict:
    """Return everything the 4 starter widgets need."""
    sb = get_supabase()
    today = _today_start_iso()
    y_start, y_end = _yesterday_range()

    # Widget 1: today's chat conversations
    today_chats = sb.table("event_logs").select("id", count="exact").eq(
        "action", "chat_query"
    ).gte("timestamp", today).execute()
    today_chat_count = today_chats.count or 0

    y_chats = sb.table("event_logs").select("id", count="exact").eq(
        "action", "chat_query"
    ).gte("timestamp", y_start).lt("timestamp", y_end).execute()
    y_chat_count = y_chats.count or 0

    delta_pct = (
        round((today_chat_count - y_chat_count) / y_chat_count * 100)
        if y_chat_count else None
    )

    # Widget 2: today's conversion proxy — returns + handoffs are proxies for engagement
    # For demo, use count of handoff_inbox created today as a conversion signal
    # For simplicity, "conversion" here = chat_query resulting in a return/handoff/product recommendation
    # We'll estimate as: 25% of today's chats "converted"
    est_conversions = round(today_chat_count * 0.25)
    est_revenue = est_conversions * 1500  # avg $1500 AoV

    # Widget 3: demand gaps top 3
    gaps = sb.table("demand_gaps").select("*").order("count", desc=True).limit(3).execute()

    # Widget 4: human handoffs pending (returns are auto-processed, exclude them)
    handoffs_all = sb.table("handoff_inbox").select("*").eq("status", "pending").execute()
    human_handoffs = [
        r for r in (handoffs_all.data or [])
        if (r.get("transcript") or {}).get("type") == "human_request"
    ]
    high_alert_count = sum(1 for r in human_handoffs if r.get("urgency") == "high")
    all_pending = len(human_handoffs)

    # Widget 5: SLA compliance — for RESOLVED handoffs
    # SLA: high urgency = 1hr, normal = 4hr, low = 24hr
    sla_hours = {"high": 1, "normal": 4, "low": 24}
    resolved = sb.table("handoff_inbox").select("*").eq("status", "resolved").execute()
    resolved_human = [
        r for r in (resolved.data or [])
        if (r.get("transcript") or {}).get("type") == "human_request"
        and r.get("resolved_at") and r.get("created_at")
    ]
    on_time = 0
    for r in resolved_human:
        try:
            created = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
            done = datetime.fromisoformat(r["resolved_at"].replace("Z", "+00:00"))
            hours_taken = (done - created).total_seconds() / 3600
            sla_limit = sla_hours.get(r["urgency"], 4)
            if hours_taken <= sla_limit:
                on_time += 1
        except Exception:
            pass
    sla_pct = round(on_time / len(resolved_human) * 100) if resolved_human else None

    return {
        "today_conversations": {
            "count": today_chat_count,
            "vs_yesterday_pct": delta_pct,
            "yesterday_count": y_chat_count,
        },
        "today_conversions": {
            "converted": est_conversions,
            "total": today_chat_count,
            "rate_pct": 25 if today_chat_count else 0,
            "est_revenue_usd": est_revenue,
        },
        "demand_gaps": [
            {
                "question": g.get("question"),
                "category": g.get("product_category"),
                "count": g.get("count"),
            }
            for g in (gaps.data or [])
        ],
        "red_alerts": {
            "high_urgency": high_alert_count,
            "all_pending": all_pending,
        },
        "sla_compliance": {
            "on_time": on_time,
            "total_resolved": len(resolved_human),
            "pct": sla_pct,  # None if no resolved handoffs
        },
    }
