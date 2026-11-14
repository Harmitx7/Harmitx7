#!/usr/bin/env python3
"""
Single Master Card Renderer for Harmit Kalal (@Harmitx7).
Renders the complete editorial animated profile SVG cards:

1. cards/hero.svg                - Editorial Hero with Instrument Serif typography & vector portrait
2. cards/heatmap.svg             - 53-week contribution graph in warm cobalt editorial palette
3. cards/activity.svg            - Monthly activity chart & balanced metrics panel
4. cards/build.svg               - Signature Card 1: BUILD (tribunal-kit)
5. cards/create.svg              - Signature Card 2: CREATE (DeckReactor)
6. cards/explore.svg             - Signature Card 3: EXPLORE (ClashVision & F1 Telemetry)
7. cards/footer.svg              - Editorial colophon & verification seal

Engine Guarantees:
- Warm paper-and-ink editorial foundation with three controlled accents (Blue, Red, Yellow).
- ZERO coordinate collisions or transform-collapse bugs: all groups maintain explicit geometry.
- Embedded Base64 WOFF font subsets (Instrument Serif, Geist, Geist Mono).
- Staggered CSS animation sequence top-to-bottom.
- Full STATIC=1 support for final-frame rendering.
- Complete prefers-reduced-motion accessibility fallbacks.
- GitHub Camo compliance (< 50 KB per card, valid XML, zero external requests).
"""

import base64
import json
import os
import sys
from html import escape
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
DATA_CONTRIB = os.path.join(REPO_ROOT, "data", "contributions.json")
OUT_DIR = os.path.join(REPO_ROOT, "cards")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

# Check static mode
IS_STATIC = os.environ.get("STATIC") == "1"

# Import Editorial Typographic Hero, Monthly Activity & Contribution Calendar Generators
from scripts.generate_hero import render_hero_svg
from scripts.generate_monthly_activity import render_monthly_activity_svg, extract_monthly_data
from scripts.generate_contribution_calendar import render_contribution_calendar_svg, extract_calendar_data

# ══════════════════════════════════════════════════════════════════════════
# WARM PAPER-AND-INK EDITORIAL PALETTE (Master Reference Specification)
# ══════════════════════════════════════════════════════════════════════════
BG_BASE = "#F3F3F0"          # Warm off-white paper canvas
BG_CARD = "#F3F3F0"          # Primary editorial container paper
BG_SUBTLE = "#EAEAEC"        # Inset panel surface
BORDER_HAIRLINE = "#DEDEDA"  # 1px warm structural hairline
BORDER_FOCUS = "#C4C4C0"     # Higher contrast hairline divider
DIVIDER_LINE = "#DEDEDA"     # Metric dividers

# The Three Signature World Solid Colors
COLOR_BUILD = "#244DFF"      # Vibrant Electric Blue (01 // BUILD)
COLOR_CREATE = "#F13931"     # Vibrant Tomato Red / Crimson (02 // CREATE)
COLOR_EXPLORE = "#FDCA17"    # Warm Golden Amber / Yellow (03 // EXPLORE)

# High-contrast Editorial Typography
TEXT_PRIMARY = "#151515"     # Near-black editorial ink
TEXT_SECONDARY = "#52524C"   # Slate body text
TEXT_MUTED = "#77777D"       # Muted graphite / metadata
TEXT_FAINT = "#A0A0A5"       # Faint captions & guide rules

FONT_SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
FONT_SANS = "Geist, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

# ══════════════════════════════════════════════════════════════════════════
# FONT SUBSETTING & BASE64 EMBEDDING
# ══════════════════════════════════════════════════════════════════════════
_CACHED_FONTS: Dict[str, str] = {}


def get_embedded_fonts_css(font_keys: Optional[List[str]] = None) -> str:
    """Generate @font-face CSS rules with embedded Base64 WOFF data URIs."""
    if font_keys is None:
        font_keys = ["serif", "sans", "mono"]

    font_defs = {
        "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
        "sans": ("Geist", "normal", 400, "geist-400.woff"),
        "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
    }

    blocks = []
    for key in font_keys:
        if key not in font_defs:
            continue
        family, style, weight, filename = font_defs[key]
        if key not in _CACHED_FONTS:
            fpath = os.path.join(FONTS_DIR, filename)
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    _CACHED_FONTS[key] = base64.b64encode(f.read()).decode("ascii")
            else:
                _CACHED_FONTS[key] = ""
        b64 = _CACHED_FONTS.get(key)
        if b64:
            blocks.append(
                f"@font-face {{\n"
                f"  font-family: '{family}';\n"
                f"  font-style: {style};\n"
                f"  font-weight: {weight};\n"
                f"  src: url('data:font/woff;base64,{b64}') format('woff');\n"
                f"  font-display: swap;\n"
                f"}}"
            )
    return "\n".join(blocks)


