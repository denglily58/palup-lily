"""Seed 3 demo merchant users into Supabase Auth.

Run: cd backend && source venv/bin/activate && python scripts/seed_users.py
"""
import sys
from pathlib import Path

# Make backend/ importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from db.supabase_client import get_supabase

SEED_USERS = [
    {
        "email": "emily@luna.beauty",
        "password": "LunaDemo2026!",
        "user_metadata": {
            "name": "Emily Chen",
            "role": "E-commerce Manager",
        },
    },
    {
        "email": "david@luna.beauty",
        "password": "LunaDemo2026!",
        "user_metadata": {
            "name": "David Wang",
            "role": "Marketing Manager",
        },
    },
    {
        "email": "alex@luna.beauty",
        "password": "LunaDemo2026!",
        "user_metadata": {
            "name": "Alex Kim",
            "role": "Admin",
        },
    },
]


def main():
    supabase = get_supabase()
    for user in SEED_USERS:
        try:
            result = supabase.auth.admin.create_user({
                "email": user["email"],
                "password": user["password"],
                "email_confirm": True,  # skip confirmation for demo
                "user_metadata": user["user_metadata"],
            })
            print(f"✅ Created: {user['email']} → {user['user_metadata']['name']}")
        except Exception as exc:
            msg = str(exc)
            if "already been registered" in msg or "already exists" in msg:
                print(f"⏭  Skipped (exists): {user['email']}")
            else:
                print(f"❌ Failed: {user['email']} — {exc}")


if __name__ == "__main__":
    main()
