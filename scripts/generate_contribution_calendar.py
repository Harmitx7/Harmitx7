"""
Harmit Kalal (@Harmitx7) — "Every day, in blue" Premium GitHub Contribution Calendar Generator
Visual Direction: High-contrast Swiss/Editorial typography, warm paper-and-ink canvas (#F3F3F0),
53-week chronological contribution grid with five-tier blue intensity progression.
Strictly Camo-compliant (< 50 KB), self-contained, and valid SVG XML.
"""

import base64
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

DATA_CONTRIB = os.path.join(REPO_ROOT, "data", "contributions.json")
OUT_ASSET = os.path.join(REPO_ROOT, "assets", "contribution-calendar.svg")
OUT_CARD = os.path.join(REPO_ROOT, "cards", "heatmap.svg")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

# Check static mode
IS_STATIC = os.environ.get("STATIC") == "1"

# ══════════════════════════════════════════════════════════════════════════
# COLOR PALETTE — "EVERY DAY, IN BLUE" SPECIFICATION
# ══════════════════════════════════════════════════════════════════════════
BG_SURFACE = "#F3F3F0"       # Warm off-white paper canvas
BORDER_CONTAINER = "#DEDEDA" # Subtle container edge hairline
TEXT_PRIMARY = "#171717"     # Near-black editorial ink
TEXT_SECONDARY = "#77777D"   # Neutral grey metadata & month labels
ACCENT_BLUE = "#244DFF"      # Strong electric blue for title and peak activity

# 5 Intensity Levels
LEVEL_COLORS = {
    0: "#E6E6E2",  # Empty pale-grey cell
    1: "#DCE4FF",  # Level 1: pale soft blue
    2: "#AFC1FF",  # Level 2: light blue
    3: "#5478FF",  # Level 3: medium blue
    4: "#244DFF",  # Level 4: strong electric blue
}

FONT_SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
FONT_SANS = "Geist, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

# ══════════════════════════════════════════════════════════════════════════
# FONT SUBSETTING & BASE64 EMBEDDING
# ══════════════════════════════════════════════════════════════════════════
_CACHED_FONTS: Dict[str, str] = {}


def get_embedded_fonts_css() -> str:
    """Generate @font-face CSS rules with embedded Base64 WOFF data URIs for Instrument Serif."""
    if "serif" not in _CACHED_FONTS:
        fpath = os.path.join(FONTS_DIR, "serif-400.woff")
        if os.path.exists(fpath):
            with open(fpath, "rb") as f:
                _CACHED_FONTS["serif"] = base64.b64encode(f.read()).decode("ascii")
        else:
            _CACHED_FONTS["serif"] = ""
    b64 = _CACHED_FONTS.get("serif", "")
    if not b64:
        return ""
    return (
        f"@font-face {{\n"
        f"  font-family: 'Instrument Serif';\n"
        f"  font-style: normal;\n"
        f"  font-weight: 400;\n"
        f"  src: url('data:font/woff;base64,{b64}') format('woff');\n"
        f"  font-display: swap;\n"
        f"}}"
    )