def get_base_css(extra_css: str = "", font_keys: Optional[List[str]] = None) -> str:
    """Master stylesheet with staggered animations and reduced-motion barrier."""
    fonts_css = get_embedded_fonts_css(font_keys)

    if IS_STATIC:
        return f"""
    {fonts_css}
    * {{ animation: none !important; opacity: 1 !important; }}
    text {{ font-family: {FONT_SANS}; }}
    .serif {{ font-family: {FONT_SERIF}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    .mono {{ font-family: {FONT_MONO}; }}
    {extra_css}
"""

    return f"""
    {fonts_css}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes growBar {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}

    text {{ font-family: {FONT_SANS}; }}
    .serif {{ font-family: {FONT_SERIF}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    .mono {{ font-family: {FONT_MONO}; }}
    
    .anim-fade {{ animation: fadeIn 0.8s ease both; }}
    .anim-lift {{ animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both; }}

    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        opacity: 1 !important;
        transform: none !important;
      }}
    }}
    {extra_css}
"""


# ══════════════════════════════════════════════════════════════════════════
# 1. EDITORIAL HERO (cards/hero.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_hero_card() -> str:
    """Render 880x300 editorial hero with Instrument Serif typography and vector portrait."""
    delay_hdr = "0.05s" if not IS_STATIC else "0s"
    delay_name = "0.15s" if not IS_STATIC else "0s"
    delay_body = "0.25s" if not IS_STATIC else "0s"
    delay_portrait = "0.20s" if not IS_STATIC else "0s"

    extra_css = f"""
    .d-hdr {{ animation: fadeIn 0.5s ease {delay_hdr} both; }}
    .d-name {{ animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_name} both; }}
    .d-body {{ animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_body} both; }}
    .d-portrait {{ animation: fadeIn 0.8s ease {delay_portrait} both; }}
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 300" width="100%" height="300">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
    <linearGradient id="p-sheen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{ACCENT_BLUE}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{BG_BASE}" stop-opacity="0.8"/>
    </linearGradient>
  </defs>

  <!-- Editorial Card Canvas -->
  <rect x="1" y="1" width="878" height="298" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>

  <!-- Top Metadata Header -->
  <g class="d-hdr">
    <text x="36" y="36" fill="{TEXT_MUTED}" class="mono" font-size="11" letter-spacing="2">PORTFOLIO · 2026</text>
    <circle cx="682" cy="32" r="3.5" fill="{ACCENT_BLUE}"/>
    <text x="696" y="36" fill="{TEXT_SECONDARY}" class="mono" font-size="11" letter-spacing="1">AVAILABLE FOR CORE ROLES</text>
    <line x1="36" y1="48" x2="844" y2="48" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  </g>

  <!-- Left Content Column (Strictly x=36 to x=540 to prevent any overlap) -->
  <g class="d-name">
    <text x="36" y="106" fill="{TEXT_PRIMARY}" class="serif" font-size="52" letter-spacing="-0.5">Harmit Kalal</text>
    <text x="36" y="136" fill="{ACCENT_BLUE}" class="sans" font-size="14.5" font-weight="600" letter-spacing="0.5">AI Systems Engineer &amp; System Architect</text>
  </g>

  <g class="d-body">
    <text x="36" y="172" fill="{TEXT_SECONDARY}" class="sans" font-size="14" font-weight="400">
      Building anti-hallucination multi-agent governance and deterministic software systems.
    </text>
    <text x="36" y="194" fill="{TEXT_MUTED}" class="sans" font-size="13">
      Specializing in autonomous agent runtimes, subagent verification, and low-latency telemetry.
    </text>

    <!-- Editorial Spec Rows -->
    <line x1="36" y1="222" x2="540" y2="222" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    
    <text x="36" y="246" fill="{TEXT_MUTED}" class="mono" font-size="10.5" letter-spacing="1">PRIMARY</text>
    <text x="100" y="246" fill="{TEXT_PRIMARY}" class="sans" font-size="12">Multi-Agent Governance · Telemetry Analytics · Deception Layers</text>

    <text x="36" y="270" fill="{TEXT_MUTED}" class="mono" font-size="10.5" letter-spacing="1">ORIGIN</text>
    <text x="100" y="270" fill="{TEXT_SECONDARY}" class="sans" font-size="12">India &#160;·&#160; <tspan fill="{ACCENT_BLUE}">harmit.vercel.app</tspan> &#160;·&#160; <tspan fill="{TEXT_MUTED}">github.com/Harmitx7</tspan></text>
  </g>

  <!-- Right Column: Dedicated Architectural Vector Portrait (Starts at x=580, completely isolated) -->
  <g class="d-portrait">
    <rect x="580" y="66" width="264" height="214" rx="10" fill="{BG_BASE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    <rect x="580" y="66" width="264" height="214" rx="10" fill="url(#p-sheen)"/>

    <!-- Subtle Architectural Coordinate Framework -->
    <line x1="600" y1="92" x2="824" y2="92" stroke="{BORDER_HAIRLINE}" stroke-width="0.75" stroke-dasharray="3 3"/>
    <line x1="600" y1="210" x2="824" y2="210" stroke="{BORDER_HAIRLINE}" stroke-width="0.75" stroke-dasharray="3 3"/>
    <line x1="712" y1="80" x2="712" y2="220" stroke="{BORDER_HAIRLINE}" stroke-width="0.75" stroke-dasharray="3 3"/>

    <!-- Minimalist Handcrafted Vector Portrait Profile -->
    <g transform="translate(642, 86)">
      <!-- Head Contour & Neural Geometry -->
      <circle cx="70" cy="54" r="42" fill="none" stroke="{BORDER_FOCUS}" stroke-width="1.2"/>
      <circle cx="70" cy="54" r="32" fill="none" stroke="{ACCENT_BLUE}" stroke-width="1.5" stroke-opacity="0.8"/>
      <circle cx="70" cy="54" r="20" fill="none" stroke="{ACCENT_YELLOW}" stroke-width="1" stroke-opacity="0.6"/>

      <!-- Stylized Vector Lines (Profile & Vision Ray) -->
      <path d="M 52 46 Q 70 30 88 46 Q 96 60 84 76 Q 70 88 54 82" fill="none" stroke="{TEXT_PRIMARY}" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M 64 64 L 88 64" fill="none" stroke="{ACCENT_BLUE}" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M 88 64 L 102 52" fill="none" stroke="{ACCENT_YELLOW}" stroke-width="1.5" stroke-linecap="round"/>
      <circle cx="102" cy="52" r="3" fill="{ACCENT_YELLOW}"/>

      <!-- Base Pedestal -->
      <path d="M 38 98 Q 70 90 102 98" fill="none" stroke="{BORDER_FOCUS}" stroke-width="1.5" stroke-linecap="round"/>
    </g>

    <!-- Emblem Typography -->
    <text x="712" y="244" fill="{TEXT_PRIMARY}" class="serif" font-size="16" text-anchor="middle">Harmit Kalal</text>
    <text x="712" y="262" fill="{TEXT_MUTED}" class="mono" font-size="9.5" text-anchor="middle" letter-spacing="1.5">AI SYSTEMS ARCHITECT</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# 2. EDITORIAL CONTRIBUTION GRAPH (cards/heatmap.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_heatmap_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x258 53-week 'Every day, in blue' contribution calendar SVG."""
    cal_data = extract_calendar_data(contrib_data)
    return render_contribution_calendar_svg(cal_data, is_static=IS_STATIC)



