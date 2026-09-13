"""Supabase client — server-side (uses service_role key, bypasses RLS)."""
import os
from functools import lru_cache
from typing import Optional

from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_KEY"]
    return create_client(url, key)


def log_event(
    user_id: Optional[str],
    user_email: Optional[str],
    action: str,
    target: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> None:
    """Insert a row into event_logs. Non-blocking (fails silently to not break user flow)."""
    try:
        row = {
            "user_id": user_id,
            "user_email": user_email,
            "action": action,
            "target": target,
            "metadata": metadata or {},
        }
        get_supabase().table("event_logs").insert(row).execute()
    except Exception as exc:  # noqa: BLE001 — intentional: log failures must not break user flow
        print(f"[event_log] Failed to write: {exc}")


def recent_events(limit: int = 50) -> list:
    """Fetch recent events for B端 activity log."""
    try:
        result = (
            get_supabase()
            .table("event_logs")
            .select("*")
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception as exc:
        print(f"[event_log] Failed to fetch: {exc}")
        return []
