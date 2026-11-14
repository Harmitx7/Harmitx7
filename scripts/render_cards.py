#!/usr/bin/env python3
"""
Single Master Card Renderer for Harmit Kalal (@Harmitx7).
Renders the complete editorial animated profile SVG cards:

1. cards/hero.svg                - Editorial Hero with Instrument Serif typography & vector portrait
2. cards/heatmap.svg             - 53-week contribution graph in warm cobalt editorial palette
3. cards/activity.svg            - Monthly activity chart & balanced metrics panel
4. cards/build.svg               - Signature World 1: BUILD (tribunal-kit)
5. cards/create.svg              - Signature World 2: CREATE (DeckReactor & Labs)
6. cards/explore.svg             - Signature World 3: EXPLORE (ClashVision & F1 Telemetry)
7. cards/secure.svg              - Drop-in alias for backward compatibility
8. cards/simulate.svg            - Drop-in alias for backward compatibility
9. cards/repo-tribunal-kit.svg   - Featured repository 1
10. cards/repo-clashvision.svg   - Featured repository 2
11. cards/repo-f1-telemetry.svg  - Featured repository 3
12. cards/footer.svg             - Editorial colophon & verification seal

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
# WARM PAPER-AND-INK EDITORIAL PALETTE (Blue · Red · Yellow Triad)
# ══════════════════════════════════════════════════════════════════════════
BG_BASE = "#111215"          # Dark warm charcoal paper canvas
BG_CARD = "#16171D"          # Primary editorial card paper
BG_SUBTLE = "#1C1D24"        # Inset panel paper surface
BORDER_HAIRLINE = "#262832"  # 1px warm structural rule
BORDER_FOCUS = "#3A3C4A"     # Higher contrast hairline divider

# The Three Controlled Accents
ACCENT_BLUE = "#3B82F6"      # Editorial Cobalt (BUILD, primary focus, code)
ACCENT_RED = "#EF4444"       # Editorial Carmine (EXPLORE, research, telemetry)
ACCENT_YELLOW = "#F59E0B"    # Warm Amber / Ochre (CREATE, peaks, interactive)

# Warm Typography
TEXT_PRIMARY = "#F5F3EF"     # Warm bone / ivory ink
TEXT_SECONDARY = "#C4C0B6"   # Warm sand / parchment body
TEXT_MUTED = "#7D7A73"       # Muted graphite / metadata
TEXT_FAINT = "#4A4843"       # Faint captions & guide rules

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
# 4. THREE SIGNATURE WORLDS (cards/build.svg, cards/create.svg, cards/explore.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_tile_build() -> str:
    """Render 286x250 editorial glass tile for BUILD (tribunal-kit & AI Governance)."""
    w, h = 286, 250
    card_id = "tile-build"
    accent = ACCENT_BLUE
    entrance_delay = 0.28 if not IS_STATIC else 0.0
    extra_css = get_glass_card_css(card_id, accent, entrance_delay=entrance_delay, shimmer_period=8.2)
    defs_content = get_glass_card_defs(card_id, accent, w, h)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
    {defs_content}
  </defs>

  <g class="anim-card card-root">
    <!-- Base Glass Surface with Depth Clipping -->
    <g clip-path="url(#card-clip-{card_id})">
      <!-- Smoked Glass Body -->
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glass-base-{card_id})" />

      <!-- Subtle Ambient Lighting -->
      <rect class="ambient-glow" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#ambient-glow-{card_id})" />

      <!-- Top Inner Glass Highlight Rule -->
      <line x1="12" y1="2" x2="{w-12}" y2="2" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1" />

      <!-- Moving Diagonal Shimmer Sweep -->
      <rect class="shimmer-rect" x="-250" y="-150" width="180" height="550" fill="url(#shimmer-band-{card_id})" />
    </g>

    <!-- Outer Illuminated Glass Edge -->
    <rect class="glass-edge" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="none" stroke="url(#glass-rim-{card_id})" stroke-width="1" />
    
    <!-- 1. Top Category & Accent Pill + Vector Motif -->
    <g class="content-stagger-1">
      <text x="22" y="32" fill="{accent}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">01 // BUILD</text>
      <circle cx="260" cy="28" r="4" fill="{accent}"/>

      <!-- Minimalist Vector Motif: Directed Neural Agent Graph -->
      <g transform="translate(22, 46)">
        <rect x="0" y="0" width="44" height="44" rx="8" fill="#14151D" stroke="#262835" stroke-width="1"/>
        <circle cx="14" cy="14" r="3.5" fill="{accent}"/>
        <circle cx="30" cy="14" r="3" fill="{TEXT_MUTED}"/>
        <circle cx="22" cy="30" r="4" fill="{TEXT_PRIMARY}"/>
        <line x1="14" y1="14" x2="30" y2="14" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.7"/>
        <line x1="14" y1="14" x2="22" y2="30" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.7"/>
        <line x1="30" y1="14" x2="22" y2="30" stroke="{BORDER_FOCUS}" stroke-width="1.2"/>
      </g>
    </g>

    <!-- 2. Project Title -->
    <g class="content-stagger-2">
      <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">tribunal-kit</text>
    </g>

    <!-- 3. Subtitle -->
    <g class="content-stagger-3">
      <text x="22" y="142" fill="{accent}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">MULTI-AGENT GOVERNANCE</text>
    </g>
    
    <!-- 4. Description -->
    <g class="content-stagger-4">
      <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        Anti-hallucination governance layer
      </text>
      <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        for autonomous AI coding agents.
      </text>
    </g>

    <!-- 5. Bottom Metadata Row -->
    <g class="content-stagger-5">
      <line x1="22" y1="208" x2="264" y2="208" stroke="#262834" stroke-width="1"/>
      <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">TypeScript · Rust</text>
      <text x="264" y="228" fill="{accent}" class="sans" font-size="11" font-weight="600" text-anchor="end">Explore →</text>
    </g>
  </g>
</svg>"""
    return svg


