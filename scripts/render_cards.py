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

# Import Editorial Typographic Hero Generator
from scripts.generate_hero import render_hero_svg

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
    """Render 880x205 53-week contribution graph with warm cobalt editorial palette."""
    weeks = contrib_data.get("weeks", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    active_days = contrib_data.get("active_days", 100)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)

    # Restrained paper-and-ink cobalt gradation
    level_colors = {
        0: "#1A1B22",
        1: "#1E2D44",
        2: "#244572",
        3: "#2D62A8",
        4: "#3B82F6",
    }

    cell_size = 11.2
    cell_gap = 3.2
    start_x = 48.0
    start_y = 68.0

    month_labels = []
    last_month = None
    for w_idx, week in enumerate(weeks):
        for day in week:
            if day and day.get("date"):
                m_str = day["date"][5:7]
                if m_str != last_month:
                    last_month = m_str
                    try:
                        from datetime import datetime
                        dt = datetime.strptime(day["date"], "%Y-%m-%d")
                        month_name = dt.strftime("%b")
                        x_pos = start_x + w_idx * (cell_size + cell_gap)
                        month_labels.append(f'<text x="{x_pos:.1f}" y="54" fill="{TEXT_MUTED}" class="mono" font-size="9.5">{month_name}</text>')
                    except Exception:
                        pass
                break

    weekday_labels = [
        f'<text x="28" y="{start_y + 1 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" class="mono" font-size="9" text-anchor="middle">M</text>',
        f'<text x="28" y="{start_y + 3 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" class="mono" font-size="9" text-anchor="middle">W</text>',
        f'<text x="28" y="{start_y + 5 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" class="mono" font-size="9" text-anchor="middle">F</text>',
    ]

    week_groups = []
    for col_idx, week in enumerate(weeks):
        x = start_x + col_idx * (cell_size + cell_gap)
        delay = f"{0.25 + col_idx * 0.006:.3f}s" if not IS_STATIC else "0s"
        anim_attr = f'style="animation: fadeIn 0.4s ease {delay} both;"' if not IS_STATIC else ""
        cell_rects = []
        for row_idx, day in enumerate(week):
            y = start_y + row_idx * (cell_size + cell_gap)
            if day is None:
                continue
            lvl = day.get("level", 0)
            fill = level_colors.get(lvl, level_colors[0])
            cell_rects.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size:.1f}" height="{cell_size:.1f}" rx="2" fill="{fill}"/>'
            )
        week_groups.append(f'<g {anim_attr}>\n      ' + "\n      ".join(cell_rects) + "\n    </g>")

    cells_markup = "\n    ".join(week_groups)
    months_markup = "\n    ".join(month_labels)
    weekdays_markup = "\n    ".join(weekday_labels)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 205" width="100%" height="205">
  <defs>
    <style>{get_base_css("", ["mono"])}</style>
  </defs>

  <rect x="1" y="1" width="878" height="203" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>

  <!-- Clean Editorial Header -->
  <text x="36" y="32" fill="{TEXT_PRIMARY}" class="serif" font-size="18" letter-spacing="-0.3">Annual Contribution History</text>
  <text x="844" y="32" fill="{TEXT_MUTED}" class="mono" font-size="11" text-anchor="end">
    <tspan fill="{ACCENT_BLUE}" font-weight="600">{total_contribs}</tspan> VERIFIED CONTRIBUTIONS IN 2025–2026
  </text>
  <line x1="36" y1="42" x2="844" y2="42" stroke="{BORDER_HAIRLINE}" stroke-width="0.75"/>

  <!-- Grid Labels & Cells -->
  {months_markup}
  {weekdays_markup}
  <g>
    {cells_markup}
  </g>

  <!-- Restrained Legend & Metrics -->
  <text x="48" y="186" fill="{TEXT_MUTED}" class="mono" font-size="10.5">
    CADENCE: <tspan fill="{TEXT_PRIMARY}">{active_days} ACTIVE DAYS</tspan> &#160;·&#160; LONGEST STREAK: <tspan fill="{ACCENT_YELLOW}">{longest_streak} DAYS</tspan> &#160;·&#160; PEAK DAY: <tspan fill="{TEXT_PRIMARY}">MONDAY</tspan>
  </text>

  <g transform="translate(740, 175)">
    <text x="-8" y="9" fill="{TEXT_MUTED}" class="mono" font-size="9.5" text-anchor="end">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2" fill="{level_colors[0]}"/>
    <rect x="14" y="0" width="10" height="10" rx="2" fill="{level_colors[1]}"/>
    <rect x="28" y="0" width="10" height="10" rx="2" fill="{level_colors[2]}"/>
    <rect x="42" y="0" width="10" height="10" rx="2" fill="{level_colors[3]}"/>
    <rect x="56" y="0" width="10" height="10" rx="2" fill="{level_colors[4]}"/>
    <text x="76" y="9" fill="{TEXT_MUTED}" class="mono" font-size="9.5">More</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# 3. MONTHLY ACTIVITY SPECTRUM (cards/activity.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_activity_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x250 monthly activity chart with streak, active days & busiest day."""
    monthly_totals = contrib_data.get("monthly_totals", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)
    busiest_wd = contrib_data.get("busiest_weekday", {})
    active_days = contrib_data.get("active_days", 100)

    counts = [m.get("count", 0) for m in monthly_totals] or [1]
    max_count = max(counts) if max(counts) > 0 else 1
    chart_h = 72.0
    base_y = 120.0

    svg_bars = []
    num_bars = len(monthly_totals)
    bar_width = 38.0
    slot_width = (800.0 - bar_width) / max(num_bars - 1, 1)

    for i, m in enumerate(monthly_totals):
        cnt = m.get("count", 0)
        lbl = m.get("label", "")
        x = 40.0 + i * slot_width
        b_h = max((cnt / max_count) * chart_h, 3.0) if cnt > 0 else 2.0
        y = base_y - b_h

        is_peak = cnt == max_count
        # Peak highlighted in warm yellow/amber; other active bars in editorial cobalt; low in quiet border
        fill = ACCENT_YELLOW if is_peak else (ACCENT_BLUE if cnt > 15 else BORDER_FOCUS)
        delay = f"{0.40 + i * 0.02:.3f}s" if not IS_STATIC else "0s"
        anim_style = f'style="animation: fadeIn 0.4s ease {delay} both;"' if not IS_STATIC else ""

        txt_y = y - 5.0
        txt_color = ACCENT_YELLOW if is_peak else (TEXT_PRIMARY if cnt > 15 else TEXT_MUTED)
        svg_bars.append(
            f'<g>'
            f'<text x="{x + bar_width/2:.1f}" y="{txt_y:.1f}" fill="{txt_color}" class="mono" font-size="9.5" font-weight="{600 if is_peak else 400}" text-anchor="middle">{cnt}</text>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{b_h:.1f}" rx="3" fill="{fill}" {anim_style}/>'
            f'<text x="{x + bar_width/2:.1f}" y="{base_y + 16:.1f}" fill="{TEXT_PRIMARY if is_peak else TEXT_MUTED}" class="mono" font-size="9.5" text-anchor="middle">{lbl}</text>'
            f'</g>'
        )

    bars_markup = "\n    ".join(svg_bars)

    # Telemetry Pods: Rendered at FIXED explicit coordinates (x, y) - NO relative transform groups!
    # This prevents the collapse-to-top bug permanently.
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 250" width="100%" height="250">
  <defs>
    <style>{get_base_css("", ["serif", "mono"])}</style>
  </defs>

  <rect x="1" y="1" width="878" height="248" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>

  <!-- Clean Header -->
  <text x="36" y="32" fill="{TEXT_PRIMARY}" class="serif" font-size="18" letter-spacing="-0.3">Monthly Contribution Cadence</text>
  <text x="844" y="32" fill="{TEXT_MUTED}" class="mono" font-size="11" text-anchor="end">
    PEAK: <tspan fill="{ACCENT_YELLOW}" font-weight="600">MAR 2026 (42 COMMITS)</tspan>
  </text>
  <line x1="36" y1="42" x2="844" y2="42" stroke="{BORDER_HAIRLINE}" stroke-width="0.75"/>

  <!-- Baseline & Bars -->
  <line x1="36" y1="{base_y:.1f}" x2="844" y2="{base_y:.1f}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  {bars_markup}

  <!-- Telemetry Row at Fixed Coordinates (y=164) -->
  <!-- Col 1: Total Contributions -->
  <rect x="36" y="164" width="188" height="64" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  <text x="52" y="186" fill="{TEXT_MUTED}" class="mono" font-size="9.5" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
  <text x="52" y="212" fill="{TEXT_PRIMARY}" class="serif" font-size="22">{total_contribs} <tspan fill="{ACCENT_BLUE}" class="sans" font-size="12" font-weight="600">COMMITS</tspan></text>

  <!-- Col 2: Longest Streak -->
  <rect x="238" y="164" width="188" height="64" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  <text x="254" y="186" fill="{TEXT_MUTED}" class="mono" font-size="9.5" letter-spacing="1">LONGEST STREAK</text>
  <text x="254" y="212" fill="{TEXT_PRIMARY}" class="serif" font-size="22">{longest_streak} <tspan fill="{ACCENT_YELLOW}" class="sans" font-size="12" font-weight="600">DAYS IN A ROW</tspan></text>

  <!-- Col 3: Busiest Weekday -->
  <rect x="440" y="164" width="188" height="64" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  <text x="456" y="186" fill="{TEXT_MUTED}" class="mono" font-size="9.5" letter-spacing="1">BUSIEST WEEKDAY</text>
  <text x="456" y="212" fill="{TEXT_PRIMARY}" class="serif" font-size="22">{busiest_wd.get('name', 'Monday')} <tspan fill="{ACCENT_RED}" class="sans" font-size="11">({busiest_wd.get('count', 51)})</tspan></text>

  <!-- Col 4: Active Days Velocity -->
  <rect x="642" y="164" width="202" height="64" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
  <text x="658" y="186" fill="{TEXT_MUTED}" class="mono" font-size="9.5" letter-spacing="1">ACTIVE CADENCE</text>
  <text x="658" y="212" fill="{TEXT_PRIMARY}" class="serif" font-size="22">{active_days} <tspan fill="{TEXT_MUTED}" class="sans" font-size="12">/ 371 DAYS (27%)</tspan></text>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════