# ══════════════════════════════════════════════════════════════════════════
# 3. MONTHLY ACTIVITY SPECTRUM (cards/activity.svg & assets/monthly-activity.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_activity_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x340 editorial monthly activity visualization SVG."""
    stats = extract_monthly_data(contrib_data)
    return render_monthly_activity_svg(stats, is_static=IS_STATIC)


# ══════════════════════════════════════════════════════════════════════════
# GLASS SHIMMER ARCHITECTURE HELPERS
# ══════════════════════════════════════════════════════════════════════════
def get_glass_card_defs(card_id: str, accent: str, w: int, h: int) -> str:
    """Generate SVG definitions for smoked glass surface, ambient glow, illuminated rim, and shimmer band."""
    return f"""
    <!-- Clip path to rounded card surface -->
    <clipPath id="card-clip-{card_id}">
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" />
    </clipPath>

    <!-- Deep Smoked Glass Surface Gradient -->
    <linearGradient id="glass-base-{card_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1B1C25" />
      <stop offset="35%" stop-color="#15161E" />
      <stop offset="100%" stop-color="#0F1016" />
    </linearGradient>

    <!-- Ambient Accent Glow -->
    <radialGradient id="ambient-glow-{card_id}" cx="14%" cy="14%" r="48%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.18" />
      <stop offset="55%" stop-color="{accent}" stop-opacity="0.04" />
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.0" />
    </radialGradient>

    <!-- Illuminated Glass Edge & Rim Light -->
    <linearGradient id="glass-rim-{card_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.65" />
      <stop offset="25%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="65%" stop-color="#FFFFFF" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.4" />
    </linearGradient>

    <!-- Diagonal Specular Shimmer Band -->
    <linearGradient id="shimmer-band-{card_id}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.0" />
      <stop offset="35%" stop-color="#FFFFFF" stop-opacity="0.02" />
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.08" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="52%" stop-color="#FFFFFF" stop-opacity="0.08" />
      <stop offset="65%" stop-color="#FFFFFF" stop-opacity="0.02" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </linearGradient>"""