def render_tile_create() -> str:
    """Render 286x250 editorial glass tile for CREATE (Design & Visual Systems)."""
    w, h = 286, 250
    card_id = "tile-create"
    accent = ACCENT_YELLOW
    entrance_delay = 0.44 if not IS_STATIC else 0.0
    extra_css = get_glass_card_css(card_id, accent, entrance_delay=entrance_delay, shimmer_period=8.7)
    defs_content = get_glass_card_defs(card_id, accent, w, h)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
    {defs_content}
  </defs>

  <g class="anim-card card-root">
    <!-- Base Glass Surface with Depth Clipping -->
    <g clip-path="url(#card-clip-{card_id})">
      <!-- Smoked Glass Body -->
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glass-base-{card_id})" />

      <!-- Subtle Ambient Lighting -->
      <rect class="ambient-glow" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#ambient-glow-{card_id})" />

      <!-- Top Inner Glass Highlight Rule -->
      <line x1="12" y1="2" x2="{w-12}" y2="2" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1" />

      <!-- Moving Diagonal Shimmer Sweep -->
      <rect class="shimmer-rect" x="-250" y="-150" width="180" height="550" fill="url(#shimmer-band-{card_id})" />
    </g>

    <!-- Outer Illuminated Glass Edge -->
    <rect class="glass-edge" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="none" stroke="url(#glass-rim-{card_id})" stroke-width="1" />
    
    <!-- 1. Top Category & Accent Pill + Vector Motif -->
    <g class="content-stagger-1">
      <text x="22" y="32" fill="{accent}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">02 // CREATE</text>
      <circle cx="260" cy="28" r="4" fill="{accent}"/>

      <!-- Minimalist Vector Motif: Generative Harmonic Curve -->
      <g transform="translate(22, 46)">
        <rect x="0" y="0" width="44" height="44" rx="8" fill="#14151D" stroke="#262835" stroke-width="1"/>
        <path d="M 10 32 Q 22 8 34 32" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round"/>
        <circle cx="22" cy="18" r="3" fill="{TEXT_PRIMARY}"/>
      </g>
    </g>

    <!-- 2. Project Title -->
    <g class="content-stagger-2">
      <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">DeckReactor</text>
    </g>

    <!-- 3. Subtitle -->
    <g class="content-stagger-3">
      <text x="22" y="142" fill="{accent}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">CREATIVE LABS &amp; SYSTEMS</text>
    </g>
    
    <!-- 4. Description -->
    <g class="content-stagger-4">
      <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        Dynamic canvas environments and
      </text>
      <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        generative visual developer tooling.
      </text>
    </g>

    <!-- 5. Bottom Metadata Row -->
    <g class="content-stagger-5">
      <line x1="22" y1="208" x2="264" y2="208" stroke="#262834" stroke-width="1"/>
      <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">React · SVG · Canvas</text>
      <text x="264" y="228" fill="{accent}" class="sans" font-size="11" font-weight="600" text-anchor="end">Visit Lab →</text>
    </g>
  </g>
