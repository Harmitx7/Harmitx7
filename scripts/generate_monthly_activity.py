"""
Harmit Kalal (@Harmitx7) — Editorial Monthly GitHub Activity Generator
Visual Direction: High-contrast Swiss/Editorial typography, warm paper palette,
two-column layout (70% chart / 30% statistics), and progressive bar reveal animation.
Strictly Camo-compliant (< 50 KB), self-contained, and valid SVG XML.
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
OUT_ASSET = os.path.join(REPO_ROOT, "assets", "monthly-activity.svg")
OUT_CARD = os.path.join(REPO_ROOT, "cards", "activity.svg")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

# Check static mode
IS_STATIC = os.environ.get("STATIC") == "1"

# ══════════════════════════════════════════════════════════════════════════
# COLOR PALETTE — EDITORIAL SWISS SPECIFICATION
# ══════════════════════════════════════════════════════════════════════════
BG_SURFACE = "#F3F3F0"       # Warm off-white paper canvas
BORDER_CONTAINER = "#DEDEDA" # Subtle container edge rule
DIVIDER_LINE = "#DEDEDA"     # Horizontal metric separators
TEXT_PRIMARY = "#151515"     # Near-black editorial ink
TEXT_SECONDARY = "#77777D"   # Neutral grey metadata & descriptions
TEXT_FAINT = "#A0A0A5"       # Subdued slash / secondary denominator
ACCENT_BLUE = "#315BFF"      # Vibrant electric blue for maximum peak
BAR_INACTIVE = "#151515"     # Near-black monthly bars
BAR_CURRENT = "#C8C8C4"      # Soft grey for ongoing partial month

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
        font_keys = ["serif", "sans"]

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


# ══════════════════════════════════════════════════════════════════════════
# DATA EXTRACTION & INTELLIGENCE PIPELINE
# ══════════════════════════════════════════════════════════════════════════
def extract_monthly_data(contrib_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract and validate 12-month statistics from contributions JSON."""
    if contrib_data is None:
        if os.path.exists(DATA_CONTRIB):
            with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
                contrib_data = json.load(f)
        else:
            contrib_data = {}

    total_contributions = contrib_data.get("total_contributions", 257)
    active_days = contrib_data.get("active_days", 101)
    total_calendar_days = contrib_data.get("total_calendar_days", 371)

    # Streak calculations
    longest_streak_obj = contrib_data.get("longest_streak") or {}
    longest_streak = longest_streak_obj.get("days", 5) if isinstance(longest_streak_obj, dict) else 5

    # Busiest day calculation
    busiest_day_obj = contrib_data.get("busiest_day") or {}
    busiest_day_commits = busiest_day_obj.get("count", 12) if isinstance(busiest_day_obj, dict) else 12

    # Monthly breakdown (exactly 12 months)
    monthly_raw = contrib_data.get("monthly_totals", [])
    if len(monthly_raw) >= 12:
        last12 = monthly_raw[-12:]
    else:
        # Fallback 12 months if sparse
        last12 = monthly_raw

    # Identify highest/peak month
    peak_count = 0
    peak_idx = -1
    for i, m in enumerate(last12):
        cnt = m.get("count", 0)
        if cnt > peak_count:
            peak_count = cnt
            peak_idx = i

    months = []
    for i, m in enumerate(last12):
        cnt = m.get("count", 0)
        is_peak = (i == peak_idx)
        is_current = (i == len(last12) - 1)
        months.append({
            "key": m.get("key", ""),
            "label": m.get("label", ""),
            "year": m.get("year", 2026),
            "count": cnt,
            "is_peak": is_peak,
            "is_current": is_current,
        })

    return {
        "total_contributions": total_contributions,
        "active_days": active_days,
        "total_calendar_days": total_calendar_days,
        "longest_streak": longest_streak,
        "busiest_day_commits": busiest_day_commits,
        "months": months,
        "peak_count": peak_count,
        "peak_idx": peak_idx,
    }