def get_glass_card_css(
    card_id: str,
    accent: str,
    entrance_delay: Any = 0.30,
    shimmer_period: float = 8.5,
) -> str:
    """Generate scoped CSS for cinematic card entrance, ambient bloom, sequential content reveal, and glass shimmer."""
    if IS_STATIC:
        return f"""
    .anim-card, .glass-edge, .ambient-glow,
    .content-stagger-1, .content-stagger-2, .content-stagger-3, .content-stagger-4, .content-stagger-5 {{
      opacity: 1 !important;
      transform: none !important;
    }}
    .ambient-glow {{ opacity: 0.20 !important; }}
    .shimmer-rect {{ display: none !important; }}
    """

    if isinstance(entrance_delay, str):
        try:
            t_card = float(entrance_delay.replace("s", ""))
        except ValueError:
            t_card = 0.30
    else:
        t_card = float(entrance_delay)

    s1 = f"{t_card + 0.12:.2f}s"
    s2 = f"{t_card + 0.22:.2f}s"
    s3 = f"{t_card + 0.32:.2f}s"
    s4 = f"{t_card + 0.42:.2f}s"
    s5 = f"{t_card + 0.52:.2f}s"
    shimmer_start = f"{t_card + 0.36:.2f}s"
    bloom_start = f"{t_card:.2f}s"
    rim_start = f"{t_card:.2f}s"

    return f"""
    .anim-card {{
      animation: cardEntrance_{card_id} 0.80s cubic-bezier(0.16, 1, 0.3, 1) {t_card:.2f}s both;
    }}
    @keyframes cardEntrance_{card_id} {{
      0% {{
        opacity: 0;
        transform: translateY(28px);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    .ambient-glow {{
      animation: ambientBloom_{card_id} 1.20s ease {bloom_start} both;
    }}
    @keyframes ambientBloom_{card_id} {{
      0% {{
        opacity: 0;
      }}
      40% {{
        opacity: 0.10;
      }}
      75% {{
        opacity: 0.45;
      }}
      100% {{
        opacity: 0.20;
      }}
    }}

    .glass-edge {{
      animation: rimReveal_{card_id} 0.90s ease {rim_start} both;
    }}
    @keyframes rimReveal_{card_id} {{
      0% {{
        opacity: 0;
      }}
      70% {{
        opacity: 1;
      }}
      100% {{
        opacity: 0.85;
      }}
    }}

    @keyframes contentRise_{card_id} {{
      0% {{
        opacity: 0;
        transform: translateY(8px);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    .content-stagger-1 {{ animation: contentRise_{card_id} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {s1} both; }}
    .content-stagger-2 {{ animation: contentRise_{card_id} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {s2} both; }}
    .content-stagger-3 {{ animation: contentRise_{card_id} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {s3} both; }}
    .content-stagger-4 {{ animation: contentRise_{card_id} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {s4} both; }}
    .content-stagger-5 {{ animation: contentRise_{card_id} 0.55s cubic-bezier(0.16, 1, 0.3, 1) {s5} both; }}

    @keyframes shimmerSweep_{card_id} {{
      0% {{
        transform: rotate(26deg) translate(-280px, -140px);
        opacity: 0;
      }}
      2% {{
        opacity: 0.9;
      }}
      10% {{
        transform: rotate(26deg) translate(360px, -140px);
        opacity: 0.9;
      }}
      12%, 100% {{
        transform: rotate(26deg) translate(420px, -140px);
        opacity: 0;
      }}
    }}
    .shimmer-rect {{
      animation: shimmerSweep_{card_id} {shimmer_period}s cubic-bezier(0.16, 1, 0.3, 1) {shimmer_start} infinite;
      pointer-events: none;
    }}

    @media (hover: hover) {{
      .card-root:hover .glass-edge {{
        stroke: {accent};
        stroke-opacity: 0.80;
        filter: drop-shadow(0 0 8px {accent}40);
      }}
      .card-root:hover .ambient-glow {{
        opacity: 0.38;
      }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .anim-card, .ambient-glow, .glass-edge, .shimmer-rect,
      .content-stagger-1, .content-stagger-2, .content-stagger-3, .content-stagger-4, .content-stagger-5 {{
        animation: none !important;
        transform: none !important;
        opacity: 1 !important;
      }}
      .shimmer-rect {{ display: none !important; }}
    }}
    """


