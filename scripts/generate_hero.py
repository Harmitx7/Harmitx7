#!/usr/bin/env python3
"""
Editorial Typographic Portrait Hero Generator for Harmit Kalal (@Harmitx7).
Renders a custom self-contained SVG inspired by high-contrast editorial typography
and generative monochrome ASCII/halftone portraiture.

Features:
- Warm off-white paper canvas (#F4F4F1) with subtle rounded frame (rx="16")
- 2.1:1 target aspect ratio (900x430)
- Left column: Small blue square + role, two-line Instrument Serif name (Harmit / Kalal in italic),
  clean sans bio, and website link with blue arrow
- Right column: High-resolution monochrome ASCII generative portrait floating seamlessly
  without any rectangular image frame, aspect-ratio calibrated to natural facial proportions
- Restrained top-to-bottom reveal animation with full STATIC=1 support
- Reduced-motion accessibility barrier
- Self-contained, CAMO-compliant (< 50 KB, valid XML, zero external requests)
"""

import base64
import os
import sys
from typing import Optional
import numpy as np
from PIL import Image, ImageEnhance

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AVATAR_PATH = os.path.join(REPO_ROOT, "assets", "portrait_avatar.png")
OUTPUT_HERO_ASSETS = os.path.join(REPO_ROOT, "assets", "hero.svg")
OUTPUT_HERO_CARDS = os.path.join(REPO_ROOT, "cards", "hero.svg")
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")

IS_STATIC = os.environ.get("STATIC") == "1"