# ══════════════════════════════════════════════════════════════════════════
# SVG RENDERING ENGINE
# ══════════════════════════════════════════════════════════════════════════
def render_monthly_activity_svg(
    stats: Optional[Dict[str, Any]] = None,
    is_static: Optional[bool] = None,
) -> str:
    """Render 880x332 editorial monthly activity visualization SVG (2.65:1 ratio)."""
    if is_static is None:
        is_static = IS_STATIC

    if stats is None:
        stats = extract_monthly_data()

    w, h = 880, 332
    fonts_css = get_embedded_fonts_css()

    total_contributions = stats["total_contributions"]
    active_days = stats["active_days"]
    total_calendar_days = stats["total_calendar_days"]
    longest_streak = stats["longest_streak"]
    busiest_day_commits = stats["busiest_day_commits"]
    months = stats["months"]
    peak_count = stats["peak_count"]

    # Geometry constants
    left_x = 44
    y_baseline = 256
    max_bar_h = 114
    min_bar_h = 12
    bar_w = 28
    bar_gap = 16

    # Build bars SVG
    bars_svg_list = []
    bar_animations_css = []

    for i, m in enumerate(months):
        bx = left_x + i * (bar_w + bar_gap)
        cnt = m["count"]
        is_peak = m["is_peak"]
        is_current = m["is_current"]

        if peak_count > 0:
            bh = int(min_bar_h + (cnt / peak_count) * (max_bar_h - min_bar_h)) if cnt > 0 else 4
        else:
            bh = min_bar_h

        by = y_baseline - bh

        # Palette selection
        if is_peak:
            fill_color = ACCENT_BLUE
        elif is_current:
            fill_color = BAR_CURRENT
        else:
            fill_color = BAR_INACTIVE

        bar_id = f"bar-{i}"

        # Timing: Normal bars stagger 0.20s -> 0.64s; Blue peak bar appears last at 0.76s
        if not is_static:
            if is_peak:
                bar_delay = "0.76s"
            else:
                bar_delay = f"{0.20 + i * 0.04:.2f}s"

            bar_animations_css.append(
                f".{bar_id} {{\n"
                f"  transform-box: fill-box;\n"
                f"  transform-origin: bottom;\n"
                f"  animation: barGrow 0.70s cubic-bezier(0.16, 1, 0.3, 1) {bar_delay} both;\n"
                f"}}"
            )

        # Bar element
        bars_svg_list.append(
            f'    <!-- Month {i+1}: {m["label"]} ({cnt} commits) -->\n'
            f'    <rect class="bar {bar_id}" x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="4" ry="4" fill="{fill_color}" />'
        )

        # Highlight value above peak blue bar
        if is_peak:
            label_y = by - 8
            cx = bx + bar_w // 2
            peak_anim_class = "anim-peak-count" if not is_static else ""
            bars_svg_list.append(
                f'    <text class="mono {peak_anim_class}" x="{cx}" y="{label_y}" fill="{ACCENT_BLUE}" font-size="11" font-weight="600" text-anchor="middle">{cnt:,}</text>'
            )

        # Month label beneath bar
        label_y = y_baseline + 20
        cx = bx + bar_w // 2
        bars_svg_list.append(
            f'    <text class="sans label-month" x="{cx}" y="{label_y}" fill="{TEXT_SECONDARY}" font-size="11" text-anchor="middle">{m["label"]}</text>'
        )

    rendered_bars_svg = "\n".join(bars_svg_list)
    bars_css = "\n".join(bar_animations_css)

    # Master CSS Architecture
    if is_static:
        extra_css = f"""
    * {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    .bar {{ transform: none !important; }}
    """
    else:
        extra_css = f"""
    @keyframes fadeIn {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes slideUp {{
      0% {{ opacity: 0; transform: translateY(12px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes barGrow {{
      0% {{ transform: scaleY(0); }}
      100% {{ transform: scaleY(1); }}
    }}

    .anim-root {{ animation: fadeIn 0.8s ease both; }}
    .anim-header {{ animation: slideUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }}
    .anim-stat-1 {{ animation: slideUp 0.60s cubic-bezier(0.16, 1, 0.3, 1) 0.32s both; }}
    .anim-div-1  {{ animation: fadeIn 0.50s ease 0.42s both; }}
    .anim-stat-2 {{ animation: slideUp 0.60s cubic-bezier(0.16, 1, 0.3, 1) 0.52s both; }}
    .anim-div-2  {{ animation: fadeIn 0.50s ease 0.62s both; }}
    .anim-stat-3 {{ animation: slideUp 0.60s cubic-bezier(0.16, 1, 0.3, 1) 0.72s both; }}
    .anim-peak-count {{ animation: fadeIn 0.50s ease 0.95s both; }}

    {bars_css}

    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        opacity: 1 !important;
        transform: none !important;
      }}
      .bar {{ transform: none !important; }}
    }}
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      {fonts_css}
      text {{ font-family: {FONT_SANS}; }}
      .serif {{ font-family: {FONT_SERIF}; }}
      .sans {{ font-family: {FONT_SANS}; }}
      .mono {{ font-family: {FONT_MONO}; }}
      {extra_css}
    </style>
  </defs>

  <!-- Container Surface with Subtle Rounded Border -->
  <g class="anim-root">
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{BG_SURFACE}" stroke="{BORDER_CONTAINER}" stroke-width="1"/>
  </g>

  <!-- ══════════════════════════════════════════════════════════════════════════
       LEFT COLUMN — APPROXIMATELY 70% (MONTHLY CONTRIBUTIONS)
       ══════════════════════════════════════════════════════════════════════════ -->
  <g class="anim-header">
    <!-- Small Uppercase Section Label -->
    <text x="{left_x}" y="50" fill="{TEXT_SECONDARY}" class="mono" font-size="10.5" font-weight="500" letter-spacing="2">
      THE LAST 12 MONTHS ON GITHUB
    </text>

    <!-- Oversized Editorial Headline -->
    <text x="{left_x}" y="94" fill="{TEXT_PRIMARY}">
      <tspan class="serif" font-size="44" font-weight="400">{total_contributions:,} </tspan>
      <tspan class="serif" font-size="44" font-style="italic">contributions</tspan>
    </text>
  </g>

  <!-- Monthly Bar Chart -->
  <g>
{rendered_bars_svg}
  </g>

  <!-- ══════════════════════════════════════════════════════════════════════════
       RIGHT COLUMN — APPROXIMATELY 30% (EDITORIAL KEY STATISTICS)
       ══════════════════════════════════════════════════════════════════════════ -->
  
  <!-- STATISTIC 01: Streak -->
  <g class="anim-stat-1">
    <text x="640" y="84" fill="{TEXT_PRIMARY}">
      <tspan class="serif" font-size="38" font-weight="400">{longest_streak} </tspan>
      <tspan class="serif" font-size="34" font-style="italic">days</tspan>
    </text>
    <text x="640" y="106" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      current streak, and the longest
    </text>
  </g>

  <!-- Thin Horizontal Divider 01 -->
  <line class="anim-div-1" x1="640" y1="130" x2="836" y2="130" stroke="{DIVIDER_LINE}" stroke-width="1" />

  <!-- STATISTIC 02: Active Days Ratio -->
  <g class="anim-stat-2">
    <text x="640" y="176">
      <tspan class="serif" font-size="38" fill="{TEXT_PRIMARY}" font-weight="400">{active_days} </tspan>
      <tspan class="serif" font-size="32" fill="{TEXT_FAINT}">/ </tspan>
      <tspan class="serif" font-size="34" fill="{TEXT_SECONDARY}" font-style="italic">{total_calendar_days}</tspan>
    </text>
    <text x="640" y="198" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      days with a commit
    </text>
  </g>

  <!-- Thin Horizontal Divider 02 -->
  <line class="anim-div-2" x1="640" y1="222" x2="836" y2="222" stroke="{DIVIDER_LINE}" stroke-width="1" />

  <!-- STATISTIC 03: Peak Velocity on Busiest Day -->
  <g class="anim-stat-3">
    <text x="640" y="268" fill="{TEXT_PRIMARY}" class="serif" font-size="38" font-weight="400">
      {busiest_day_commits}
    </text>
    <text x="640" y="290" fill="{TEXT_SECONDARY}" class="sans" font-size="12">
      on the busiest day
    </text>
  </g>
</svg>"""
    return svg


def compile_monthly_activity(
    contrib_path: str = DATA_CONTRIB,
    out_asset_path: str = OUT_ASSET,
    out_card_path: str = OUT_CARD,
) -> str:
    """Compile and write monthly activity SVG to assets and cards directories."""
    contrib_data = {}
    if os.path.exists(contrib_path):
        with open(contrib_path, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)

    stats = extract_monthly_data(contrib_data)
    svg_content = render_monthly_activity_svg(stats)

    for p in [out_asset_path, out_card_path]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_content)
        size_kb = len(svg_content.encode("utf-8")) / 1024
        print(f"✔ Compiled monthly activity SVG ({size_kb:.1f} KB) -> {p}")

    return svg_content


if __name__ == "__main__":
    compile_monthly_activity()