# ══════════════════════════════════════════════════════════════════════════
# 4. FLAGSHIP SYSTEMS ARCHITECTURE DECK & SIGNATURE WORLDS
# ══════════════════════════════════════════════════════════════════════════
def render_projects_deck(theme: str = "light") -> str:
    """
    Render 880x216 unified Flagship Systems Architecture Deck.
    Combines the 3 signature project domains (BUILD, CREATE, EXPLORE) into a single cohesive,
    responsive console with 2.5px top illuminated chromatic bevel tabs, preventing mobile slivers.
    """
    is_dark = (theme == "dark")
    bg_canvas = "#0D1117" if is_dark else "#F3F3F0"
    border_canvas = "#30363D" if is_dark else "#DEDEDA"
    bg_pod = "#161B22" if is_dark else "#FFFFFF"
    border_pod = "#30363D" if is_dark else "#E2E2DE"

    text_primary = "#F0F6FC" if is_dark else "#151515"
    text_secondary = "#8B949E" if is_dark else "#52524C"
    text_muted = "#6E7681" if is_dark else "#77777D"

    accent_build = "#388BFD" if is_dark else "#244DFF"
    accent_create = "#F85149" if is_dark else "#F13931"
    accent_explore = "#E3B341" if is_dark else "#D9A208"

    fonts_css = get_embedded_fonts_css(["serif", "sans", "mono"])

    anim_css = "" if IS_STATIC else """
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .anim-root { animation: fadeIn 0.7s ease both; }
    .anim-hdr { animation: fadeIn 0.5s ease 0.10s both; }
    .anim-pod-1 { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both; }
    .anim-pod-2 { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.28s both; }
    .anim-pod-3 { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.38s both; }
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 216" width="100%" height="216">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .sans {{ font-family: {FONT_SANS}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {anim_css}
      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    </style>
  </defs>

  <!-- Root Deck Canvas -->
  <g class="anim-root">
    <rect x="1" y="1" width="878" height="214" rx="16" fill="{bg_canvas}" stroke="{border_canvas}" stroke-width="1"/>
  </g>

  <!-- Header Bar -->
  <g class="anim-hdr">
    <text x="36" y="38" fill="{text_muted}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">04 // FLAGSHIP SYSTEMS ARCHITECTURE</text>
    <text x="844" y="38" fill="{text_muted}" class="mono" font-size="9.5" text-anchor="end" letter-spacing="1.2">AUTONOMOUS ENGINE MATRIX · 3 WORLDS</text>
    <line x1="36" y1="48" x2="844" y2="48" stroke="{border_canvas}" stroke-width="0.75"/>
  </g>

  <!-- ════════════ POD 1: BUILD (tribunal-kit) ════════════ -->
  <g class="anim-pod-1">
    <rect x="36" y="60" width="254" height="140" rx="10" fill="{bg_pod}" stroke="{border_pod}" stroke-width="1"/>
    <!-- Top 3px Chromatic Bevel -->
    <rect x="36" y="60" width="254" height="3" rx="1.5" fill="{accent_build}"/>
    
    <text x="54" y="86" fill="{accent_build}" class="mono" font-size="10" font-weight="600" letter-spacing="1.5">01 // BUILD</text>
    <text x="272" y="86" fill="{accent_build}" class="sans" font-size="12" font-weight="600" text-anchor="end">→</text>

    <text x="54" y="118">
      <tspan class="serif" font-size="22" font-weight="400" fill="{text_primary}">tribunal</tspan>
      <tspan class="serif" font-size="22" font-style="italic" fill="{text_primary}">-kit</tspan>
    </text>

    <text x="54" y="141" fill="{text_secondary}" class="sans" font-size="11.5">Anti-hallucination governance layer</text>
    <text x="54" y="157" fill="{text_secondary}" class="sans" font-size="11.5">for autonomous AI coding agents.</text>

    <text x="54" y="184" fill="{text_muted}" class="mono" font-size="9.5">TypeScript · Rust · MCP</text>
  </g>

  <!-- ════════════ POD 2: CREATE (DeckReactor) ════════════ -->
  <g class="anim-pod-2">
    <rect x="313" y="60" width="254" height="140" rx="10" fill="{bg_pod}" stroke="{border_pod}" stroke-width="1"/>
    <!-- Top 3px Chromatic Bevel -->
    <rect x="313" y="60" width="254" height="3" rx="1.5" fill="{accent_create}"/>

    <text x="331" y="86" fill="{accent_create}" class="mono" font-size="10" font-weight="600" letter-spacing="1.5">02 // CREATE</text>
    <text x="549" y="86" fill="{accent_create}" class="sans" font-size="12" font-weight="600" text-anchor="end">→</text>

    <text x="331" y="118">
      <tspan class="serif" font-size="22" font-weight="400" fill="{text_primary}">Deck</tspan>
      <tspan class="serif" font-size="22" font-style="italic" fill="{text_primary}">Reactor</tspan>
    </text>

    <text x="331" y="141" fill="{text_secondary}" class="sans" font-size="11.5">Dynamic canvas environments &amp;</text>
    <text x="331" y="157" fill="{text_secondary}" class="sans" font-size="11.5">generative visual developer tooling.</text>

    <text x="331" y="184" fill="{text_muted}" class="mono" font-size="9.5">React · Canvas · WebGL</text>
  </g>

  <!-- ════════════ POD 3: EXPLORE (ClashVision & F1) ════════════ -->
  <g class="anim-pod-3">
    <rect x="590" y="60" width="254" height="140" rx="10" fill="{bg_pod}" stroke="{border_pod}" stroke-width="1"/>
    <!-- Top 3px Chromatic Bevel -->
    <rect x="590" y="60" width="254" height="3" rx="1.5" fill="{accent_explore}"/>

    <text x="608" y="86" fill="{accent_explore}" class="mono" font-size="10" font-weight="600" letter-spacing="1.5">03 // EXPLORE</text>
    <text x="826" y="86" fill="{accent_explore}" class="sans" font-size="12" font-weight="600" text-anchor="end">→</text>

    <text x="608" y="118">
      <tspan class="serif" font-size="22" font-weight="400" fill="{text_primary}">ClashVision </tspan>
      <tspan class="serif" font-size="22" font-style="italic" fill="{text_primary}">&amp; F1</tspan>
    </text>

    <text x="608" y="141" fill="{text_secondary}" class="sans" font-size="11.5">Real-time tactical prediction and</text>
    <text x="608" y="157" fill="{text_secondary}" class="sans" font-size="11.5">high-frequency lap simulation.</text>

    <text x="608" y="184" fill="{text_muted}" class="mono" font-size="9.5">Python · PyTorch · DuckDB</text>
  </g>
</svg>"""
    return svg


