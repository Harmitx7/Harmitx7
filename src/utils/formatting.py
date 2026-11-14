"""Text formatting, number formatting, XML escaping, and unique ID utilities."""

import html
import re
from typing import Set

_REGISTERED_IDS: Set[str] = set()


def reset_id_registry() -> None:
    """Reset registered IDs (useful across test runs or clean generator passes)."""
    global _REGISTERED_IDS
    _REGISTERED_IDS.clear()


def generate_unique_id(prefix: str, name: str) -> str:
    """
    Generate an XML/SVG safe unique ID that avoids collisions across SVGs.
    Ensures alphanumeric and underscore characters only.
    """
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    candidate = f"{prefix}_{clean_name}"
    counter = 1
    final_id = candidate
    while final_id in _REGISTERED_IDS:
        final_id = f"{candidate}_{counter}"
        counter += 1
    _REGISTERED_IDS.add(final_id)
    return final_id


def escape_xml(text: str) -> str:
    """Escape XML special characters (&, <, >, ', \")."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def truncate_text(text: str, max_chars: int, suffix: str = "...") -> str:
    """Truncate text safely with an ellipsis suffix."""
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len(suffix)].rstrip() + suffix


def format_bytes(bytes_count: int) -> str:
    """Format bytes count into human-readable string (KB, MB, GB)."""
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_count / (1024 * 1024 * 1024):.2f} GB"


def format_number(val: int) -> str:
    """Format integer with thousands separator commas."""
    return f"{val:,}"


def format_percentage(val: float, decimals: int = 1) -> str:
    """Format float into percentage string."""
    return f"{val:.{decimals}f}%"