</svg>"""
    return svg


def render_tile_explore() -> str:
    """Render 286x250 editorial glass tile for EXPLORE (RL Policy & Telemetry)."""
    w, h = 286, 250
    card_id = "tile-explore"
    accent = ACCENT_RED
    entrance_delay = 0.60 if not IS_STATIC else 0.0
    extra_css = get_glass_card_css(card_id, accent, entrance_delay=entrance_delay, shimmer_period=9.2)
    defs_content = get_glass_card_defs(card_id, accent, w, h)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
    {defs_content}
  </defs>

  <g class="anim-card card-root">
    <!-- Base Glass Surface with Depth Clipping -->
    <g clip-path="url(#card-clip-{card_id})">
      <!-- Smoked Glass Body -->
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glass-base-{card_id})" />

      <!-- Subtle Ambient Lighting -->
      <rect class="ambient-glow" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#ambient-glow-{card_id})" />

      <!-- Top Inner Glass Highlight Rule -->
      <line x1="12" y1="2" x2="{w-12}" y2="2" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1" />

      <!-- Moving Diagonal Shimmer Sweep -->
      <rect class="shimmer-rect" x="-250" y="-150" width="180" height="550" fill="url(#shimmer-band-{card_id})" />
    </g>

    <!-- Outer Illuminated Glass Edge -->
    <rect class="glass-edge" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="none" stroke="url(#glass-rim-{card_id})" stroke-width="1" />
    
    <!-- 1. Top Category & Accent Pill + Vector Motif -->
    <g class="content-stagger-1">
      <text x="22" y="32" fill="{accent}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">03 // EXPLORE</text>
      <circle cx="260" cy="28" r="4" fill="{accent}"/>

      <!-- Minimalist Vector Motif: Telemetry Lap Trace Wave -->
      <g transform="translate(22, 46)">
        <rect x="0" y="0" width="44" height="44" rx="8" fill="#14151D" stroke="#262835" stroke-width="1"/>
        <path d="M 8 26 L 16 14 L 24 30 L 32 10 L 38 20" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>

    <!-- 2. Project Title -->
    <g class="content-stagger-2">
      <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">ClashVision &amp; F1</text>
    </g>

    <!-- 3. Subtitle -->
    <g class="content-stagger-3">
      <text x="22" y="142" fill="{accent}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">RL POLICY &amp; TELEMETRY</text>
    </g>
    
    <!-- 4. Description -->
    <g class="content-stagger-4">
      <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        Real-time tactical battle prediction
      </text>
      <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
        and high-frequency lap simulation.
      </text>
    </g>

    <!-- 5. Bottom Metadata Row -->
    <g class="content-stagger-5">
      <line x1="22" y1="208" x2="264" y2="208" stroke="#262834" stroke-width="1"/>
      <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">Python · PyTorch · DuckDB</text>
      <text x="264" y="228" fill="{accent}" class="sans" font-size="11" font-weight="600" text-anchor="end">Inspect →</text>
    </g>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# 5. FEATURED REPOSITORIES (cards/repo-*.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_repo_card(
    repo_name: str,
    tagline: str,
    description_l1: str,
    description_l2: str,
    language: str,
    stars: int,
    forks: int,
    meta_tag: str,
    accent: str,
    card_id: str,
    entrance_delay: Any = 0.30,
    shimmer_period: float = 8.5,
) -> str:
    """Render 286x210 editorial project card with smoked glass appearance and cinematic staggered reveal."""
    w, h = 286, 210
    extra_css = get_glass_card_css(card_id, accent, entrance_delay=entrance_delay, shimmer_period=shimmer_period)
    defs_content = get_glass_card_defs(card_id, accent, w, h)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
    {defs_content}
  </defs>

  <g class="anim-card card-root">
    <!-- Base Glass Surface with Depth Clipping -->
    <g clip-path="url(#card-clip-{card_id})">
      <!-- Smoked Glass Body -->
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glass-base-{card_id})" />

      <!-- Subtle Ambient Lighting -->
      <rect class="ambient-glow" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#ambient-glow-{card_id})" />

      <!-- Top Inner Glass Highlight Rule -->
      <line x1="12" y1="2" x2="{w-12}" y2="2" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1" />

      <!-- Moving Diagonal Shimmer Sweep -->
      <rect class="shimmer-rect" x="-250" y="-150" width="180" height="550" fill="url(#shimmer-band-{card_id})" />
    </g>

    <!-- Outer Illuminated Glass Edge -->
    <rect class="glass-edge" x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="none" stroke="url(#glass-rim-{card_id})" stroke-width="1" />

    <!-- 1. Top Metadata Bar -->
    <g class="content-stagger-1">
      <g transform="translate(20, 20)">
        <!-- Language Pill -->
        <circle cx="5" cy="8" r="3.5" fill="{accent}"/>
        <text x="14" y="12" fill="{TEXT_MUTED}" class="mono" font-size="10">{language}</text>

        <!-- Stars and Forks -->
        <text x="244" y="12" fill="{TEXT_MUTED}" class="mono" font-size="10" text-anchor="end">
          ★ {stars} &#160;·&#160; ⑂ {forks}
        </text>
      </g>
    </g>

    <!-- 2. Repository Title -->
    <g class="content-stagger-2">
      <text x="20" y="66" fill="{TEXT_PRIMARY}" class="serif" font-size="21">{repo_name}</text>
    </g>

    <!-- 3. Subtitle / Tagline -->
    <g class="content-stagger-3">
      <text x="20" y="84" fill="{accent}" class="sans" font-size="10.5" font-weight="600" letter-spacing="0.5">{tagline}</text>
    </g>

    <!-- 4. Description -->
    <g class="content-stagger-4">
      <text x="20" y="112" fill="{TEXT_SECONDARY}" class="sans" font-size="12">{description_l1}</text>
      <text x="20" y="128" fill="{TEXT_SECONDARY}" class="sans" font-size="12">{description_l2}</text>
    </g>

    <!-- 5. Divider & Quick Start / Action Link -->
    <g class="content-stagger-5">
      <line x1="20" y1="152" x2="264" y2="152" stroke="#262834" stroke-width="1"/>
      <text x="20" y="180" fill="{TEXT_MUTED}" class="mono" font-size="10">{meta_tag}</text>
      <text x="264" y="180" fill="{TEXT_PRIMARY}" class="sans" font-size="11" font-weight="600" text-anchor="end">View Code →</text>
    </g>
  </g>
</svg>"""
    return svg