def render_tile_build(theme: str = "light") -> str:
    """Render 286x196 signature card for BUILD (tribunal-kit)."""
    w, h = 286, 196
    is_dark = (theme == "dark")
    bg = "#161B22" if is_dark else COLOR_BUILD
    border = "#388BFD" if is_dark else "#3B62FF"
    text_color = "#F0F6FC" if is_dark else "#FFFFFF"
    accent_bar = "#388BFD" if is_dark else "#FFFFFF"
    fonts_css = get_embedded_fonts_css(["serif"])

    anim_css = "" if IS_STATIC else """
    @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .card-root { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }
    """

    bevel_bar = f'<rect x="1" y="1" width="{w-2}" height="3" rx="1.5" fill="{accent_bar}" />' if is_dark else ""

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {anim_css}
      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    </style>
  </defs>

  <g class="card-root">
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{bg}" stroke="{border}" stroke-width="1" />
    {bevel_bar}

    <text x="22" y="32" fill="{accent_bar}" class="mono" font-size="11" font-weight="600" letter-spacing="2">01 // BUILD</text>
    <text x="264" y="32" fill="{accent_bar}" class="sans" font-size="14" font-weight="600" text-anchor="end">→</text>

    <text x="22" y="86" fill="{text_color}">
      <tspan class="serif" font-size="30" font-weight="400">tribunal</tspan>
      <tspan class="serif" font-size="30" font-style="italic">-kit</tspan>
    </text>

    <text x="22" y="122" fill="{text_color}" fill-opacity="0.92" font-size="12">
      Anti-hallucination governance layer
    </text>
    <text x="22" y="140" fill="{text_color}" fill-opacity="0.92" font-size="12">
      for autonomous AI coding agents.
    </text>

    <text x="22" y="170" fill="{text_color}" fill-opacity="0.65" class="mono" font-size="10">TypeScript · Rust</text>
  </g>
</svg>"""
    return svg


def render_tile_create(theme: str = "light") -> str:
    """Render 286x196 signature card for CREATE (DeckReactor)."""
    w, h = 286, 196
    is_dark = (theme == "dark")
    bg = "#161B22" if is_dark else COLOR_CREATE
    border = "#F85149" if is_dark else "#F7524A"
    text_color = "#F0F6FC" if is_dark else "#FFFFFF"
    accent_bar = "#F85149" if is_dark else "#FFFFFF"
    fonts_css = get_embedded_fonts_css(["serif"])

    anim_css = "" if IS_STATIC else """
    @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .card-root { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.28s both; }
    """

    bevel_bar = f'<rect x="1" y="1" width="{w-2}" height="3" rx="1.5" fill="{accent_bar}" />' if is_dark else ""

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {anim_css}
      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    </style>
  </defs>

  <g class="card-root">
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{bg}" stroke="{border}" stroke-width="1" />
    {bevel_bar}

    <text x="22" y="32" fill="{accent_bar}" class="mono" font-size="11" font-weight="600" letter-spacing="2">02 // CREATE</text>
    <text x="264" y="32" fill="{accent_bar}" class="sans" font-size="14" font-weight="600" text-anchor="end">→</text>

    <text x="22" y="86" fill="{text_color}">
      <tspan class="serif" font-size="30" font-weight="400">Deck</tspan>
      <tspan class="serif" font-size="30" font-style="italic">Reactor</tspan>
    </text>

    <text x="22" y="122" fill="{text_color}" fill-opacity="0.92" font-size="12">
      Dynamic canvas environments and
    </text>
    <text x="22" y="140" fill="{text_color}" fill-opacity="0.92" font-size="12">
      generative visual developer tooling.
    </text>

    <text x="22" y="170" fill="{text_color}" fill-opacity="0.65" class="mono" font-size="10">React · SVG · Canvas</text>
  </g>
</svg>"""
    return svg


