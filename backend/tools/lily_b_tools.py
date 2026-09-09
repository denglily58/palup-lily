"""Lily-B tools — read event_logs / handoff_inbox / demand_gaps / orders for merchant analytics."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from db.supabase_client import get_supabase

SEED_DIR = Path(__file__).parent.parent.parent / "seed"


def query_recent_chats(hours: int = 24, keyword_filter: Optional[str] = None) -> str:
    """Query buyer chat events from the last N hours, optionally filtered by keyword.

    Use this to answer questions like 'what did buyers ask about today', 'this week', or
    'chats mentioning sensitive skin'.

    Args:
        hours: Look-back window in hours (24 = today, 168 = 7 days).
        keyword_filter: Optional substring to filter message_preview by (case-insensitive).

    Returns:
        JSON string with a list of chat events (timestamp, message preview, session_id, tokens).
    """
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        result = (
            get_supabase()
            .table("event_logs")
            .select("*")
            .eq("action", "chat_query")
            .gte("timestamp", since)
            .order("timestamp", desc=True)
            .limit(50)
            .execute()
        )
    except Exception as exc:
        return f"Error querying: {exc}"

    events = result.data or []
    if keyword_filter:
        kw = keyword_filter.lower()
        events = [
            e for e in events
            if kw in (e.get("metadata") or {}).get("message_preview", "").lower()
        ]

    summary = [
        {
            "timestamp": e["timestamp"],
            "message": (e.get("metadata") or {}).get("message_preview", ""),
            "lang": (e.get("metadata") or {}).get("lang"),
            "session_id": e.get("target"),
        }
        for e in events
    ]
    return json.dumps({
        "period_hours": hours,
        "filter": keyword_filter,
        "count": len(summary),
        "chats": summary,
    })


def get_demand_gaps(limit: int = 10) -> str:
    """Get product demand gaps buyers have asked for but LUNA doesn't sell.

    Use this to answer 'what should we consider adding to our product line'.

    Args:
        limit: Max number of gaps to return, ordered by frequency descending.

    Returns:
        JSON string with list of demand gaps and their ask counts.
    """
    try:
        result = (
            get_supabase()
            .table("demand_gaps")
            .select("*")
            .order("count", desc=True)
            .limit(limit)
            .execute()
        )
        return json.dumps({"gaps": result.data or []})
    except Exception as exc:
        return f"Error: {exc}"


def get_handoff_queue(status: str = "pending") -> str:
    """Get customer-service handoffs matching the given status.

    Use this to answer 'what needs human follow-up' or 'any urgent issues today'.

    Args:
        status: One of 'pending', 'in_progress', 'resolved'.

    Returns:
        JSON string with matching handoff records (includes reason, urgency, timestamps).
    """
    try:
        result = (
            get_supabase()
            .table("handoff_inbox")
            .select("*")
            .eq("status", status)
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
        return json.dumps({"status": status, "count": len(result.data or []), "queue": result.data or []})
    except Exception as exc:
        return f"Error: {exc}"


def get_sales_summary() -> str:
    """Get aggregate sales stats from seed orders (30 orders across last 30 days).

    Use this to answer 'how much are we selling', 'what's our AoV', 'top products'.

    Returns:
        JSON string with total orders, revenue, AoV, status breakdown, top products.
    """
    with open(SEED_DIR / "orders.json") as f:
        orders = json.load(f)

    total_revenue = sum(o["total"] for o in orders)
    aov = total_revenue / len(orders) if orders else 0

    status_counts: dict = {}
    for o in orders:
        status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1

    product_revenue: dict = {}
    for o in orders:
        for item in o["items"]:
            pid = item["product_id"]
            product_revenue[pid] = product_revenue.get(pid, 0) + item["price"] * item["qty"]
    top_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:5]

    return json.dumps({
        "total_orders": len(orders),
        "total_revenue_usd": total_revenue,
        "aov_usd": round(aov, 2),
        "by_status": status_counts,
        "top_products_by_revenue": [{"product_id": p, "revenue_usd": r} for p, r in top_products],
    })