# ══════════════════════════════════════════════════════════════════════════
# DATA EXTRACTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════
def extract_calendar_data(contrib_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract and validate 53-week contribution grid from contributions JSON."""
    if contrib_data is None:
        if os.path.exists(DATA_CONTRIB):
            with open(DATA_CONTRIB, "r", encoding="utf-8") as f:
                contrib_data = json.load(f)
        else:
            contrib_data = {}

    raw_weeks = contrib_data.get("weeks", [])
    total_contributions = contrib_data.get("total_contributions", 257)

    # Ensure 53 weeks
    if len(raw_weeks) > 53:
        weeks = raw_weeks[-53:]
    else:
        weeks = raw_weeks

    # Calculate month label positions (first week each month occurs)
    month_positions: List[Tuple[int, str]] = []
    seen_months = set()

    for col_idx, week in enumerate(weeks):
        for day in week:
            d_str = day.get("date")
            if not d_str:
                continue
            try:
                dt = datetime.strptime(d_str, "%Y-%m-%d")
                m_key = dt.strftime("%Y-%m")
                if m_key not in seen_months:
                    seen_months.add(m_key)
                    # Filter: Only show labels up to August to allow bottom-right legend space
                    # matching the editorial reference layout perfectly
                    month_name = dt.strftime("%b")
                    if col_idx <= 38:
                        month_positions.append((col_idx, month_name))
            except Exception:
                pass

    return {
        "weeks": weeks,
        "total_contributions": total_contributions,
        "month_positions": month_positions,
    }


# ══════════════════════════════════════════════════════════════════════════
# SVG RENDERING ENGINE
# ══════════════════════════════════════════════════════════════════════════
def render_contribution_calendar_svg(
    calendar_data: Optional[Dict[str, Any]] = None,
    is_static: Optional[bool] = None,
) -> str:
    """Render 880x258 editorial contribution calendar SVG with 3.4:1 aspect ratio."""
    if is_static is None:
        is_static = IS_STATIC

    if calendar_data is None:
        calendar_data = extract_calendar_data()

    w, h = 880, 258
    fonts_css = get_embedded_fonts_css()

    weeks = calendar_data["weeks"]
    month_positions = calendar_data["month_positions"]

    # Geometry constants
    left_x = 42.0
    grid_y = 86.0
    step = 15.1

    # Build columns and cells SVG
    col_svg_list = []

    for col_idx, week in enumerate(weeks):
        cx = round(left_x + col_idx * step, 1)
        anim_attr = ""
        if not is_static:
            delay = f"{0.18 + col_idx * 0.011:.3f}s"
            anim_attr = f' style="animation-delay:{delay}"'

        cell_rects = []
        for row_idx, day in enumerate(week):
            cy = round(grid_y + row_idx * step, 1)
            level = day.get("level", 0) if day else 0
            if level not in LEVEL_COLORS:
                level = 0

            cell_rects.append(f'<rect class="c l{level}" x="{cx}" y="{cy}"/>')

        col_svg_list.append(
            f'    <g class="col-week"{anim_attr}>' + "".join(cell_rects) + "</g>"
        )

    rendered_grid_svg = "\n".join(col_svg_list)

    # Build month labels
    month_labels_svg = []
    for col_idx, lbl in month_positions:
        mx = round(left_x + col_idx * step + 5.8, 1)
        month_labels_svg.append(
            f'<text x="{mx}" y="222" fill="{TEXT_SECONDARY}" class="mono" font-size="10.5" text-anchor="middle">{lbl}</text>'
        )
    rendered_months_svg = "\n    ".join(month_labels_svg)

    # Master CSS Architecture
    if is_static:
        extra_css = """
    * { animation: none !important; opacity: 1 !important; transform: none !important; }
    """
    else:
        extra_css = """
    @keyframes fadeIn {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
    @keyframes slideUp {
      0% { opacity: 0; transform: translateY(10px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes colRise {
      0% { opacity: 0; transform: scale(0.65); }
      100% { opacity: 1; transform: scale(1); }
    }

    .anim-root { animation: fadeIn 0.8s ease both; }
    .anim-header { animation: slideUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.12s both; }
    .anim-footer { animation: fadeIn 0.50s ease 0.82s both; }
    .col-week {
      transform-box: fill-box;
      transform-origin: center;
      animation: colRise 0.40s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        opacity: 1 !important;
        transform: none !important;
      }
      .col-week { transform: none !important; }
    }
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
      rect.c {{ width: 11.6px; height: 11.6px; rx: 2.5px; }}
      .l0 {{ fill: {LEVEL_COLORS[0]}; }}
      .l1 {{ fill: {LEVEL_COLORS[1]}; }}
      .l2 {{ fill: {LEVEL_COLORS[2]}; }}
      .l3 {{ fill: {LEVEL_COLORS[3]}; }}
      .l4 {{ fill: {LEVEL_COLORS[4]}; }}
      {extra_css}
    </style>
  </defs>

  <!-- Container Surface with Subtle Rounded Border -->
  <g class="anim-root">
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{BG_SURFACE}" stroke="{BORDER_CONTAINER}" stroke-width="1"/>
  </g>

  <!-- ══════════════════════════════════════════════════════════════════════════
       HEADER — "Every day, in blue" & REFRESHED DAILY
       ══════════════════════════════════════════════════════════════════════════ -->
  <g class="anim-header">
    <!-- Upper-Left Headline -->
    <text x="{left_x}" y="56">
      <tspan class="serif" font-size="38" font-weight="400" fill="{TEXT_PRIMARY}">Every day, </tspan>
      <tspan class="serif" font-size="38" font-style="italic" fill="{ACCENT_BLUE}">in blue</tspan>
    </text>

    <!-- Upper-Right Daily Status -->
    <text x="838" y="52" fill="{TEXT_SECONDARY}" class="mono" font-size="10.5" font-weight="500" letter-spacing="2.5" text-anchor="end">
      REFRESHED DAILY
    </text>
  </g>

  <!-- ══════════════════════════════════════════════════════════════════════════
       CONTRIBUTION GRID (53 WEEKS x 7 DAYS)
       ══════════════════════════════════════════════════════════════════════════ -->
  <g>
{rendered_grid_svg}
  </g>

  <!-- ══════════════════════════════════════════════════════════════════════════
       FOOTER — MONTH LABELS & FIVE-TIER BLUE INTENSITY LEGEND
       ══════════════════════════════════════════════════════════════════════════ -->
  <g class="anim-footer">
    <!-- Month Labels -->
    {rendered_months_svg}

    <!-- Bottom-Right Intensity Legend: less [][][][][] more -->
    <g transform="translate(712, 214)">
      <text x="0" y="8" fill="{TEXT_SECONDARY}" class="mono" font-size="10.5">less</text>
      <rect x="30" y="0" width="9" height="9" rx="2" fill="{LEVEL_COLORS[0]}" />
      <rect x="42" y="0" width="9" height="9" rx="2" fill="{LEVEL_COLORS[1]}" />
      <rect x="54" y="0" width="9" height="9" rx="2" fill="{LEVEL_COLORS[2]}" />
      <rect x="66" y="0" width="9" height="9" rx="2" fill="{LEVEL_COLORS[3]}" />
      <rect x="78" y="0" width="9" height="9" rx="2" fill="{LEVEL_COLORS[4]}" />
      <text x="94" y="8" fill="{TEXT_SECONDARY}" class="mono" font-size="10.5">more</text>
    </g>
  </g>
</svg>"""
    return svg


def compile_contribution_calendar(
    contrib_path: str = DATA_CONTRIB,
    out_asset_path: str = OUT_ASSET,
    out_card_path: str = OUT_CARD,
) -> str:
    """Compile and write contribution calendar SVG to assets and cards directories."""
    contrib_data = {}
    if os.path.exists(contrib_path):
        with open(contrib_path, "r", encoding="utf-8") as f:
            contrib_data = json.load(f)

    cal_data = extract_calendar_data(contrib_data)
    svg_content = render_contribution_calendar_svg(cal_data)

    for p in [out_asset_path, out_card_path]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_content)
        size_kb = len(svg_content.encode("utf-8")) / 1024
        print(f"✔ Compiled contribution calendar SVG ({size_kb:.1f} KB) -> {p}")

    return svg_content


if __name__ == "__main__":
    compile_contribution_calendar()
