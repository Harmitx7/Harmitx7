#!/usr/bin/env python3
"""
Single Master Card Renderer for Harmit Kalal (@Harmitx7).
Renders all animated profile cards into cards/:
1. cards/hero.svg           - Hero with name, one-line bio & vector ASCII portrait
2. cards/heatmap.svg        - 53-week contribution graph in Harmit's brand colors
3. cards/activity.svg       - Monthly activity chart with streak, active days & busiest day
4. cards/build.svg          - Linked tile 1 (BUILD: tribunal-kit)
5. cards/secure.svg         - Linked tile 2 (SECURE: ARGUS-X)
6. cards/simulate.svg       - Linked tile 3 (SIMULATE: F1 Telemetry & ClashVision)
7. cards/repo-tribunal-kit  - Featured repository card 1
8. cards/repo-clashvision   - Featured repository card 2
9. cards/repo-f1-telemetry  - Featured repository card 3
10. cards/footer.svg        - Verified cryptographic closing signature

Supports:
- STATIC=1 environment override for instant static final-frame mode
- Embedded Base64 WOFF font subsets (Geist Mono, Geist)
- SMIL and CSS keyframe animations with staggered top-to-bottom sequence
- prefers-reduced-motion accessibility barrier
- Full GitHub Camo proxy compliance (< 50 KB per card, 0 external requests, valid XML)
"""

import base64
import json
import os
import sys
from html import escape
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_CONTRIB = os.path.join(REPO_ROOT, "data", "contributions.json")
OUT_DIR = os.path.join(REPO_ROOT, "cards")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

# Check static mode
IS_STATIC = os.environ.get("STATIC") == "1"

# ══════════════════════════════════════════════════════════════════════════════
# BRAND PALETTE (Matched to Harmit's portfolio & README)
# ══════════════════════════════════════════════════════════════════════════════
BG_VOID = "#05070B"
BG_SURFACE = "#0B0F17"
BG_CARD = "#0C111C"
BG_SUBTLE = "#101624"
BORDER_DEFAULT = "#1E293B"
BORDER_HIGHLIGHT = "#334155"

BRAND_CYAN = "#00F0FF"       # Electric Cyan accent
BRAND_MINT = "#00E676"       # Operational Green
BRAND_ORANGE = "#FF6B00"     # Solar Flame
BRAND_AMBER = "#FBBF24"      # Star Amber

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#64748B"

FONT_MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
FONT_SANS = "Geist, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# ══════════════════════════════════════════════════════════════════════════════
# FONT SUBSETTING & BASE64 EMBEDDING (pyftsubset output)
# ══════════════════════════════════════════════════════════════════════════════
_CACHED_FONTS: Dict[str, str] = {}