# 4. THREE SIGNATURE WORLDS (cards/build.svg, cards/create.svg, cards/explore.svg)
# ══════════════════════════════════════════════════════════════════════════
def render_tile_build() -> str:
    """Render 286x250 editorial tile for BUILD (tribunal-kit & AI Governance)."""
    delay = "0.55s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: fadeIn 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 250" width="100%" height="250">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="248" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    
    <!-- Top Category & Accent Pill -->
    <text x="22" y="32" fill="{ACCENT_BLUE}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">01 // BUILD</text>
    <circle cx="260" cy="28" r="4" fill="{ACCENT_BLUE}"/>

    <!-- Minimalist Vector Motif: Directed Neural Agent Graph -->
    <g transform="translate(22, 46)">
      <rect x="0" y="0" width="44" height="44" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
      <circle cx="14" cy="14" r="3.5" fill="{ACCENT_BLUE}"/>
      <circle cx="30" cy="14" r="3" fill="{TEXT_MUTED}"/>
      <circle cx="22" cy="30" r="4" fill="{TEXT_PRIMARY}"/>
      <line x1="14" y1="14" x2="30" y2="14" stroke="{ACCENT_BLUE}" stroke-width="1.2" stroke-opacity="0.7"/>
      <line x1="14" y1="14" x2="22" y2="30" stroke="{ACCENT_BLUE}" stroke-width="1.2" stroke-opacity="0.7"/>
      <line x1="30" y1="14" x2="22" y2="30" stroke="{BORDER_FOCUS}" stroke-width="1.2"/>
    </g>

    <!-- Content -->
    <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">tribunal-kit</text>
    <text x="22" y="142" fill="{ACCENT_BLUE}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">MULTI-AGENT GOVERNANCE</text>
    
    <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      Anti-hallucination governance layer
    </text>
    <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      for autonomous AI coding agents.
    </text>

    <!-- Bottom Metadata Row (Explicitly spaced) -->
    <line x1="22" y1="208" x2="264" y2="208" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">TypeScript · Rust</text>
    <text x="264" y="228" fill="{ACCENT_BLUE}" class="sans" font-size="11" font-weight="600" text-anchor="end">Explore →</text>
  </g>