def render_tile_explore(theme: str = "light") -> str:
    """Render 286x196 signature card for EXPLORE (ClashVision & F1)."""
    w, h = 286, 196
    is_dark = (theme == "dark")
    bg = "#161B22" if is_dark else COLOR_EXPLORE
    border = "#E3B341" if is_dark else "#E5B208"
    text_color = "#F0F6FC" if is_dark else TEXT_PRIMARY
    accent_bar = "#E3B341" if is_dark else TEXT_PRIMARY
    fonts_css = get_embedded_fonts_css(["serif"])

    anim_css = "" if IS_STATIC else """
    @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .card-root { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.40s both; }
    """

    bevel_bar = f'<rect x="1" y="1" width="{w-2}" height="3" rx="1.5" fill="{accent_bar}" />' if is_dark else ""

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {anim_css}
      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    </style>
  </defs>

  <g class="card-root">
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{bg}" stroke="{border}" stroke-width="1" />
    {bevel_bar}

    <text x="22" y="32" fill="{accent_bar}" class="mono" font-size="11" font-weight="600" letter-spacing="2">03 // EXPLORE</text>
    <text x="264" y="32" fill="{accent_bar}" class="sans" font-size="14" font-weight="600" text-anchor="end">→</text>

    <text x="22" y="86" fill="{text_color}">
      <tspan class="serif" font-size="28" font-weight="400">ClashVision </tspan>
      <tspan class="serif" font-size="28" font-style="italic">&amp; F1</tspan>
    </text>

    <text x="22" y="122" fill="{text_color}" fill-opacity="0.9" font-size="12">
      Real-time tactical battle prediction
    </text>
    <text x="22" y="140" fill="{text_color}" fill-opacity="0.9" font-size="12">
      and high-frequency lap simulation.
    </text>

    <text x="22" y="170" fill="{text_color}" fill-opacity="0.65" class="mono" font-size="10">Python · PyTorch · DuckDB</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# 5. EDITORIAL COLOPHON & VERIFICATION SEAL (cards/footer.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_footer_card(theme: str = "light") -> str:
    """Render 880x72 authentic verification seal and editorial colophon."""
    is_dark = (theme == "dark")
    bg = "#0D1117" if is_dark else BG_CARD
    border = "#30363D" if is_dark else BORDER_HAIRLINE
    text_primary = "#F0F6FC" if is_dark else TEXT_PRIMARY
    text_muted = "#6E7681" if is_dark else TEXT_MUTED
    pulse_dot = "#388BFD" if is_dark else COLOR_BUILD

    fonts_css = get_embedded_fonts_css(["serif"])

    anim_css = "" if IS_STATIC else f"""
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.7; transform: scale(1); }}
      50% {{ opacity: 1.0; transform: scale(1.3); }}
    }}
    .card-root {{ animation: fadeIn 0.6s ease 0.40s both; }}
    .anim-pulse {{
      transform-origin: 594px 36px;
      animation: pulseGlow 3s ease-in-out infinite;
    }}
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 72" width="100%" height="72">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {anim_css}
      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      }}
    </style>
  </defs>

  <g class="card-root">
    <rect x="1" y="1" width="878" height="70" rx="14" fill="{bg}" stroke="{border}" stroke-width="1"/>

    <!-- Left: Identity & Mandate -->
    <text x="36" y="42" fill="{text_primary}" class="serif" font-size="20">Harmit Kalal</text>
    <text x="148" y="42" fill="{text_muted}" class="sans" font-size="12"> · AI Systems Engineer &amp; System Architect</text>

    <!-- Right: Verified Pipeline Indicator & Colophon Seal -->
    <circle cx="594" cy="38" r="3.5" fill="{pulse_dot}" class="anim-pulse"/>
    <text x="844" y="42" fill="{text_muted}" class="mono" font-size="10" text-anchor="end" letter-spacing="1.2">
      VERIFIED TELEMETRY · DETERMINISTIC PIPELINE · DAILY REFRESH
    </text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# COMPILER DISPATCHER
# ══════════════════════════════════════════════════════════════════════════
def compile_cards(out_dir: str = OUT_DIR) -> Dict[str, str]:
    """Render all editorial cards in dark and light themes into target directory."""
    os.makedirs(out_dir, exist_ok=True)
    assets_dir = os.path.join(REPO_ROOT, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Load contribution intelligence
    contrib_data: Dict[str, Any] = {}
    if os.path.exists(DATA_CONTRIB):
        with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)

    results: Dict[str, str] = {}

    for theme in ["dark", "light"]:
        # 1. Hero
        hero_content = render_hero_svg(theme=theme)
        hero_file = f"hero-{theme}.svg"
        hero_path = os.path.join(out_dir, hero_file)
        with open(hero_path, "w", encoding="utf-8") as f:
            f.write(hero_content)
        results[hero_file] = hero_path

        # 2. Heatmap / Contribution Calendar
        cal_data = extract_calendar_data(contrib_data)
        heatmap_content = render_contribution_calendar_svg(cal_data, theme=theme)
        heatmap_file = f"heatmap-{theme}.svg"
        heatmap_path = os.path.join(out_dir, heatmap_file)
        with open(heatmap_path, "w", encoding="utf-8") as f:
            f.write(heatmap_content)
        results[heatmap_file] = heatmap_path

        # 3. Monthly Activity
        stats = extract_monthly_data(contrib_data)
        activity_content = render_monthly_activity_svg(stats, theme=theme)
        activity_file = f"activity-{theme}.svg"
        activity_path = os.path.join(out_dir, activity_file)
        with open(activity_path, "w", encoding="utf-8") as f:
            f.write(activity_content)
        results[activity_file] = activity_path

        # 4. Flagship Projects Deck
        projects_content = render_projects_deck(theme=theme)
        projects_file = f"projects-{theme}.svg"
        projects_path = os.path.join(out_dir, projects_file)
        with open(projects_path, "w", encoding="utf-8") as f:
            f.write(projects_content)
        results[projects_file] = projects_path

        # 5. Standalone Tiles (BUILD, CREATE, EXPLORE)
        build_content = render_tile_build(theme=theme)
        build_file = f"build-{theme}.svg"
        build_path = os.path.join(out_dir, build_file)
        with open(build_path, "w", encoding="utf-8") as f:
            f.write(build_content)
        results[build_file] = build_path

        create_content = render_tile_create(theme=theme)
        create_file = f"create-{theme}.svg"
        create_path = os.path.join(out_dir, create_file)
        with open(create_path, "w", encoding="utf-8") as f:
            f.write(create_content)
        results[create_file] = create_path

        explore_content = render_tile_explore(theme=theme)
        explore_file = f"explore-{theme}.svg"
        explore_path = os.path.join(out_dir, explore_file)
        with open(explore_path, "w", encoding="utf-8") as f:
            f.write(explore_content)
        results[explore_file] = explore_path

        # 6. Colophon / Footer
        footer_content = render_footer_card(theme=theme)
        footer_file = f"footer-{theme}.svg"
        footer_path = os.path.join(out_dir, footer_file)
        with open(footer_path, "w", encoding="utf-8") as f:
            f.write(footer_content)
        results[footer_file] = footer_path

        # Default fallback files (light theme copies for legacy markdown viewers)
        if theme == "light":
            defaults = {
                "hero.svg": hero_content,
                "heatmap.svg": heatmap_content,
                "activity.svg": activity_content,
                "projects.svg": projects_content,
                "build.svg": build_content,
                "create.svg": create_content,
                "explore.svg": explore_content,
                "footer.svg": footer_content,
            }
            for d_name, d_content in defaults.items():
                d_path = os.path.join(out_dir, d_name)
                with open(d_path, "w", encoding="utf-8") as f:
                    f.write(d_content)
                results[d_name] = d_path

            # Mirror to assets
            with open(os.path.join(assets_dir, "monthly-activity.svg"), "w", encoding="utf-8") as f:
                f.write(activity_content)
            with open(os.path.join(assets_dir, "contribution-calendar.svg"), "w", encoding="utf-8") as f:
                f.write(heatmap_content)
            with open(os.path.join(assets_dir, "hero.svg"), "w", encoding="utf-8") as f:
                f.write(hero_content)

    for fname, fpath in results.items():
        size_kb = os.path.getsize(fpath) / 1024
        print(f"✔ Rendered {fname:<24} ({size_kb:4.1f} KB) -> {fpath}")

    return results


if __name__ == "__main__":
    compile_cards(OUT_DIR)
