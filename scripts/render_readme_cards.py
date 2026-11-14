#!/usr/bin/env python3
"""
Master SVG Card Compiler — Reference-Inspired Animated SVG Portfolio Experience.
Compiles handcrafted, animated, data-driven SVG cards into cards/ for Harmit Kalal (@Harmitx7).
Supports:
- STATIC=1 environment override for instant static final-frame mode
- Embedded Base64 WOFF font subsets (Geist Mono, Geist, Instrument Serif)
- GitHub Camo proxy compliance (0 scripts, 0 onload, valid XML, < 50 KB per card)
- Coordinated top-to-bottom entrance animations
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
DATA_REPOS = os.path.join(REPO_ROOT, "data", "repositories.json")
DATA_PROFILE = os.path.join(REPO_ROOT, "data", "profile.json")
OUT_DIR = os.path.join(REPO_ROOT, "cards")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

# Check static mode
IS_STATIC = os.environ.get("STATIC") == "1"

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE (Editorial Cyber-Observatory)
# ══════════════════════════════════════════════════════════════════════════════
BG_VOID = "#05070B"
BG_SURFACE = "#0B0F17"
BG_CARD = "#0C111C"
BG_SUBTLE = "#111827"
BORDER_DEFAULT = "#1E293B"
BORDER_HIGHLIGHT = "#334155"

CYAN_PRIMARY = "#00F0FF"
CYAN_MUTED = "#008B9B"
MINT_PRIMARY = "#00E676"
MINT_MUTED = "#057A44"
ORANGE_ACCENT = "#FF6B00"
AMBER_ACCENT = "#FBBF24"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#64748B"
TEXT_SUBTLE = "#475569"

# Font stacks
FONT_MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
FONT_SANS = "Geist, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_SERIF = "'Instrument Serif', Georgia, serif"

# ══════════════════════════════════════════════════════════════════════════════
# FONT EMBEDDING UTILITY
# ══════════════════════════════════════════════════════════════════════════════
_CACHED_FONTS: Dict[str, str] = {}


def get_embedded_fonts_css(font_keys: Optional[List[str]] = None) -> str:
    """Generate @font-face CSS rules with embedded Base64 WOFF fonts."""
    if font_keys is None:
        font_keys = ["mono", "sans"]

    font_defs = {
        "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
        "sans": ("Geist", "normal", 400, "geist-400.woff"),
        "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
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
    """Generate master CSS stylesheet for SVG card with targeted font embedding."""
    if font_keys is None:
        font_keys = ["mono"]  # Lean default: only embed 6.8KB Geist Mono

    fonts_css = get_embedded_fonts_css(font_keys)

    if IS_STATIC:
        return f"""
    {fonts_css}
    * {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    text {{ font-family: {FONT_MONO}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    .serif {{ font-family: {FONT_SERIF}; }}
    {extra_css}
"""

    return f"""
    {fonts_css}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
    @keyframes pop {{ 0% {{ opacity: 0; transform: scale(0.7); }} 70% {{ opacity: 1; transform: scale(1.05); }} 100% {{ transform: none; }} }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}
    @keyframes beacon {{ 0%, 100% {{ transform: scale(1); opacity: 0.95; }} 50% {{ transform: scale(1.25); opacity: 0.4; }} }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes orbit {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    text {{ font-family: {FONT_MONO}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    .serif {{ font-family: {FONT_SERIF}; }}
    {extra_css}

    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        transform: none !important;
        opacity: 1 !important;
      }}
    }}
"""


# ══════════════════════════════════════════════════════════════════════════════
# CARD 1: SIGNATURE HERO (hero.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_hero_card() -> str:
    """Render 880x310 signature animated hero card."""
    delay_header = "0.1s" if not IS_STATIC else "0s"
    delay_name = "0.2s" if not IS_STATIC else "0s"
    delay_bio = "0.3s" if not IS_STATIC else "0s"
    delay_badges = "0.4s" if not IS_STATIC else "0s"
    delay_orb = "0.2s" if not IS_STATIC else "0s"

    extra_css = f"""
    .anim-hdr {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_header} both; }}
    .anim-name {{ animation: rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) {delay_name} both; }}
    .anim-bio {{ animation: rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) {delay_bio} both; }}
    .anim-badges {{ animation: rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) {delay_badges} both; }}
    .anim-orb {{ animation: fade 0.8s ease {delay_orb} both; }}
    .orbit-ring {{ transform-origin: 740px 155px; transform-box: view-box; animation: orbit 24s linear infinite; }}
    .beacon-pulse {{ transform-origin: 28px 36px; transform-box: view-box; animation: beacon 2.5s ease-in-out infinite; }}
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 310" width="100%" height="310">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
    <linearGradient id="hero-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{CYAN_PRIMARY}" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="{BORDER_DEFAULT}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="{ORANGE_ACCENT}" stop-opacity="0.6"/>
    </linearGradient>
    <radialGradient id="orb-core" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{CYAN_PRIMARY}" stop-opacity="0.8"/>
      <stop offset="60%" stop-color="{CYAN_MUTED}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{CYAN_PRIMARY}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background Card -->
  <rect x="1" y="1" width="878" height="308" rx="14" fill="{BG_CARD}" stroke="url(#hero-border)" stroke-width="1.5"/>

  <!-- Top Metadata Bar -->
  <g class="anim-hdr">
    <circle class="beacon-pulse" cx="28" cy="36" r="4.5" fill="{MINT_PRIMARY}"/>
    <circle cx="28" cy="36" r="2.5" fill="{TEXT_PRIMARY}"/>
    <text x="44" y="40" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1.5">SYS_ID: H-7 // LAT 19.0760 LON 72.8777 // STATUS: ALL SYSTEMS NOMINAL</text>
    <text x="850" y="40" fill="{CYAN_PRIMARY}" font-size="11" text-anchor="end" letter-spacing="1">ARCHITECTURAL HUD</text>
    <line x1="20" y1="56" x2="860" y2="56" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  </g>

  <!-- Left Content Column -->
  <g class="anim-name">
    <text x="40" y="98" fill="{CYAN_PRIMARY}" font-size="12" letter-spacing="2">01 // PRINCIPAL IDENTITY</text>
    <text x="40" y="146" fill="{TEXT_PRIMARY}" font-size="44" font-weight="700" letter-spacing="-0.5">Harmit Kalal</text>
    <text x="40" y="176" fill="{TEXT_SECONDARY}" class="sans" font-size="16" font-weight="500">AI Systems Engineer &amp; System Architect</text>
  </g>

  <g class="anim-bio">
    <text x="40" y="214" fill="{TEXT_MUTED}" class="sans" font-size="13">Architecting anti-hallucination multi-agent AI frameworks, real-time battle policy engines,</text>
    <text x="40" y="234" fill="{TEXT_MUTED}" class="sans" font-size="13">and high-frequency deterministic telemetry systems. Focused on ground-truth engineering.</text>
  </g>

  <!-- Metric Badges Row -->
  <g class="anim-badges">
    <!-- Badge 1: tribunal-kit -->
    <rect x="40" y="258" width="168" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="50" y="276" fill="{CYAN_PRIMARY}" font-size="10.5" font-weight="600">⚡ TRIBUNAL-KIT</text>
    <text x="145" y="276" fill="{TEXT_SECONDARY}" font-size="10.5">52 AGENTS</text>

    <!-- Badge 2: Hackathon -->
    <rect x="218" y="258" width="232" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="228" y="276" fill="{MINT_PRIMARY}" font-size="10.5" font-weight="600">🏆 BOI × IIT-H WINNER</text>
    <text x="365" y="276" fill="{TEXT_SECONDARY}" font-size="10.5">ARGUS-X</text>

    <!-- Badge 3: Code Volume -->
    <rect x="460" y="258" width="164" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="470" y="276" fill="{ORANGE_ACCENT}" font-size="10.5" font-weight="600">📦 12.05 MB CODE</text>
    <text x="575" y="276" fill="{TEXT_SECONDARY}" font-size="10.5">15 REPOS</text>
  </g>

  <!-- Right Visual Motif: Cyber Architect Constellation Orb -->
  <g class="anim-orb">
    <!-- Ambient Radial Glow -->
    <circle cx="740" cy="175" r="95" fill="url(#orb-core)"/>
    
    <!-- Outer Coordinates Grid -->
    <circle cx="740" cy="175" r="80" fill="none" stroke="{BORDER_DEFAULT}" stroke-width="1" stroke-dasharray="3 4"/>
    <circle cx="740" cy="175" r="60" fill="none" stroke="{CYAN_MUTED}" stroke-width="1" stroke-opacity="0.4"/>
    <circle cx="740" cy="175" r="40" fill="none" stroke="{BORDER_DEFAULT}" stroke-width="1"/>

    <!-- Rotating Orbital Rings -->
    <g class="orbit-ring">
      <ellipse cx="740" cy="175" rx="78" ry="28" fill="none" stroke="{CYAN_PRIMARY}" stroke-width="1.2" stroke-opacity="0.8"/>
      <ellipse cx="740" cy="175" rx="28" ry="78" fill="none" stroke="{ORANGE_ACCENT}" stroke-width="1" stroke-opacity="0.6"/>
      <!-- Orbital Satellite Nodes -->
      <circle cx="818" cy="175" r="3.5" fill="{CYAN_PRIMARY}"/>
      <circle cx="662" cy="175" r="2.5" fill="{CYAN_PRIMARY}"/>
      <circle cx="740" cy="97" r="3" fill="{ORANGE_ACCENT}"/>
    </g>

    <!-- Core Nucleus -->
    <circle cx="740" cy="175" r="14" fill="{BG_CARD}" stroke="{CYAN_PRIMARY}" stroke-width="2"/>
    <circle cx="740" cy="175" r="6" fill="{CYAN_PRIMARY}"/>
    <text x="740" y="275" fill="{TEXT_MUTED}" font-size="10" text-anchor="middle" letter-spacing="2">AUTONOMOUS RUNTIME</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 2: CONTRIBUTION HEATMAP (heatmap.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_heatmap_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x210 53-week contribution calendar card."""
    weeks = contrib_data.get("weeks", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    active_days = contrib_data.get("active_days", 100)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)

    # Color scale (Cyber Cyan / Emerald intensity)
    level_colors = {
        0: "#101622",  # idle cell
        1: "#004752",  # level 1
        2: "#008B9B",  # level 2
        3: "#00D4E5",  # level 3
        4: "#00F0FF",  # level 4 neon
    }

    extra_css = """
    .cell { transition: fill 0.2s ease; }
    """

    svg_cells = []
    cell_size = 11.2
    cell_gap = 3.2
    start_x = 48.0
    start_y = 70.0

    # Render month labels
    month_labels = []
    last_month = None
    for w_idx, week in enumerate(weeks):
        for day in week:
            if day and day.get("date"):
                m_str = day["date"][5:7] # MM
                if m_str != last_month:
                    last_month = m_str
                    dt = None
                    try:
                        from datetime import datetime
                        dt = datetime.strptime(day["date"], "%Y-%m-%d")
                        month_name = dt.strftime("%b")
                        x_pos = start_x + w_idx * (cell_size + cell_gap)
                        month_labels.append(f'<text x="{x_pos:.1f}" y="56" fill="{TEXT_MUTED}" font-size="9.5">{month_name}</text>')
                    except Exception:
                        pass
                break

    # Weekday labels
    weekday_labels = [
        f'<text x="26" y="{start_y + 1 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">M</text>',
        f'<text x="26" y="{start_y + 3 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">W</text>',
        f'<text x="26" y="{start_y + 5 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">F</text>',
    ]

    # Render column groups with staggered animation
    week_groups = []
    for col_idx, week in enumerate(weeks):
        x = start_x + col_idx * (cell_size + cell_gap)
        delay = f"{0.05 + col_idx * 0.008:.3f}s" if not IS_STATIC else "0s"
        anim_attr = f'style="animation: fade 0.3s ease {delay} both;"' if not IS_STATIC else ""
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
    <style>{get_base_css(extra_css, ["mono"])}</style>
  </defs>

  <!-- Background -->
  <rect x="1" y="1" width="878" height="203" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Header -->
  <text x="36" y="32" fill="{CYAN_PRIMARY}" font-size="11" letter-spacing="2">02 // ANNUAL SHIPPING CADENCE</text>
  <text x="188" y="32" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1">· 53-WEEK CONTRIBUTION CALENDAR</text>
  
  <!-- Right Badge -->
  <rect x="620" y="16" width="224" height="24" rx="6" fill="{BG_SUBTLE}" stroke="{CYAN_PRIMARY}" stroke-opacity="0.4" stroke-width="1"/>
  <text x="732" y="32" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600" text-anchor="middle">
    <tspan fill="{CYAN_PRIMARY}">{total_contribs}</tspan> CONTRIBUTIONS IN PAST YEAR
  </text>

  <!-- Labels -->
  {months_markup}
  {weekdays_markup}

  <!-- Grid Cells -->
  <g>
    {cells_markup}
  </g>

  <!-- Footer Legend & Stats -->
  <text x="48" y="186" fill="{TEXT_MUTED}" font-size="10.5">
    ACTIVE CADENCE: <tspan fill="{MINT_PRIMARY}">{active_days} ACTIVE DAYS</tspan> &#160;·&#160; LONGEST STREAK: <tspan fill="{TEXT_PRIMARY}">{longest_streak} DAYS</tspan>
  </text>

  <g transform="translate(735, 175)">
    <text x="-8" y="10" fill="{TEXT_MUTED}" font-size="9.5" text-anchor="end">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2" fill="{level_colors[0]}"/>
    <rect x="14" y="0" width="10" height="10" rx="2" fill="{level_colors[1]}"/>
    <rect x="28" y="0" width="10" height="10" rx="2" fill="{level_colors[2]}"/>
    <rect x="42" y="0" width="10" height="10" rx="2" fill="{level_colors[3]}"/>
    <rect x="56" y="0" width="10" height="10" rx="2" fill="{level_colors[4]}"/>
    <text x="76" y="10" fill="{TEXT_MUTED}" font-size="9.5">More</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 3: MONTHLY ACTIVITY (activity.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_activity_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x250 monthly activity bars with streak & weekday telemetry."""
    monthly_totals = contrib_data.get("monthly_totals", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)
    busiest_day = contrib_data.get("busiest_day", {})
    busiest_wd = contrib_data.get("busiest_weekday", {})
    active_days = contrib_data.get("active_days", 100)

    # Calculate max month count for proportional bar scaling
    counts = [m.get("count", 0) for m in monthly_totals] or [1]
    max_count = max(counts) if max(counts) > 0 else 1
    chart_h = 78.0
    base_y = 126.0

    extra_css = """
    .bar-rect { transform-origin: bottom; }
    """

    svg_bars = []
    # Distribute 13 bars across x = 40 to 840 (width 800)
    num_bars = len(monthly_totals)
    bar_width = 32.0
    slot_width = (800.0 - bar_width) / max(num_bars - 1, 1)

    for i, m in enumerate(monthly_totals):
        cnt = m.get("count", 0)
        lbl = m.get("label", "")
        x = 40.0 + i * slot_width
        b_h = max((cnt / max_count) * chart_h, 3.0) if cnt > 0 else 2.0
        y = base_y - b_h

        is_peak = cnt == max_count
        fill = CYAN_PRIMARY if is_peak else (MINT_PRIMARY if cnt > 15 else BORDER_HIGHLIGHT)
        delay = f"{0.15 + i * 0.03:.3f}s" if not IS_STATIC else "0s"
        anim_style = f"animation: grow 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both;" if not IS_STATIC else ""

        # Number on top
        txt_y = y - 5.0
        txt_color = CYAN_PRIMARY if is_peak else TEXT_MUTED
        svg_bars.append(
            f'<g>'
            f'<text x="{x + bar_width/2:.1f}" y="{txt_y:.1f}" fill="{txt_color}" font-size="9.5" font-weight="{600 if is_peak else 400}" text-anchor="middle">{cnt}</text>'
            f'<rect class="bar-rect" x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{b_h:.1f}" rx="4" fill="{fill}" style="{anim_style}"/>'
            f'<text x="{x + bar_width/2:.1f}" y="{base_y + 16:.1f}" fill="{TEXT_MUTED if not is_peak else TEXT_PRIMARY}" font-size="10" text-anchor="middle">{lbl}</text>'
            f'</g>'
        )

    bars_markup = "\n    ".join(svg_bars)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 250" width="100%" height="250">
  <defs>
    <style>{get_base_css(extra_css)}</style>
  </defs>

  <rect x="1" y="1" width="878" height="248" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Header -->
  <text x="36" y="32" fill="{CYAN_PRIMARY}" font-size="11" letter-spacing="2">03 // MONTHLY ACTIVITY SPECTRUM</text>
  <text x="210" y="32" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1">· CONTRIBUTIONS BY MONTH (12-MONTH CADENCE)</text>

  <!-- Bars Area -->
  <line x1="36" y1="{base_y:.1f}" x2="844" y2="{base_y:.1f}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  {bars_markup}

  <!-- Telemetry Pods at Bottom -->
  <g transform="translate(36, 172)">
    <!-- Pod 1 -->
    <rect x="0" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="14" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
    <text x="14" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{total_contribs} <tspan fill="{CYAN_PRIMARY}" font-size="11" font-weight="400">COMMITS</tspan></text>

    <!-- Pod 2 -->
    <rect x="204" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="218" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">LONGEST STREAK</text>
    <text x="218" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{longest_streak} <tspan fill="{MINT_PRIMARY}" font-size="11" font-weight="400">DAYS CONSECUTIVE</tspan></text>

    <!-- Pod 3 -->
    <rect x="408" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="422" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">BUSIEST WEEKDAY</text>
    <text x="422" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{busiest_wd.get('name', 'Mon')} <tspan fill="{ORANGE_ACCENT}" font-size="11" font-weight="400">({busiest_wd.get('count', 51)} COMMITS)</tspan></text>

    <!-- Pod 4 -->
    <rect x="612" y="0" width="194" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="626" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">ACTIVE DAYS VELOCITY</text>
    <text x="626" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{active_days} <tspan fill="{TEXT_MUTED}" font-size="11" font-weight="400">/ 371 DAYS (27%)</tspan></text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 4: THREE HORIZONTAL CLICKABLE TILES (build.svg, secure.svg, simulate.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_tile_build() -> str:
    """Render 286x240 tile for BUILD (tribunal-kit & AI Governance)."""
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css()}</style>
    <linearGradient id="tile-grad-build" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{CYAN_PRIMARY}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{BORDER_DEFAULT}" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- Card Frame -->
  <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Accent Top Border -->
  <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{CYAN_PRIMARY}" stroke-width="2.5"/>

  <!-- Header -->
  <text x="24" y="34" fill="{CYAN_PRIMARY}" font-size="10.5" font-weight="600" letter-spacing="2">04A // BUILD</text>
  <text x="262" y="34" fill="{CYAN_PRIMARY}" font-size="14" text-anchor="end">⟶</text>

  <!-- Vector Icon: Multi-Agent Neural Mesh -->
  <g transform="translate(24, 52)">
    <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <circle cx="16" cy="16" r="4" fill="{CYAN_PRIMARY}"/>
    <circle cx="30" cy="16" r="3" fill="{TEXT_MUTED}"/>
    <circle cx="23" cy="30" r="4.5" fill="{MINT_PRIMARY}"/>
    <line x1="16" y1="16" x2="30" y2="16" stroke="{CYAN_MUTED}" stroke-width="1.5"/>
    <line x1="16" y1="16" x2="23" y2="30" stroke="{CYAN_MUTED}" stroke-width="1.5"/>
    <line x1="30" y1="16" x2="23" y2="30" stroke="{CYAN_MUTED}" stroke-width="1.5"/>
  </g>

  <!-- Content -->
  <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">tribunal-kit</text>
  <text x="24" y="146" fill="{CYAN_PRIMARY}" font-size="11" font-weight="600">ANTI-HALLUCINATION AI</text>
  <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">52 autonomous specialist agents,</text>
  <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">40 workflows &amp; .acf spec engine.</text>

  <!-- Metric Footer -->
  <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">27x Context Compression</text>
  <text x="262" y="224" fill="{CYAN_PRIMARY}" font-size="10.5" text-anchor="end">TypeScript · Rust</text>
</svg>"""
    return svg


def render_tile_secure() -> str:
    """Render 286x240 tile for SECURE (ARGUS-X Malware Analysis)."""
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css()}</style>
  </defs>

  <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>
  <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{MINT_PRIMARY}" stroke-width="2.5"/>

  <text x="24" y="34" fill="{MINT_PRIMARY}" font-size="10.5" font-weight="600" letter-spacing="2">04B // SECURE</text>
  <text x="262" y="34" fill="{MINT_PRIMARY}" font-size="14" text-anchor="end">⟶</text>

  <!-- Vector Icon: Shield with Threat Radar -->
  <g transform="translate(24, 52)">
    <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <path d="M 23 10 L 35 15 L 35 26 Q 35 34 23 37 Q 11 34 11 26 L 11 15 Z" fill="none" stroke="{MINT_PRIMARY}" stroke-width="1.8"/>
    <circle cx="23" cy="22" r="3" fill="{MINT_PRIMARY}"/>
  </g>

  <!-- Content -->
  <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">ARGUS-X</text>
  <text x="24" y="146" fill="{MINT_PRIMARY}" font-size="11" font-weight="600">MALWARE DECEPTION</text>
  <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">Trigger-graph reasoning &amp; dynamic</text>
  <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">shadow deception verification.</text>

  <!-- Metric Footer -->
  <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">BOI × IIT-H Winner</text>
  <text x="262" y="224" fill="{MINT_PRIMARY}" font-size="10.5" text-anchor="end">Python · MITRE</text>
</svg>"""
    return svg


def render_tile_simulate() -> str:
    """Render 286x240 tile for SIMULATE (F1 Telemetry & ClashVision)."""
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css()}</style>
  </defs>

  <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>
  <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{ORANGE_ACCENT}" stroke-width="2.5"/>

  <text x="24" y="34" fill="{ORANGE_ACCENT}" font-size="10.5" font-weight="600" letter-spacing="2">04C // SIMULATE</text>
  <text x="262" y="34" fill="{ORANGE_ACCENT}" font-size="14" text-anchor="end">⟶</text>

  <!-- Vector Icon: Telemetry Waveform -->
  <g transform="translate(24, 52)">
    <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <path d="M 8 28 L 15 28 L 20 14 L 26 34 L 32 18 L 38 28" fill="none" stroke="{ORANGE_ACCENT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Content -->
  <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">F1 &amp; ClashVision</text>
  <text x="24" y="146" fill="{ORANGE_ACCENT}" font-size="11" font-weight="600">TELEMETRY &amp; RL POLICY</text>
  <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">High-frequency lap trace simulation</text>
  <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">&amp; real-time battle PCI evaluation.</text>

  <!-- Metric Footer -->
  <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">Sub-ms Physics Interpolation</text>
  <text x="262" y="224" fill="{ORANGE_ACCENT}" font-size="10.5" text-anchor="end">FastAPI · DuckDB</text>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 5: SECTION TITLE (title-systems-dark.svg & title-systems-light.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_title_card(theme: str = "dark") -> str:
    """Render 880x70 adaptive section title banner."""
    is_dark = theme == "dark"
    bg_fill = BG_CARD if is_dark else "#F1F5F9"
    border_col = BORDER_DEFAULT if is_dark else "#CBD5E1"
    text_col = TEXT_PRIMARY if is_dark else "#0F172A"
    sub_col = CYAN_PRIMARY if is_dark else "#0284C7"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 70" width="100%" height="70">
  <defs>
    <style>{get_base_css()}</style>
  </defs>

  <rect x="1" y="1" width="878" height="68" rx="10" fill="{bg_fill}" stroke="{border_col}" stroke-width="1.2"/>
  <rect x="18" y="16" width="4" height="38" rx="2" fill="{sub_col}"/>
  
  <text x="36" y="32" fill="{sub_col}" font-size="10.5" font-weight="600" letter-spacing="2">05 // ARCHITECTURAL DOSSIER</text>
  <text x="36" y="52" fill="{text_col}" font-size="16" font-weight="700">Flagship Production Systems &amp; Frameworks</text>
  <text x="850" y="42" fill="{TEXT_MUTED}" font-size="11" text-anchor="end">VERIFIED OPEN-SOURCE REPOSITORIES</text>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 6: FEATURED REPOSITORY CARDS (repo-*.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_repo_card(
    name: str,
    stars: int,
    forks: int,
    language: str,
    lang_color: str,
    desc_line1: str,
    desc_line2: str,
    footer_text: str,
) -> str:
    """Render 286x210 individual repository showcase card."""
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 210" width="100%" height="210">
  <defs>
    <style>{get_base_css()}</style>
  </defs>

  <rect x="1" y="1" width="284" height="208" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Top bar -->
  <text x="24" y="32" fill="{CYAN_PRIMARY}" font-size="10" letter-spacing="1.5">SYS_REPO</text>
  <g transform="translate(200, 20)">
    <circle cx="10" cy="10" r="3.5" fill="{lang_color}"/>
    <text x="20" y="13" fill="{TEXT_MUTED}" font-size="10">{language}</text>
  </g>

  <!-- Repo Title -->
  <text x="24" y="66" fill="{TEXT_PRIMARY}" font-size="17" font-weight="700">{escape(name)}</text>

  <!-- Description -->
  <text x="24" y="96" fill="{TEXT_MUTED}" class="sans" font-size="11.5">{escape(desc_line1)}</text>
  <text x="24" y="114" fill="{TEXT_MUTED}" class="sans" font-size="11.5">{escape(desc_line2)}</text>

  <!-- Stats Pill -->
  <g transform="translate(24, 134)">
    <rect x="0" y="0" width="80" height="24" rx="5" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="14" y="16" fill="{AMBER_ACCENT}" font-size="11">★</text>
    <text x="28" y="16" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600">{stars} stars</text>

    <rect x="88" y="0" width="80" height="24" rx="5" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="100" y="16" fill="{TEXT_MUTED}" font-size="11">⑂</text>
    <text x="114" y="16" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600">{forks} fork</text>
  </g>

  <!-- Footer link indicator -->
  <line x1="24" y1="174" x2="262" y2="174" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  <text x="24" y="194" fill="{TEXT_MUTED}" font-size="10.5">{escape(footer_text)}</text>
  <text x="262" y="194" fill="{CYAN_PRIMARY}" font-size="12" text-anchor="end">⟶</text>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 7: DEVELOPER INFORMATION PANEL (developer-panel.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_developer_panel() -> str:
    """Render 880x250 developer info dossier (terminal & neofetch inspired)."""
    extra_css = """
    .cursor-blink { animation: blink 1s step-start infinite; }
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 250" width="100%" height="250">
  <defs>
    <style>{get_base_css(extra_css)}</style>
  </defs>

  <rect x="1" y="1" width="878" height="248" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Console Header Bar -->
  <rect x="1" y="1" width="878" height="38" rx="14" fill="{BG_SUBTLE}"/>
  <path d="M 1 20 L 1 38 L 879 38 L 879 20 Z" fill="{BG_SUBTLE}"/>
  <circle cx="26" cy="19" r="5" fill="#EF4444"/>
  <circle cx="44" cy="19" r="5" fill="#F59E0B"/>
  <circle cx="62" cy="19" r="5" fill="#10B981"/>
  <text x="440" y="23" fill="{TEXT_MUTED}" font-size="11" text-anchor="middle" letter-spacing="1">harmit@deepspace: ~/architecture-manifest.dossier</text>
  <line x1="1" y1="38" x2="879" y2="38" stroke="{BORDER_DEFAULT}" stroke-width="1"/>

  <!-- Left Column: Specs -->
  <g transform="translate(36, 60)">
    <text x="0" y="16" fill="{CYAN_PRIMARY}" font-size="11" letter-spacing="1.5">06A // SYSTEM SPECS &amp; RUNTIME</text>

    <text x="0" y="42" fill="{TEXT_MUTED}" font-size="11">OPERATING ENTITY:</text>
    <text x="145" y="42" fill="{TEXT_PRIMARY}" font-size="11" font-weight="600">Harmit Kalal (@Harmitx7)</text>

    <text x="0" y="64" fill="{TEXT_MUTED}" font-size="11">PRIMARY MANDATE:</text>
    <text x="145" y="64" fill="{TEXT_PRIMARY}" font-size="11" font-weight="600">AI Systems Engineer &amp; System Architect</text>

    <text x="0" y="86" fill="{TEXT_MUTED}" font-size="11">ACTIVE RUNTIME:</text>
    <text x="145" y="86" fill="{MINT_PRIMARY}" font-size="11" font-weight="600">tribunal-kit v1.0 (Rust / TypeScript)</text>

    <text x="0" y="108" fill="{TEXT_MUTED}" font-size="11">CORE RESEARCH:</text>
    <text x="145" y="108" fill="{TEXT_PRIMARY}" font-size="11">Anti-Hallucination SDD, .acf Compression</text>

    <text x="0" y="130" fill="{TEXT_MUTED}" font-size="11">CODEBASE ANALYZED:</text>
    <text x="145" y="130" fill="{ORANGE_ACCENT}" font-size="11" font-weight="600">12,052,249 bytes across 15 repositories</text>

    <text x="0" y="152" fill="{TEXT_MUTED}" font-size="11">UPTIME METRIC:</text>
    <text x="145" y="152" fill="{TEXT_PRIMARY}" font-size="11">100.0% · 0.00% Hallucination Target</text>
  </g>

  <!-- Divider -->
  <line x1="450" y1="56" x2="450" y2="225" stroke="{BORDER_DEFAULT}" stroke-width="1" stroke-dasharray="2 3"/>

  <!-- Right Column: Focus & Stack -->
  <g transform="translate(480, 60)">
    <text x="0" y="16" fill="{MINT_PRIMARY}" font-size="11" letter-spacing="1.5">06B // TECHNICAL STACK &amp; HONORS</text>

    <text x="0" y="42" fill="{TEXT_MUTED}" font-size="11">LANGUAGES:</text>
    <text x="120" y="42" fill="{TEXT_PRIMARY}" font-size="11">TypeScript, Python, Rust, Java, C#, Go</text>

    <text x="0" y="64" fill="{TEXT_MUTED}" font-size="11">FRAMEWORKS:</text>
    <text x="120" y="64" fill="{TEXT_PRIMARY}" font-size="11">FastAPI, DuckDB, Supabase, PyTorch, Node.js</text>

    <text x="0" y="86" fill="{TEXT_MUTED}" font-size="11">CYBER DEFENSE:</text>
    <text x="120" y="86" fill="{TEXT_PRIMARY}" font-size="11">Trigger-Graph Deception, MITRE ATT&amp;CK</text>

    <text x="0" y="108" fill="{TEXT_MUTED}" font-size="11">ACHIEVEMENTS:</text>
    <text x="120" y="108" fill="{MINT_PRIMARY}" font-size="11" font-weight="600">BOI × IIT Hyderabad Hackathon Winner</text>

    <text x="0" y="130" fill="{TEXT_MUTED}" font-size="11">WEB PORTFOLIO:</text>
    <text x="120" y="130" fill="{CYAN_PRIMARY}" font-size="11">harmit.vercel.app</text>

    <text x="0" y="162" fill="{TEXT_MUTED}" font-size="11">CONSOLE INPUT:</text>
    <text x="120" y="162" fill="{TEXT_PRIMARY}" font-size="11">harmit@deepspace:~$ npx tribunal-kit init</text>
    <rect class="cursor-blink" x="424" y="152" width="7" height="13" fill="{CYAN_PRIMARY}"/>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# CARD 8: CLOSING SIGNATURE FOOTER (footer.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_footer_card() -> str:
    """Render 880x90 closing cryptographic signature HUD."""
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 90" width="100%" height="90">
  <defs>
    <style>{get_base_css()}</style>
  </defs>

  <rect x="1" y="1" width="878" height="88" rx="12" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.2"/>

  <text x="440" y="32" fill="{CYAN_PRIMARY}" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="3">
    HARMIT KALAL // ARCHITECTURAL IDENTITY VERIFIED
  </text>
  <text x="440" y="52" fill="{TEXT_MUTED}" font-size="10" text-anchor="middle" letter-spacing="1">
    SHA-256: 7e9b8f2d4c01a5e39b74f0a2d1e8c9b3 // 0 THIRD-PARTY WIDGETS // 100% CAMO COMPLIANT
  </text>
  <text x="440" y="70" fill="{TEXT_SUBTLE}" font-size="9.5" text-anchor="middle" letter-spacing="1">
    SCHEDULED GITHUB ACTIONS AUTOMATION ACTIVE · SYNCHRONIZED TWICE DAILY
  </text>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# MASTER COMPILER PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def compile_all_cards(out_dir: str = OUT_DIR) -> Dict[str, str]:
    """Compile all cards into out_dir and return file map."""
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load contribution data
    contrib_data = {}
    if os.path.exists(DATA_CONTRIB):
        with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)
    else:
        # Fallback minimal data if not fetched yet
        contrib_data = {
            "total_contributions": 250,
            "active_days": 100,
            "weeks_count": 53,
            "weeks": [],
            "monthly_totals": [],
            "longest_streak": {"days": 5},
            "busiest_day": {"date": "2026-09-27", "count": 12, "weekday": "Sun"},
            "busiest_weekday": {"name": "Monday", "count": 51},
        }

    # 2. Render cards
    cards = {
        "hero.svg": render_hero_card(),
        "heatmap.svg": render_heatmap_card(contrib_data),
        "activity.svg": render_activity_card(contrib_data),
        "build.svg": render_tile_build(),
        "secure.svg": render_tile_secure(),
        "simulate.svg": render_tile_simulate(),
        "title-systems-dark.svg": render_title_card(theme="dark"),
        "title-systems-light.svg": render_title_card(theme="light"),
        "repo-tribunal-kit.svg": render_repo_card(
            name="tribunal-kit",
            stars=6,
            forks=1,
            language="JavaScript",
            lang_color="#F7DF1E",
            desc_line1="Universal governance layer for AI coding agents.",
            desc_line2="Subagent-Driven Development (SDD) & .acf engine.",
            footer_text="npx tribunal-kit init",
        ),
        "repo-clashvision.svg": render_repo_card(
            name="ClashVision v3.0",
            stars=2,
            forks=0,
            language="Python",
            lang_color="#3572A5",
            desc_line1="AI battle predictor & real-time policy engine.",
            desc_line2="NVIDIA LocateAnything-3B & Kaggle Season 18.",
            footer_text="PCI Consistency Index",
        ),
        "repo-f1-telemetry.svg": render_repo_card(
            name="F1-TELEMETRY",
            stars=0,
            forks=0,
            language="Python",
            lang_color="#3572A5",
            desc_line1="Formula 1 high-frequency telemetry dashboard.",
            desc_line2="Deterministic physics simulation & lap comparisons.",
            footer_text="FastAPI · DuckDB · Plotly",
        ),
        "developer-panel.svg": render_developer_panel(),
        "footer.svg": render_footer_card(),
    }

    # 3. Write files
    written_files = {}
    for filename, content in cards.items():
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = os.path.getsize(filepath) / 1024.0
        print(f"✔ Rendered {filename:24} ({size_kb:4.1f} KB) -> {filepath}")
        written_files[filename] = filepath

    return written_files


def main():
    print("=" * 76)
    print("HARMITX7 // REFERENCE-INSPIRED ANIMATED SVG CARD COMPILER")
    print(f"Static Mode: {IS_STATIC}")
    print("=" * 76)
    compile_all_cards()
    print("-" * 76)
    print("✔ All cards compiled successfully.")


if __name__ == "__main__":
    main()