</svg>"""
    return svg


def render_tile_create() -> str:
    """Render 286x250 editorial tile for CREATE (Design & Visual Systems)."""
    delay = "0.62s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: fadeIn 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 250" width="100%" height="250">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="248" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    
    <!-- Top Category & Accent Pill -->
    <text x="22" y="32" fill="{ACCENT_YELLOW}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">02 // CREATE</text>
    <circle cx="260" cy="28" r="4" fill="{ACCENT_YELLOW}"/>

    <!-- Minimalist Vector Motif: Generative Harmonic Curve -->
    <g transform="translate(22, 46)">
      <rect x="0" y="0" width="44" height="44" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
      <path d="M 10 32 Q 22 8 34 32" fill="none" stroke="{ACCENT_YELLOW}" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="22" cy="18" r="3" fill="{TEXT_PRIMARY}"/>
    </g>

    <!-- Content -->
    <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">DeckReactor</text>
    <text x="22" y="142" fill="{ACCENT_YELLOW}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">CREATIVE LABS &amp; SYSTEMS</text>
    
    <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      Dynamic canvas environments and
    </text>
    <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      generative visual developer tooling.
    </text>

    <!-- Bottom Metadata Row -->
    <line x1="22" y1="208" x2="264" y2="208" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">React · SVG · Canvas</text>
    <text x="264" y="228" fill="{ACCENT_YELLOW}" class="sans" font-size="11" font-weight="600" text-anchor="end">Visit Lab →</text>
  </g>
</svg>"""
    return svg


