"""Prompt loader — reads versioned markdown prompts with YAML frontmatter.

This is the runtime source of truth. Editing a prompt md file
(and restarting backend) rotates the agent's behavior.

Frontmatter is parsed but currently only used for logging/debugging.
"""
from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split '---\\n<yaml>\\n---\\n<body>' into ({}, body). Manual parse — avoids yaml dep."""
    if not text.startswith("---\n"):
        return {}, text.strip()
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text.strip()
    fm_raw, body = parts[1], parts[2]
    fm: dict = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body.strip()


@lru_cache(maxsize=8)
def load_prompt(name: str) -> tuple[dict, str]:
    """Load a prompt md file by name. Returns (frontmatter dict, body string).

    Example: load_prompt('lily_c_en_v1') → ({'version': '1.0.0', ...}, 'You are Lily...')
    """
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    fm, body = _parse_frontmatter(path.read_text())
    return fm, body


def get_prompt(agent: str, lang: str = "en") -> str:
    """Convenience: resolve current active prompt for an agent.

    Currently hardcoded to v1. Later can read from registry.yaml.
    """
    key = f"{agent}_{lang}_v1"
    _fm, body = load_prompt(key)
    return body