def render_repo_tribunal_kit() -> str:
    return render_repo_card(
        repo_name="tribunal-kit",
        tagline="MULTI-AGENT AI GOVERNANCE",
        description_l1="Universal governance layer for AI coding",
        description_l2="agents with zero hallucination enforcement.",
        language="TypeScript / Rust",
        stars=6,
        forks=1,
        meta_tag="npm i -g tribunal-kit",
        accent=ACCENT_BLUE,
        card_id="repo-tribunal",
        entrance_delay=0.30 if not IS_STATIC else 0.0,
        shimmer_period=8.2,
    )


def render_repo_clashvision() -> str:
    return render_repo_card(
        repo_name="ClashVision v3.0",
        tagline="RL BATTLE POLICY ENGINE",
        description_l1="Real-time tactical battle predictor and",
        description_l2="deep Q-network reinforcement policy.",
        language="Python / PyTorch",
        stars=2,
        forks=0,
        meta_tag="Kaggle Season 18 Dataset",
        accent=ACCENT_YELLOW,
        card_id="repo-clashvision",
        entrance_delay=0.46 if not IS_STATIC else 0.0,
        shimmer_period=8.7,
    )


def render_repo_f1_telemetry() -> str:
    return render_repo_card(
        repo_name="F1-TELEMETRY",
        tagline="LAP ANALYTICS DASHBOARD",
        description_l1="Formula 1 high-frequency telemetry traces",
        description_l2="and deterministic lap comparison engine.",
        language="Python / FastAPI",
        stars=0,
        forks=0,
        meta_tag="DuckDB · FastEngine",
        accent=ACCENT_RED,
        card_id="repo-f1",
        entrance_delay=0.62 if not IS_STATIC else 0.0,
        shimmer_period=9.2,
    )


