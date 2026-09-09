"""Order lookup tool — Lily-C can find customer orders by email or order number."""
import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

SEED_DIR = Path(__file__).parent.parent.parent / "seed"


@lru_cache(maxsize=1)
def _load_orders() -> list:
    with open(SEED_DIR / "orders.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_shipping() -> dict:
    with open(SEED_DIR / "shipping_rules.json") as f:
        return json.load(f)


def _format_order(order: dict) -> str:
    items_str = ", ".join(
        f"{i['product_id']} shade {i['shade_code']} x{i['qty']} (${i['price']})"
        for i in order["items"]
    )
    zone = order.get("shipping_zone", "unknown")
    return (
        f"Order {order['order_number']} for {order['customer_name']} ({order['email']}) — "
        f"Status: {order['status'].upper()} — "
        f"Items: {items_str} — "
        f"Total: ${order['total']} — "
        f"Placed: {order['created_at']} — "
        f"ETA: {order.get('shipping_eta', 'N/A')} — "
        f"Tracking: {order.get('tracking_no', 'not yet assigned')} — "
        f"Ships to: {zone}"
    )


def lookup_order_by_email(email: str) -> str:
    """Look up all recent orders for a customer email address.

    Args:
        email: The customer's email address (e.g., 'sarah.johnson@gmail.com').

    Returns:
        A summary of all orders for that email, or a message if none found.
    """
    email_lower = email.strip().lower()
    matches = [o for o in _load_orders() if o["email"].lower() == email_lower]
    if not matches:
        return f"No orders found for {email}."
    matches.sort(key=lambda o: o["created_at"], reverse=True)
    lines = [f"Found {len(matches)} order(s) for {email}:"]
    for o in matches:
        lines.append(f"  - {_format_order(o)}")
    return "\n".join(lines)


def lookup_order_by_number(order_number: str) -> str:
    """Look up a specific order by its order number.

    Args:
        order_number: The order number (e.g., 'LUNA-1234' or '1234').

    Returns:
        The order details, or a message if not found.
    """
    normalized = order_number.strip().upper().replace("LUNA-", "")
    matches = [
        o for o in _load_orders()
        if o["order_number"].upper().endswith(normalized)
    ]
    if not matches:
        return f"No order found with number {order_number}."
    return _format_order(matches[0])
