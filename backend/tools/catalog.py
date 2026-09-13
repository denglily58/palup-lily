"""Catalog tool — load LUNA Beauty seed data and format for LLM context.

Simple v0 approach: inject full catalog + top reviews into system prompt.
Later can upgrade to embedding-based retrieval when catalog >100 SKU.
"""
import json
from functools import lru_cache
from pathlib import Path

_backend_seed = Path(__file__).parent.parent / "seed"
_project_seed = Path(__file__).parent.parent.parent / "seed"
SEED_DIR = _backend_seed if _backend_seed.exists() else _project_seed


@lru_cache(maxsize=1)
def load_products() -> list[dict]:
    with open(SEED_DIR / "products.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_reviews() -> list[dict]:
    with open(SEED_DIR / "reviews.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_shipping() -> dict:
    with open(SEED_DIR / "shipping_rules.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_policies() -> dict:
    with open(SEED_DIR / "policies.json") as f:
        return json.load(f)


def top_reviews_for_product(product_id: str, limit: int = 3) -> list[dict]:
    reviews = [r for r in load_reviews() if r["product_id"] == product_id]
    reviews.sort(key=lambda r: r["rating"], reverse=True)
    return reviews[:limit]


def format_catalog_markdown(lang: str = "en") -> str:
    """Format catalog + top reviews as markdown for LLM context."""
    products = load_products()
    lines = ["## LUNA Beauty Product Catalog", ""]

    for p in products:
        name = p["name_en"] if lang == "en" else p["name_zh"]
        desc = p["description_en"] if lang == "en" else p["description_zh"]
        shades_txt = ", ".join(
            f"{s['code']} {s['name_en'] if lang == 'en' else s['name_zh']} (undertone: {s['undertone']}, stock: {s['stock']})"
            for s in p["shades"]
        )
        lines.append(f"### {name} [{p['sku']}] — ${p['price']}")
        lines.append(f"- Category: {p['category']} / {p['subcategory']}")
        lines.append(f"- Description: {desc}")
        lines.append(f"- Shades: {shades_txt}")
        lines.append(f"- Tags: {', '.join(p['tags'])}")

        reviews = top_reviews_for_product(p["id"])
        if reviews:
            lines.append("- Top reviews:")
            for r in reviews:
                text = r["text_en"] if lang == "en" else r["text_zh"]
                lines.append(f'  - ★{r["rating"]} "{text}" — {r["author"]}')
        lines.append("")

    return "\n".join(lines)


def format_shipping_markdown(lang: str = "en") -> str:
    s = load_shipping()
    lines = ["## Shipping Info"]
    lines.append(f"- Free shipping over ${s['free_shipping_over']} USD")
    lines.append("- Zones (ETA / fee):")
    for z in s["zones"]:
        name = z["name_en"] if lang == "en" else z["name_zh"]
        lines.append(f"  - {name}: {z['eta_days']} days / ${z['fee']}")
    lines.append(f"- Cutoff: {s['notes']['cutoff_time_en' if lang == 'en' else 'cutoff_time_zh']}")
    return "\n".join(lines)


def format_policies_markdown(lang: str = "en") -> str:
    p = load_policies()
    lines = ["## Policies"]
    r = p["returns"]
    lines.append(f"- Returns: {r['window_days']}-day window, free return shipping")
    lines.append(f"  Conditions: {r['conditions_en' if lang == 'en' else 'conditions_zh']}")
    lines.append("- Promos:")
    for promo in p["promotions"]:
        name = promo["name_en"] if lang == "en" else promo["name_zh"]
        lines.append(f"  - {promo['code']}: {name}")
    lines.append(f"- Loyalty: {p['loyalty_program']['name_en']} (3 tiers)")
    return "\n".join(lines)


def full_context(lang: str = "en") -> str:
    """Assemble full context for Lily-C system prompt."""
    return "\n\n".join([
        format_catalog_markdown(lang),
        format_shipping_markdown(lang),
        format_policies_markdown(lang),
    ])