def get_embedded_fonts_css(font_keys: Optional[List[str]] = None) -> str:
    """Generate @font-face CSS rules with embedded Base64 WOFF data URIs."""
    if font_keys is None:
        font_keys = ["mono"]

    font_defs = {
        "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
        "sans": ("Geist", "normal", 400, "geist-400.woff"),
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
    * {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    text {{ font-family: {FONT_MONO}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    {extra_css}
"""

    return f"""
    {fonts_css}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
    @keyframes beacon {{ 0%, 100% {{ transform: scale(1); opacity: 0.95; }} 50% {{ transform: scale(1.3); opacity: 0.35; }} }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes orbit {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    text {{ font-family: {FONT_MONO}; }}
    .sans {{ font-family: {FONT_SANS}; }}
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
# 1. HERO CARD (cards/hero.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_hero_card() -> str:
    """Render 880x280 signature hero with name, one-line bio & vector ASCII portrait."""
    delay_hdr = "0.05s" if not IS_STATIC else "0s"
    delay_name = "0.15s" if not IS_STATIC else "0s"
    delay_bio = "0.25s" if not IS_STATIC else "0s"
    delay_badges = "0.35s" if not IS_STATIC else "0s"
    delay_portrait = "0.20s" if not IS_STATIC else "0s"

    extra_css = f"""
    .anim-hdr {{ animation: rise 0.5s cubic-bezier(0.16, 1, 0.3, 1) {delay_hdr} both; }}
    .anim-name {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_name} both; }}
    .anim-bio {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_bio} both; }}
    .anim-badges {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay_badges} both; }}
    .anim-portrait {{ animation: fade 0.7s ease {delay_portrait} both; }}
    .orbit-spin {{ transform-origin: 730px 145px; transform-box: view-box; animation: orbit 24s linear infinite; }}
    .beacon-pulse {{ transform-origin: 28px 34px; transform-box: view-box; animation: beacon 2.4s ease-in-out infinite; }}
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 280" width="100%" height="280">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
    <linearGradient id="hero-rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{BRAND_CYAN}" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="{BORDER_DEFAULT}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="{BRAND_ORANGE}" stop-opacity="0.6"/>
    </linearGradient>
    <radialGradient id="portrait-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{BRAND_CYAN}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{BG_CARD}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Card Background -->
  <rect x="1" y="1" width="878" height="278" rx="14" fill="{BG_CARD}" stroke="url(#hero-rim)" stroke-width="1.5"/>

  <!-- Top Metadata Bar -->
  <g class="anim-hdr">
    <circle class="beacon-pulse" cx="28" cy="34" r="4.5" fill="{BRAND_MINT}"/>
    <circle cx="28" cy="34" r="2.5" fill="{TEXT_PRIMARY}"/>
    <text x="44" y="38" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1.5">SYS_ID: H-7 // LAT 19.0760 LON 72.8777 // STATUS: ALL SYSTEMS NOMINAL</text>
    <text x="850" y="38" fill="{BRAND_CYAN}" font-size="11" text-anchor="end" letter-spacing="1">ARCHITECTURAL HUD</text>
    <line x1="20" y1="52" x2="860" y2="52" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  </g>

  <!-- Left Content Column -->
  <g class="anim-name">
    <text x="36" y="88" fill="{BRAND_CYAN}" font-size="11" letter-spacing="2">01 // PRINCIPAL IDENTITY</text>
    <text x="36" y="132" fill="{TEXT_PRIMARY}" font-size="40" font-weight="700" letter-spacing="-0.5">Harmit Kalal</text>
  </g>

  <!-- One Line About Me -->
  <g class="anim-bio">
    <text x="36" y="166" fill="{TEXT_SECONDARY}" class="sans" font-size="14.5" font-weight="500">
      AI Systems Engineer &amp; System Architect · Building anti-hallucination multi-agent governance and deterministic runtimes.
    </text>
  </g>

  <!-- Metric Badges Row -->
  <g class="anim-badges">
    <rect x="36" y="200" width="168" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="48" y="218" fill="{BRAND_CYAN}" font-size="10.5" font-weight="600">⚡ TRIBUNAL-KIT</text>
    <text x="142" y="218" fill="{TEXT_SECONDARY}" font-size="10.5">52 AGENTS</text>

    <rect x="214" y="200" width="224" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="226" y="218" fill="{BRAND_MINT}" font-size="10.5" font-weight="600">🏆 BOI × IIT-H WINNER</text>
    <text x="362" y="218" fill="{TEXT_SECONDARY}" font-size="10.5">ARGUS-X</text>

    <rect x="448" y="200" width="160" height="28" rx="6" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="460" y="218" fill="{BRAND_ORANGE}" font-size="10.5" font-weight="600">📦 12.05 MB CODE</text>
    <text x="562" y="218" fill="{TEXT_SECONDARY}" font-size="10.5">15 REPOS</text>
  </g>

  <!-- Right Column: Vector ASCII Cyber-Portrait Frame -->
  <g class="anim-portrait" transform="translate(640, 68)">
    <rect x="0" y="0" width="198" height="178" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <circle cx="99" cy="89" r="75" fill="url(#portrait-glow)"/>
    
    <!-- Portrait Header -->
    <rect x="0" y="0" width="198" height="22" rx="10" fill="{BORDER_DEFAULT}" fill-opacity="0.5"/>
    <text x="10" y="15" fill="{BRAND_CYAN}" font-size="9" letter-spacing="1">PORTRAIT // VECTOR_ASCII</text>
    <circle cx="186" cy="11" r="2.5" fill="{BRAND_MINT}"/>

    <!-- Monospace ASCII Architect Glyphs -->
    <text x="20" y="46" fill="{BRAND_CYAN}" font-size="8.5" letter-spacing="1">      .---[ SYS_ARCH ]---.      </text>
    <text x="20" y="60" fill="{TEXT_PRIMARY}" font-size="8.5" letter-spacing="1">     /    Harmit Kalal    \\     </text>
    <text x="20" y="74" fill="{TEXT_PRIMARY}" font-size="8.5" letter-spacing="1">    |  [AI-ENGINEERING]    |    </text>
    <text x="20" y="88" fill="{BRAND_MINT}" font-size="8.5" letter-spacing="1">    |  .acf Spec // 0 Halluc|   </text>
    <text x="20" y="102" fill="{TEXT_PRIMARY}" font-size="8.5" letter-spacing="1">    |   LAT 19.07  LON 72.87 |  </text>
    <text x="20" y="116" fill="{BRAND_ORANGE}" font-size="8.5" letter-spacing="1">     \\   BOI × IIT-H 2026   /    </text>
    <text x="20" y="130" fill="{BRAND_CYAN}" font-size="8.5" letter-spacing="1">      '---[ 100% GROUND ]---'      </text>

    <!-- Scanning Radar Crosshair & Rotating Orbit -->
    <g class="orbit-spin">
      <circle cx="99" cy="89" r="48" fill="none" stroke="{BRAND_CYAN}" stroke-width="1" stroke-dasharray="2 4" stroke-opacity="0.6"/>
      <circle cx="147" cy="89" r="3" fill="{BRAND_CYAN}"/>
    </g>

    <text x="99" y="162" fill="{TEXT_MUTED}" font-size="8.5" text-anchor="middle" letter-spacing="1">VERIFIED DEVELOPER AVATAR</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# 2. 53-WEEK CONTRIBUTION GRAPH (cards/heatmap.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_heatmap_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x205 53-week contribution graph in Harmit's electric cyan brand colors."""
    weeks = contrib_data.get("weeks", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    active_days = contrib_data.get("active_days", 100)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)

    level_colors = {
        0: "#101622",
        1: "#004752",
        2: "#008B9B",
        3: "#00D4E5",
        4: "#00F0FF",
    }

    cell_size = 11.2
    cell_gap = 3.2
    start_x = 48.0
    start_y = 70.0

    # Month labels
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
                        month_labels.append(f'<text x="{x_pos:.1f}" y="56" fill="{TEXT_MUTED}" font-size="9.5">{month_name}</text>')
                    except Exception:
                        pass
                break

    # Weekday labels (Mon, Wed, Fri)
    weekday_labels = [
        f'<text x="26" y="{start_y + 1 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">M</text>',
        f'<text x="26" y="{start_y + 3 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">W</text>',
        f'<text x="26" y="{start_y + 5 * (cell_size + cell_gap) + 8:.1f}" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle">F</text>',
    ]

    # Staggered week column groups (top-to-bottom entrance delay ~0.4s to 0.7s)
    week_groups = []
    for col_idx, week in enumerate(weeks):
        x = start_x + col_idx * (cell_size + cell_gap)
        delay = f"{0.35 + col_idx * 0.007:.3f}s" if not IS_STATIC else "0s"
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
    <style>{get_base_css("", ["mono"])}</style>
  </defs>

  <rect x="1" y="1" width="878" height="203" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Header -->
  <text x="36" y="32" fill="{BRAND_CYAN}" font-size="11" letter-spacing="2">02 // ANNUAL SHIPPING CADENCE</text>
  <text x="188" y="32" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1">· 53-WEEK CONTRIBUTION CALENDAR</text>
  
  <!-- Right Total Badge -->
  <rect x="620" y="16" width="224" height="24" rx="6" fill="{BG_SUBTLE}" stroke="{BRAND_CYAN}" stroke-opacity="0.4" stroke-width="1"/>
  <text x="732" y="32" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600" text-anchor="middle">
    <tspan fill="{BRAND_CYAN}">{total_contribs}</tspan> CONTRIBUTIONS IN PAST YEAR
  </text>

  <!-- Labels & Grid -->
  {months_markup}
  {weekdays_markup}
  <g>
    {cells_markup}
  </g>

  <!-- Footer Legend & Stats -->
  <text x="48" y="186" fill="{TEXT_MUTED}" font-size="10.5">
    ACTIVE CADENCE: <tspan fill="{BRAND_MINT}">{active_days} ACTIVE DAYS</tspan> &#160;·&#160; LONGEST STREAK: <tspan fill="{TEXT_PRIMARY}">{longest_streak} DAYS</tspan>
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
# 3. MONTHLY ACTIVITY CHART (cards/activity.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_activity_card(contrib_data: Dict[str, Any]) -> str:
    """Render 880x250 monthly activity chart with streak, active days & busiest day."""
    monthly_totals = contrib_data.get("monthly_totals", [])
    total_contribs = contrib_data.get("total_contributions", 250)
    longest_streak = contrib_data.get("longest_streak", {}).get("days", 5)
    busiest_wd = contrib_data.get("busiest_weekday", {})
    active_days = contrib_data.get("active_days", 100)

    counts = [m.get("count", 0) for m in monthly_totals] or [1]
    max_count = max(counts) if max(counts) > 0 else 1
    chart_h = 78.0
    base_y = 126.0

    svg_bars = []
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
        fill = BRAND_CYAN if is_peak else (BRAND_MINT if cnt > 15 else BORDER_HIGHLIGHT)
        delay = f"{0.65 + i * 0.025:.3f}s" if not IS_STATIC else "0s"
        anim_style = f"animation: grow 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both;" if not IS_STATIC else ""

        txt_y = y - 5.0
        txt_color = BRAND_CYAN if is_peak else TEXT_MUTED
        svg_bars.append(
            f'<g>'
            f'<text x="{x + bar_width/2:.1f}" y="{txt_y:.1f}" fill="{txt_color}" font-size="9.5" font-weight="{600 if is_peak else 400}" text-anchor="middle">{cnt}</text>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{b_h:.1f}" rx="4" fill="{fill}" style="transform-origin: bottom; {anim_style}"/>'
            f'<text x="{x + bar_width/2:.1f}" y="{base_y + 16:.1f}" fill="{TEXT_MUTED if not is_peak else TEXT_PRIMARY}" font-size="10" text-anchor="middle">{lbl}</text>'
            f'</g>'
        )

    bars_markup = "\n    ".join(svg_bars)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 250" width="100%" height="250">
  <defs>
    <style>{get_base_css("", ["mono"])}</style>
  </defs>

  <rect x="1" y="1" width="878" height="248" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

  <!-- Header -->
  <text x="36" y="32" fill="{BRAND_CYAN}" font-size="11" letter-spacing="2">03 // MONTHLY ACTIVITY SPECTRUM</text>
  <text x="210" y="32" fill="{TEXT_MUTED}" font-size="11" letter-spacing="1">· CONTRIBUTIONS BY MONTH (PEAK: MAR 2026 // 42 COMMITS)</text>

  <!-- Bars Area -->
  <line x1="36" y1="{base_y:.1f}" x2="844" y2="{base_y:.1f}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
  {bars_markup}

  <!-- Telemetry Pods at Bottom -->
  <g transform="translate(36, 172)">
    <!-- Pod 1: Total Activity -->
    <rect x="0" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="14" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
    <text x="14" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{total_contribs} <tspan fill="{BRAND_CYAN}" font-size="11" font-weight="400">COMMITS</tspan></text>

    <!-- Pod 2: Longest Streak -->
    <rect x="204" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="218" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">LONGEST STREAK</text>
    <text x="218" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{longest_streak} <tspan fill="{BRAND_MINT}" font-size="11" font-weight="400">DAYS CONSECUTIVE</tspan></text>

    <!-- Pod 3: Busiest Weekday -->
    <rect x="408" y="0" width="190" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="422" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">BUSIEST WEEKDAY</text>
    <text x="422" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{busiest_wd.get('name', 'Mon')} <tspan fill="{BRAND_ORANGE}" font-size="11" font-weight="400">({busiest_wd.get('count', 51)} COMMITS)</tspan></text>

    <!-- Pod 4: Active Days Velocity -->
    <rect x="612" y="0" width="194" height="56" rx="8" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="626" y="22" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="1">ACTIVE DAYS VELOCITY</text>
    <text x="626" y="44" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">{active_days} <tspan fill="{TEXT_MUTED}" font-size="11" font-weight="400">/ 371 DAYS (27%)</tspan></text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# 4. THREE LINKED TILES (cards/build.svg, cards/secure.svg, cards/simulate.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_tile_build() -> str:
    """Render 286x240 tile for BUILD (tribunal-kit & AI Governance)."""
    delay = "0.95s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>
    <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{BRAND_CYAN}" stroke-width="2.5"/>

    <text x="24" y="34" fill="{BRAND_CYAN}" font-size="10.5" font-weight="600" letter-spacing="2">04A // BUILD</text>
    <text x="262" y="34" fill="{BRAND_CYAN}" font-size="14" text-anchor="end">⟶</text>

    <!-- Vector Icon: Multi-Agent Neural Mesh -->
    <g transform="translate(24, 52)">
      <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
      <circle cx="16" cy="16" r="4" fill="{BRAND_CYAN}"/>
      <circle cx="30" cy="16" r="3" fill="{TEXT_MUTED}"/>
      <circle cx="23" cy="30" r="4.5" fill="{BRAND_MINT}"/>
      <line x1="16" y1="16" x2="30" y2="16" stroke="{BRAND_CYAN}" stroke-width="1.5" stroke-opacity="0.6"/>
      <line x1="16" y1="16" x2="23" y2="30" stroke="{BRAND_CYAN}" stroke-width="1.5" stroke-opacity="0.6"/>
      <line x1="30" y1="16" x2="23" y2="30" stroke="{BRAND_CYAN}" stroke-width="1.5" stroke-opacity="0.6"/>
    </g>

    <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">tribunal-kit</text>
    <text x="24" y="146" fill="{BRAND_CYAN}" font-size="11" font-weight="600">AI AGENT GOVERNANCE</text>
    <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">52 autonomous specialist agents,</text>
    <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">40 workflows &amp; .acf spec engine.</text>

    <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">27x Context Compression</text>
    <text x="262" y="224" fill="{BRAND_CYAN}" font-size="10.5" text-anchor="end">TypeScript · Rust</text>
  </g>
</svg>"""
    return svg


def render_tile_secure() -> str:
    """Render 286x240 tile for SECURE (ARGUS-X Malware Analysis)."""
    delay = "1.02s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>
    <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{BRAND_MINT}" stroke-width="2.5"/>

    <text x="24" y="34" fill="{BRAND_MINT}" font-size="10.5" font-weight="600" letter-spacing="2">04B // SECURE</text>
    <text x="262" y="34" fill="{BRAND_MINT}" font-size="14" text-anchor="end">⟶</text>

    <!-- Vector Icon: Shield with Threat Radar -->
    <g transform="translate(24, 52)">
      <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
      <path d="M 23 10 L 35 15 L 35 26 Q 35 34 23 37 Q 11 34 11 26 L 11 15 Z" fill="none" stroke="{BRAND_MINT}" stroke-width="1.8"/>
      <circle cx="23" cy="22" r="3" fill="{BRAND_MINT}"/>
    </g>

    <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">ARGUS-X</text>
    <text x="24" y="146" fill="{BRAND_MINT}" font-size="11" font-weight="600">MALWARE DECEPTION</text>
    <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">Trigger-graph reasoning &amp; dynamic</text>
    <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">shadow deception verification.</text>

    <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">BOI × IIT-H Winner</text>
    <text x="262" y="224" fill="{BRAND_MINT}" font-size="10.5" text-anchor="end">Python · MITRE</text>
  </g>
</svg>"""
    return svg


def render_tile_simulate() -> str:
    """Render 286x240 tile for SIMULATE (F1 Telemetry & ClashVision)."""
    delay = "1.09s" if not IS_STATIC else "0s"
    extra_css = f".anim-tile {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 240" width="100%" height="240">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
  </defs>

  <g class="anim-tile">
    <rect x="1" y="1" width="284" height="238" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>
    <path d="M 1 14 Q 1 1 14 1 L 272 1 Q 285 1 285 14" fill="none" stroke="{BRAND_ORANGE}" stroke-width="2.5"/>

    <text x="24" y="34" fill="{BRAND_ORANGE}" font-size="10.5" font-weight="600" letter-spacing="2">04C // SIMULATE</text>
    <text x="262" y="34" fill="{BRAND_ORANGE}" font-size="14" text-anchor="end">⟶</text>

    <!-- Vector Icon: Telemetry Waveform -->
    <g transform="translate(24, 52)">
      <rect x="0" y="0" width="46" height="46" rx="10" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
      <path d="M 8 28 L 15 28 L 20 14 L 26 34 L 32 18 L 38 28" fill="none" stroke="{BRAND_ORANGE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <text x="24" y="126" fill="{TEXT_PRIMARY}" font-size="18" font-weight="700">F1 &amp; ClashVision</text>
    <text x="24" y="146" fill="{BRAND_ORANGE}" font-size="11" font-weight="600">TELEMETRY &amp; RL POLICY</text>
    <text x="24" y="170" fill="{TEXT_MUTED}" class="sans" font-size="12">High-frequency lap trace simulation</text>
    <text x="24" y="186" fill="{TEXT_MUTED}" class="sans" font-size="12">&amp; real-time battle PCI evaluation.</text>

    <line x1="24" y1="204" x2="262" y2="204" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="24" y="224" fill="{TEXT_SECONDARY}" font-size="10.5">Sub-ms Physics Interpolation</text>
    <text x="262" y="224" fill="{BRAND_ORANGE}" font-size="10.5" text-anchor="end">FastAPI · DuckDB</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# 5. FEATURED REPOSITORY CARDS (repo-*.svg)
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
    delay_s: float = 1.25,
) -> str:
    """Render 286x200 individual repository showcase card."""
    delay = f"{delay_s:.2f}s" if not IS_STATIC else "0s"
    extra_css = f".anim-repo {{ animation: rise 0.6s cubic-bezier(0.16, 1, 0.3, 1) {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 200" width="100%" height="200">
  <defs>
    <style>{get_base_css(extra_css, ["mono", "sans"])}</style>
  </defs>

  <g class="anim-repo">
    <rect x="1" y="1" width="284" height="198" rx="14" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.5"/>

    <!-- Top bar -->
    <text x="24" y="32" fill="{BRAND_CYAN}" font-size="10" letter-spacing="1.5">SYS_REPO</text>
    <g transform="translate(195, 20)">
      <circle cx="10" cy="10" r="3.5" fill="{lang_color}"/>
      <text x="20" y="13" fill="{TEXT_MUTED}" font-size="10">{language}</text>
    </g>

    <!-- Repo Title -->
    <text x="24" y="66" fill="{TEXT_PRIMARY}" font-size="17" font-weight="700">{escape(name)}</text>

    <!-- Description -->
    <text x="24" y="94" fill="{TEXT_MUTED}" class="sans" font-size="11.5">{escape(desc_line1)}</text>
    <text x="24" y="112" fill="{TEXT_MUTED}" class="sans" font-size="11.5">{escape(desc_line2)}</text>

    <!-- Stats Pill -->
    <g transform="translate(24, 130)">
      <rect x="0" y="0" width="80" height="24" rx="5" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
      <text x="14" y="16" fill="{BRAND_AMBER}" font-size="11">★</text>
      <text x="28" y="16" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600">{stars} stars</text>

      <rect x="88" y="0" width="80" height="24" rx="5" fill="{BG_SUBTLE}" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
      <text x="100" y="16" fill="{TEXT_MUTED}" font-size="11">⑂</text>
      <text x="114" y="16" fill="{TEXT_PRIMARY}" font-size="10.5" font-weight="600">{forks} fork</text>
    </g>

    <!-- Footer link indicator -->
    <line x1="24" y1="166" x2="262" y2="166" stroke="{BORDER_DEFAULT}" stroke-width="1"/>
    <text x="24" y="186" fill="{TEXT_MUTED}" font-size="10.5">{escape(footer_text)}</text>
    <text x="262" y="186" fill="{BRAND_CYAN}" font-size="12" text-anchor="end">⟶</text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# 6. CLOSING SIGNATURE FOOTER (cards/footer.svg)
# ══════════════════════════════════════════════════════════════════════════════
def render_footer_card() -> str:
    """Render 880x80 closing cryptographic signature HUD."""
    delay = "1.45s" if not IS_STATIC else "0s"
    extra_css = f".anim-ftr {{ animation: fade 0.6s ease {delay} both; }}"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 80" width="100%" height="80">
  <defs>
    <style>{get_base_css(extra_css, ["mono"])}</style>
  </defs>

  <g class="anim-ftr">
    <rect x="1" y="1" width="878" height="78" rx="12" fill="{BG_CARD}" stroke="{BORDER_DEFAULT}" stroke-width="1.2"/>

    <text x="440" y="30" fill="{BRAND_CYAN}" font-size="11" font-weight="600" text-anchor="middle" letter-spacing="3">
      HARMIT KALAL // ARCHITECTURAL IDENTITY VERIFIED
    </text>
    <text x="440" y="48" fill="{TEXT_MUTED}" font-size="10" text-anchor="middle" letter-spacing="1">
      SHA-256: 7e9b8f2d4c01a5e39b74f0a2d1e8c9b3 // 0 THIRD-PARTY WIDGETS // 100% CAMO COMPLIANT
    </text>
    <text x="440" y="64" fill="{TEXT_MUTED}" font-size="9" text-anchor="middle" letter-spacing="1" opacity="0.7">
      AUTOMATED GITHUB ACTIONS CI/CD · SCHEDULED REFRESH TWICE DAILY
    </text>
  </g>
</svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# MASTER SCRIPT ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════
def compile_cards(out_dir: str = OUT_DIR) -> Dict[str, str]:
    """Render all animated cards and write to out_dir."""
    os.makedirs(out_dir, exist_ok=True)

    contrib_data = {}
    if os.path.exists(DATA_CONTRIB):
        with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)
    else:
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

    cards = {
        "hero.svg": render_hero_card(),
        "heatmap.svg": render_heatmap_card(contrib_data),
        "activity.svg": render_activity_card(contrib_data),
        "build.svg": render_tile_build(),
        "secure.svg": render_tile_secure(),
        "simulate.svg": render_tile_simulate(),
        "repo-tribunal-kit.svg": render_repo_card(
            name="tribunal-kit",
            stars=6,
            forks=1,
            language="JavaScript",
            lang_color="#F7DF1E",
            desc_line1="Universal governance layer for AI coding agents.",
            desc_line2="Subagent-Driven Development (SDD) & .acf engine.",
            footer_text="npx tribunal-kit init",
            delay_s=1.20,
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
            delay_s=1.27,
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
            delay_s=1.34,
        ),
        "footer.svg": render_footer_card(),
    }

    result = {}
    for filename, content in cards.items():
        fpath = os.path.join(out_dir, filename)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        size_kb = os.path.getsize(fpath) / 1024.0
        print(f"✔ Compiled {filename:22} ({size_kb:4.1f} KB) -> {fpath}")
        result[filename] = fpath

    return result


def main():
    print("=" * 76)
    print("HARMITX7 // SINGLE MASTER SVG CARD RENDERER (scripts/render_cards.py)")
    print(f"Target Directory: {OUT_DIR}")
    print(f"Static Mode:      {IS_STATIC}")
    print("=" * 76)
    compile_cards()
    print("-" * 76)
    print("✔ All cards compiled successfully.")


if __name__ == "__main__":
    main()
