"""Handoff tool — Lily-C transfers buyer to human agent via handoff_inbox."""
import uuid
from typing import Optional
from db.supabase_client import get_supabase


def request_human_agent(
    reason: Optional[str] = None,
    email: Optional[str] = None,
    urgency: str = "normal",
) -> str:
    """Transfer this conversation to a human customer service agent.

    Use this ONLY when the buyer explicitly asks for a human, is upset,
    or has a complex issue you cannot resolve (e.g. complaint about wrong
    item received, dispute, sensitive account matter).

    Args:
        reason: Short summary of why the transfer is needed.
        email: Optional buyer email so the human can follow up.
        urgency: One of 'low', 'normal', 'high'. Use 'high' for complaints or upset customers.

    Returns:
        A message telling the buyer they're being transferred and expected response time.
    """
    handoff_id = f"H-{uuid.uuid4().hex[:6].upper()}"
    try:
        get_supabase().table("handoff_inbox").insert({
            "session_id": None,
            "status": "pending",
            "urgency": urgency,
            "transcript": {
                "type": "human_request",
                "handoff_id": handoff_id,
                "reason": reason or "buyer requested human",
                "email": email,
            },
        }).execute()
    except Exception as exc:
        return (
            f"I'm having trouble connecting you right now. "
            f"Please email help@luna.beauty and mention this issue. (error: {exc})"
        )

    sla = {
        "high": "within 1 hour during business hours (Mon-Fri 9am-6pm PT)",
        "normal": "within 4 business hours (Mon-Fri 9am-6pm PT)",
        "low": "within 24 hours",
    }.get(urgency, "within 4 business hours")

    return (
        f"✅ Connecting you to our team now (Handoff ID: {handoff_id}). "
        f"A human agent will respond {sla}. "
        f"Anything urgent you'd like me to note for them?"
    )


def log_demand_gap(question: str, product_category: Optional[str] = None) -> str:
    """Log that a buyer asked for a product LUNA doesn't currently carry.

    Use this when the buyer asks for something we don't sell (e.g. sunscreen, hair care,
    a specific undertone we don't offer). Do NOT make up products.

    Args:
        question: The buyer's original question, verbatim if possible.
        product_category: A short category tag (e.g. 'sunscreen', 'hair_care', 'brow_pen_asian_tone').

    Returns:
        Confirmation that the demand was noted internally.
    """
    supabase = get_supabase()
    try:
        # Try upsert-style: if same category exists, increment; else insert.
        existing = (
            supabase.table("demand_gaps")
            .select("id, count")
            .eq("product_category", product_category or "")
            .execute()
        )
        if existing.data:
            row = existing.data[0]
            supabase.table("demand_gaps").update({
                "count": row["count"] + 1,
                "last_asked": "now()",
            }).eq("id", row["id"]).execute()
        else:
            supabase.table("demand_gaps").insert({
                "question": question,
                "product_category": product_category,
                "count": 1,
            }).execute()
    except Exception as exc:
        print(f"[demand_gap] Failed: {exc}")

    return "Noted for our product team — thank you for the suggestion!"
