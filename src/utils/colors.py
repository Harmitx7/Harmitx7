"""Design system color tokens and color utility functions."""

from typing import Tuple

# Surface & Canvas Palettes
COLOR_BG_VOID = "#05070B"
COLOR_BG_SURFACE = "#0C1017"
COLOR_BG_ELEVATED = "#141B26"
COLOR_BG_OVERLAY = "#1A2332"

# Direction D: Signature Hybrid (Editorial Cyber-Glass) Palettes
# ── Dark Mode Matrix (GitHub #0D1117 Harmony) ──
DARK_BG_BASE = "#0D1117"
DARK_BG_CARD = "#161B22"
DARK_BG_SUBTLE = "#21262D"
DARK_BORDER_HAIRLINE = "#30363D"
DARK_BORDER_FOCUS = "#8B949E"
DARK_TEXT_PRIMARY = "#F0F6FC"
DARK_TEXT_SECONDARY = "#8B949E"
DARK_TEXT_MUTED = "#6E7681"
DARK_TEXT_FAINT = "#484F58"

# ── Light Mode Matrix (Warm Paper-and-Ink) ──
LIGHT_BG_BASE = "#F3F3F0"
LIGHT_BG_CARD = "#F3F3F0"
LIGHT_BG_SUBTLE = "#EAEAEC"
LIGHT_BORDER_HAIRLINE = "#DEDEDA"
LIGHT_BORDER_FOCUS = "#C4C4C0"
LIGHT_TEXT_PRIMARY = "#151515"
LIGHT_TEXT_SECONDARY = "#52524C"
LIGHT_TEXT_MUTED = "#77777D"
LIGHT_TEXT_FAINT = "#A0A0A5"

# ── The Three Signature World Solid & Accent Colors ──
COLOR_BUILD = "#244DFF"      # Vibrant Electric Blue (01 // BUILD)
COLOR_CREATE = "#F13931"     # Vibrant Tomato Red / Crimson (02 // CREATE)
COLOR_EXPLORE = "#FDCA17"    # Warm Golden Amber / Yellow (03 // EXPLORE)

# Borders & Structure
COLOR_BORDER_SUBTLE = "#1E293B"
COLOR_BORDER_MUTED = "#0F172A"
COLOR_BORDER_CYAN = "#00F0FF"
COLOR_BORDER_AMBER = "#FF6B00"

# Text & Foreground
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_SECONDARY = "#CBD5E1"
COLOR_TEXT_MUTED = "#64748B"
COLOR_TEXT_FAINT = "#334155"

# Semantic Accents
COLOR_ACCENT_CYAN = "#00F0FF"
COLOR_ACCENT_SKY = "#38BDF8"
COLOR_ACCENT_MINT = "#00E676"
COLOR_ACCENT_TANGERINE = "#FF6B00"
COLOR_ACCENT_AMBER = "#FBBF24"
COLOR_ACCENT_CORAL = "#F43F5E"
COLOR_ACCENT_PURPLE = "#A855F7"

# Verified Language Colors
LANGUAGE_COLORS = {
    "JavaScript": "#F7DF1E",
    "Python": "#3572A5",
    "TypeScript": "#3178C6",
    "Java": "#B07219",
    "Rust": "#DEA584",
    "CSS": "#563D7C",
    "HTML": "#E34C26",
    "Kotlin": "#A97BFF",
    "Shell": "#89E051",
    "Other": "#64748B",
}


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hex color string (#RRGGBB) to (r, g, b) tuple."""
    hex_clean = hex_code.lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return (r, g, b)


def rgba_str(hex_code: str, opacity: float) -> str:
    """Return rgba(r, g, b, opacity) string."""
    r, g, b = hex_to_rgb(hex_code)
    return f"rgba({r}, {g}, {b}, {opacity:.2f})"


def get_language_color(lang_name: str) -> str:
    """Return corresponding hex color for programming language."""
    return LANGUAGE_COLORS.get(lang_name, LANGUAGE_COLORS["Other"])