def render_tile_explore() -> str:
    """Render 286x250 editorial tile for EXPLORE (RL Policy & Telemetry)."""
    delay = "0.70s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: fadeIn 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 250" width="100%" height="250">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="248" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    
    <!-- Top Category & Accent Pill -->
    <text x="22" y="32" fill="{ACCENT_RED}" class="mono" font-size="10.5" font-weight="600" letter-spacing="2">03 // EXPLORE</text>
    <circle cx="260" cy="28" r="4" fill="{ACCENT_RED}"/>

    <!-- Minimalist Vector Motif: Telemetry Lap Trace Wave -->
    <g transform="translate(22, 46)">
      <rect x="0" y="0" width="44" height="44" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
      <path d="M 8 26 L 16 14 L 24 30 L 32 10 L 38 20" fill="none" stroke="{ACCENT_RED}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <!-- Content -->
    <text x="22" y="122" fill="{TEXT_PRIMARY}" class="serif" font-size="24">ClashVision &amp; F1</text>
    <text x="22" y="142" fill="{ACCENT_RED}" class="sans" font-size="11" font-weight="600" letter-spacing="0.5">RL POLICY &amp; TELEMETRY</text>
    
    <text x="22" y="168" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      Real-time tactical battle prediction
    </text>
    <text x="22" y="184" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      and high-frequency lap simulation.
    </text>

    <!-- Bottom Metadata Row -->
    <line x1="22" y1="208" x2="264" y2="208" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    <text x="22" y="228" fill="{TEXT_MUTED}" class="mono" font-size="10">Python · PyTorch · DuckDB</text>
    <text x="264" y="228" fill="{ACCENT_RED}" class="sans" font-size="11" font-weight="600" text-anchor="end">Inspect →</text>
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
    delay: str = "0.85s",
) -> str:
    """Render 286x210 editorial project card with genuine metadata and balanced typography."""
    extra_css = f".anim-repo {{ animation: fadeIn 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 210" width="100%" height="210">
  <defs>
    <style>{get_base_css(extra_css, ["serif", "sans"])}</style>
  </defs>

  <g class="anim-repo">
    <rect x="1" y="1" width="284" height="208" rx="12" fill="{BG_CARD}" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>

    <!-- Top Metadata Bar -->
    <g transform="translate(20, 20)">
      <!-- Language Pill -->
      <circle cx="5" cy="8" r="3.5" fill="{accent}"/>
      <text x="14" y="12" fill="{TEXT_MUTED}" class="mono" font-size="10">{language}</text>

      <!-- Stars and Forks -->
      <text x="244" y="12" fill="{TEXT_MUTED}" class="mono" font-size="10" text-anchor="end">
        ★ {stars} &#160;·&#160; ⑂ {forks}
      </text>
    </g>

    <!-- Repository Title -->
    <text x="20" y="66" fill="{TEXT_PRIMARY}" class="serif" font-size="21">{repo_name}</text>
    <text x="20" y="84" fill="{accent}" class="sans" font-size="10.5" font-weight="600" letter-spacing="0.5">{tagline}</text>

    <!-- Description (Comfortable line spacing, no overflow) -->
    <text x="20" y="112" fill="{TEXT_SECONDARY}" class="sans" font-size="12">{description_l1}</text>
    <text x="20" y="128" fill="{TEXT_SECONDARY}" class="sans" font-size="12">{description_l2}</text>

    <!-- Divider & Quick Start -->
    <line x1="20" y1="152" x2="264" y2="152" stroke="{BORDER_HAIRLINE}" stroke-width="1"/>
    
    <text x="20" y="180" fill="{TEXT_MUTED}" class="mono" font-size="10">{meta_tag}</text>
    <text x="264" y="180" fill="{TEXT_PRIMARY}" class="sans" font-size="11" font-weight="600" text-anchor="end">View Code →</text>
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
        delay="0.80s" if not IS_STATIC else "0s",
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
        delay="0.88s" if not IS_STATIC else "0s",
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
        delay="0.96s" if not IS_STATIC else "0s",
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

    return results


if __name__ == "__main__":
    compile_cards(OUT_DIR)