def get_embedded_serif_b64() -> str:
    """Load and base64-encode Instrument Serif."""
    fpath = os.path.join(FONTS_DIR, "serif-400.woff")
    if os.path.exists(fpath):
        with open(fpath, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    return ""


def generate_halftone_matrix_paths(
    image_path: str,
    cols: int = 56,
    rows: int = 46,
    start_x: int = 492,
    start_y: int = 50,
    step_x: float = 6.4,
    step_y: float = 7.6,
) -> str:
    """
    Generate art-directed Swiss Exhibition Vector Halftone Matrix from portrait photo.
    Encodes 5 optical density tiers into single multi-point SVG subpaths (M{x} {y}h.01)
    with stroke-linecap="round" for flawless, hardware-accelerated rendering under 50 KB.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source portrait not found at: {image_path}")

    img = Image.open(image_path).convert("L")
    
    # Tight crop centering head and shoulders (460x460 -> 15..445, 8..448)
    cropped = img.crop((15, 8, 445, 448))

    # Enhance contrast to create crisp editorial tonal separation
    enhancer = ImageEnhance.Contrast(cropped)
    contrasted = enhancer.enhance(1.35)

    resized = contrasted.resize((cols, rows), Image.Resampling.LANCZOS)
    arr = np.array(resized)

    # 5 Calibrated optical density tiers (Deep Ink to Delicate Edge Feathering)
    tiers = {0: [], 1: [], 2: [], 3: [], 4: []}

    for r in range(rows):
        y = int(round(start_y + r * step_y))
        for c in range(cols):
            val = arr[r, c]
            if val >= 208:
                continue
            x = int(round(start_x + c * step_x))
            if val < 55:
                tiers[0].append((x, y))
            elif val < 95:
                tiers[1].append((x, y))
            elif val < 140:
                tiers[2].append((x, y))
            elif val < 180:
                tiers[3].append((x, y))
            else:
                tiers[4].append((x, y))

    styles = [
        (5.2, "#141412", "0.10s"),  # Tier 0: Deepest charcoal ink (hair, pupils)
        (3.8, "#2E2C27", "0.15s"),  # Tier 1: Dark graphite (eyebrows, jawline)
        (2.6, "#5E5B53", "0.20s"),  # Tier 2: Warm slate (cheekbones, nose contour)
        (1.5, "#8F8C82", "0.25s"),  # Tier 3: Soft skin tone highlights
        (0.8, "#BAB7AD", "0.30s"),  # Tier 4: Delicate perimeter feathering
    ]

    paths = []
    for t, pts in tiers.items():
        if not pts:
            continue
        sw, col, delay = styles[t]
        d_str = "".join([f"M{x} {y}h.01" for x, y in pts])
        anim_attr = f'style="animation: fadeIn 0.5s ease {delay} both;"' if not IS_STATIC else ""
        paths.append(
            f'<path d="{d_str}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" fill="none" {anim_attr}/>'
        )

    return "\n    ".join(paths)


def render_hero_svg(source_portrait_path: Optional[str] = None) -> str:
    """Render the master editorial typographic hero SVG (880x408, 2.16:1 ratio)."""
    portrait_path = source_portrait_path or AVATAR_PATH
    if not os.path.exists(portrait_path):
        raise FileNotFoundError(f"Personal portrait image required: {portrait_path}")

    serif_b64 = get_embedded_serif_b64()

    # Generate Swiss Exhibition Vector Halftone Matrix (calibrated to 880x408 container)
    halftone_matrix = generate_halftone_matrix_paths(
        portrait_path,
        cols=56,
        rows=46,
        start_x=488,
        start_y=42,
        step_x=6.2,
        step_y=7.1,
    )

    anim_css = "" if IS_STATIC else """
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

    .anim-role { animation: fadeIn 0.4s ease 0.05s both; }
    .anim-name1 { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.12s both; }
    .anim-name2 { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.20s both; }
    .anim-bio { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.28s both; }
    .anim-link { animation: fadeIn 0.6s ease 0.36s both; }
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 408" width="100%" height="408">
  <defs>
    <style>
      @font-face {{
        font-family: 'Instrument Serif';
        font-style: normal;
        font-weight: 400;
        src: url('data:font/woff;base64,{serif_b64}') format('woff');
        font-display: swap;
      }}

      text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      }}
      .serif {{
        font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif;
      }}
      .mono {{
        font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      }}

      .name-first {{
        font-size: 78px;
        font-weight: 400;
        fill: #151515;
        letter-spacing: -1px;
      }}
      .name-last {{
        font-size: 78px;
        font-style: italic;
        font-weight: 400;
        fill: #151515;
        letter-spacing: -1px;
      }}

      {anim_css}

      @media (prefers-reduced-motion: reduce) {{
        *, ::before, ::after {{
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
        }}
      }}
    </style>
  </defs>

  <!-- Editorial Warm Off-White Canvas -->
  <rect x="1" y="1" width="878" height="406" rx="16" fill="#F3F3F0" stroke="#DEDEDA" stroke-width="1"/>

  <!-- Left Side: Identity & Editorial Typography -->
  <!-- 1. Small Blue Square + Uppercase Professional Role -->
  <g class="anim-role">
    <rect x="46" y="46" width="7.5" height="7.5" fill="#244DFF" rx="1.5"/>
    <text x="62" y="53.5" fill="#77777D" class="mono" font-size="10.5" font-weight="600" letter-spacing="1.5">FULLSTACK ENGINEER / ARCHITECT</text>
  </g>

  <!-- 2. Two-Line Editorial Serif Name -->
  <g class="anim-name1">
    <text x="46" y="136" class="serif name-first">Harmit</text>
  </g>
  <g class="anim-name2">
    <text x="46" y="208" class="serif name-last">Kalal</text>
  </g>

  <!-- 3. Short Personal Introduction in Clean Sans-Serif -->
  <g class="anim-bio">
    <text x="46" y="254" font-size="14.5" fill="#52524C" font-weight="400">
      AI Systems Engineer &amp; Architect building anti-hallucination
    </text>
    <text x="46" y="278" font-size="14.5" fill="#52524C" font-weight="400">
      multi-agent governance and deterministic software systems.
    </text>
    <text x="46" y="304" font-size="13" fill="#77777D" font-weight="400">
      Specializing in autonomous runtimes, subagents &amp; telemetry.
    </text>
  </g>

  <!-- 4. Website Link with Small Blue Directional Arrow -->
  <g class="anim-link">
    <text x="46" y="358" font-size="13.5" font-weight="600" fill="#151515" letter-spacing="0.2">harmit.vercel.app</text>
    <text x="172" y="358" font-size="14" font-weight="700" fill="#244DFF">↗</text>
  </g>

  <!-- Right Side: Swiss Exhibition Vector Halftone Matrix -->
  <g id="halftone-matrix">
    {halftone_matrix}
  </g>
</svg>"""
    return svg


def main():
    svg_content = render_hero_svg(AVATAR_PATH)

    # Save to cards/hero.svg
    os.makedirs(os.path.dirname(OUTPUT_HERO_CARDS), exist_ok=True)
    with open(OUTPUT_HERO_CARDS, "w", encoding="utf-8") as f:
        f.write(svg_content)
    size_kb = len(svg_content.encode("utf-8")) / 1024
    print(f"✔ Rendered {os.path.basename(OUTPUT_HERO_CARDS):<16} ({size_kb:4.1f} KB) -> {OUTPUT_HERO_CARDS}")


if __name__ == "__main__":
    main()