# ══════════════════════════════════════════════════════════════════════════
# 6. EDITORIAL FOOTER & COLOPHON (cards/footer.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_footer_card() -> str:
    """Render 880x100 restrained editorial closing colophon."""
    delay = "1.05s" if not IS_STATIC else "0s"
    extra_css = f".d-foot {{ animation: fadeIn 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 100" width="100%" height="100">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
  </defs>

  <g class="d-foot">
    <rect x="1" y="1" width="878" height="98" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>

    <!-- Colophon Content -->
    <text x="36" y="38" fill="{TEXT_PRIMARY}" class="serif" font-size="18">Harmit Kalal</text>
    <text x="146" y="38" fill="{TEXT_MUTED}" class="sans" font-size="12">&#160;·&#160; AI Systems Engineer &amp; System Architect</text>

    <text x="844" y="38" fill="{TEXT_MUTED}" class="mono" font-size="10.5" text-anchor="end">
      HANDCRAFTED SVG ENGINE &#160;·&#160; 0 THIRD-PARTY WIDGETS
    </text>

    <line x1="36" y1="52" x2="844" y2="52" stroke="{BORDER_HAIRLINE}" stroke-width="0.75"/>

    <!-- Navigation / Social Links Inside Card -->
    <text x="36" y="78" fill="{ACCENT_BLUE}" class="mono" font-size="11">harmit.vercel.app</text>
    <text x="190" y="78" fill="{TEXT_MUTED}" class="mono" font-size="11">github.com/Harmitx7</text>
    <text x="350" y="78" fill="{TEXT_MUTED}" class="mono" font-size="11">linkedin.com/in/harmitkalal</text>
    <text x="560" y="78" fill="{TEXT_MUTED}" class="mono" font-size="11">harmitkalal7@gmail.com</text>

    <text x="844" y="78" fill="{TEXT_MUTED}" class="mono" font-size="10.5" text-anchor="end">
      AUTOMATED DAILY REFRESH
    </text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# COMPILER DISPATCHER
# ══════════════════════════════════════════════════════════════════════════
def compile_cards(out_dir: str = OUT_DIR) -> Dict[str, str]:
    """Render all editorial cards into target directory."""
    os.makedirs(out_dir, exist_ok=True)

    # Load contribution intelligence
    contrib_data: Dict[str, Any] = {}
    if os.path.exists(DATA_CONTRIB):
        with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)

    renderers = {
        "hero.svg": render_hero_svg(),
        "heatmap.svg": render_heatmap_card(contrib_data),
        "activity.svg": render_activity_card(contrib_data),
        # Three Signature Worlds
        "build.svg": render_tile_build(),
        "create.svg": render_tile_create(),
        "explore.svg": render_tile_explore(),
        # Featured Repositories
        "repo-tribunal-kit.svg": render_repo_tribunal_kit(),
        "repo-clashvision.svg": render_repo_clashvision(),
        "repo-f1-telemetry.svg": render_repo_f1_telemetry(),
        # Editorial Colophon
        "footer.svg": render_footer_card(),
    }

    results: Dict[str, str] = {}
    for name, content in renderers.items():
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = len(content.encode("utf-8")) / 1024
        print(f"✔ Rendered {name:<26} ({size_kb:4.1f} KB) -> {path}")
        results[name] = path

    # Also mirror monthly activity to assets/monthly-activity.svg
    assets_path = os.path.join(REPO_ROOT, "assets", "monthly-activity.svg")
    os.makedirs(os.path.dirname(assets_path), exist_ok=True)
    with open(assets_path, "w", encoding="utf-8") as f:
        f.write(renderers["activity.svg"])

    # Also mirror contribution calendar to assets/contribution-calendar.svg
    calendar_asset_path = os.path.join(REPO_ROOT, "assets", "contribution-calendar.svg")
    with open(calendar_asset_path, "w", encoding="utf-8") as f:
        f.write(renderers["heatmap.svg"])

    return results


if __name__ == "__main__":
    compile_cards(OUT_DIR)
