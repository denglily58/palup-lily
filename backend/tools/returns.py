"""Return initiation tool — Lily-C can start a return that writes to handoff_inbox."""
import uuid
from typing import Optional
from db.supabase_client import get_supabase


def initiate_return(order_number: str, reason: str, email: Optional[str] = None) -> str:
    """Initiate a return request for a specific order.

    Args:
        order_number: The order number to return (e.g., 'LUNA-1234').
        reason: Why the customer wants to return (e.g., 'wrong shade', 'allergic reaction').
        email: Optional customer email for confirmation.

    Returns:
        A confirmation message with return ID and next steps.
    """
    return_id = f"R-{uuid.uuid4().hex[:6].upper()}"

    try:
        get_supabase().table("handoff_inbox").insert({
            "session_id": None,
            "status": "pending",
            "urgency": "normal",
            "transcript": {
                "type": "return_request",
                "return_id": return_id,
                "order_number": order_number,
                "reason": reason,
                "email": email,
            },
        }).execute()
    except Exception as exc:
        return (
            f"Sorry, I couldn't file the return automatically due to a system issue. "
            f"Please email help@luna.beauty with order {order_number} and we'll process manually. "
            f"(internal error: {exc})"
        )

    return (
        f"✅ Return started for order {order_number} (reason: {reason}). "
        f"Return ID: {return_id}. "
        f"You'll receive a prepaid USPS return label via email within 24 hours. "
        f"Refund of the order total will be issued to your original payment method within 5 business days. "
        f"Free return shipping."
    )
