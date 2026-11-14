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


def generate_ascii_portrait_rows(
    image_path: str,
    cols: int = 76,
    rows: int = 50,
    start_x: int = 480,
    start_y: int = 50,
    row_height: float = 6.4,
) -> str:
    """
    Generate run-length encoded SVG ASCII portrait rows from source photo.
    Compensates for monospace character width-to-height ratio (~0.6) to preserve
    Harmit's natural facial proportions.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source portrait not found at: {image_path}")

    img = Image.open(image_path).convert("L")
    
    # Tight crop centering head and shoulders (460x460 -> 15..445, 8..448)
    cropped = img.crop((15, 8, 445, 448))

    # Enhance contrast slightly to create crisp editorial tonal separation
    enhancer = ImageEnhance.Contrast(cropped)
    contrasted = enhancer.enhance(1.28)

    resized = contrasted.resize((cols, rows), Image.Resampling.LANCZOS)
    arr = np.array(resized)

    # Editorial monochromatic character ramp (darkest ink to lightest tone)
    ramps = {
        0: "@%#WMB",   # Deepest ink: curly hair, pupils, deep shadows
        1: "8&#*+=",   # Dark tone: eyebrows, jaw contour, deep midtones
        2: "=-:+~",    # Midtone: cheekbones, nose bridge, neck shading
        3: ":-..·",    # Light tone: subtle skin highlight feathering
    }
    colors = {
        0: "#141412",  # Deep charcoal ink
        1: "#42403A",  # Dark graphite
        2: "#747168",  # Warm slate midtone
        3: "#A8A59C",  # Soft paper tone
    }

    svg_lines = []
    for r in range(rows):
        y = start_y + r * row_height
        runs = []
        current_bucket = None
        current_chars = []

        delay = f"{0.12 + r * 0.007:.3f}s" if not IS_STATIC else "0s"
        anim_attr = f'style="animation: fadeIn 0.4s ease {delay} both;"' if not IS_STATIC else ""

        for c in range(cols):
            val = arr[r, c]
            # Threshold for off-white background wall in avatar (pure float, no box)
            if val > 200:
                bucket = 4
                ch = " "
            elif val < 60:
                bucket = 0
                ch = ramps[0][(c + r) % len(ramps[0])]
            elif val < 110:
                bucket = 1
                ch = ramps[1][(c + r) % len(ramps[1])]
            elif val < 155:
                bucket = 2
                ch = ramps[2][(c + r) % len(ramps[2])]
            else:
                bucket = 3
                ch = ramps[3][(c + r) % len(ramps[3])]

            if bucket == current_bucket:
                current_chars.append(ch)
            else:
                if current_chars:
                    text = "".join(current_chars).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    if current_bucket == 4:
                        runs.append(text)
                    else:
                        runs.append(f'<tspan fill="{colors[current_bucket]}">{text}</tspan>')
                current_bucket = bucket
                current_chars = [ch]

        if current_chars:
            text = "".join(current_chars).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if current_bucket == 4:
                runs.append(text)
            else:
                runs.append(f'<tspan fill="{colors[current_bucket]}">{text}</tspan>')

        line_content = "".join(runs).rstrip()
        if line_content:
            svg_lines.append(f'<text x="{start_x}" y="{y:.1f}" xml:space="preserve" {anim_attr}>{line_content}</text>')

    return "\n    ".join(svg_lines)


def render_hero_svg(source_portrait_path: Optional[str] = None) -> str:
    """Render the master editorial typographic hero SVG."""
    portrait_path = source_portrait_path or AVATAR_PATH
    if not os.path.exists(portrait_path):
        raise FileNotFoundError(f"Personal portrait image required: {portrait_path}")

    serif_b64 = get_embedded_serif_b64()

    # Generate ASCII portrait rows with 76 columns x 50 rows
    ascii_rows = generate_ascii_portrait_rows(portrait_path, cols=76, rows=50, start_x=480, start_y=50, row_height=6.4)

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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 430" width="100%" height="430">
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
        font-size: 80px;
        font-weight: 400;
        fill: #141412;
        letter-spacing: -1px;
      }}
      .name-last {{
        font-size: 80px;
        font-style: italic;
        font-weight: 400;
        fill: #141412;
        letter-spacing: -1px;
      }}

      .ascii-grid {{
        font-family: ui-monospace, 'SF Mono', Menlo, Monaco, Consolas, monospace;
        font-size: 5.3px;
        letter-spacing: 0.65px;
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
  <rect x="1" y="1" width="898" height="428" rx="16" fill="#F4F4F1" stroke="#E3E3DC" stroke-width="1"/>

  <!-- Left Side: Identity & Editorial Typography -->
  <!-- 1. Small Blue Square + Uppercase Professional Role -->
  <g class="anim-role">
    <rect x="54" y="52" width="8.5" height="8.5" fill="#2563EB" rx="1.5"/>
    <text x="71" y="60.5" fill="#52524C" class="mono" font-size="11" font-weight="600" letter-spacing="1.5">FULLSTACK ENGINEER / ARCHITECT</text>
  </g>

  <!-- 2. Two-Line Editorial Serif Name -->
  <g class="anim-name1">
    <text x="54" y="148" class="serif name-first">Harmit</text>
  </g>
  <g class="anim-name2">
    <text x="54" y="224" class="serif name-last">Kalal</text>
  </g>

  <!-- 3. Short Personal Introduction in Clean Sans-Serif -->
  <g class="anim-bio">
    <text x="54" y="274" font-size="14.5" fill="#52524C" font-weight="400">
      AI Systems Engineer &amp; Architect building anti-hallucination
    </text>
    <text x="54" y="298" font-size="14.5" fill="#52524C" font-weight="400">
      multi-agent governance and deterministic software systems.
    </text>
    <text x="54" y="326" font-size="13" fill="#888880" font-weight="400">
      Specializing in autonomous runtimes, subagents &amp; telemetry.
    </text>
  </g>

  <!-- 4. Website Link with Small Blue Directional Arrow -->
  <g class="anim-link">
    <text x="54" y="380" font-size="13.5" font-weight="600" fill="#141412" letter-spacing="0.2">harmit.vercel.app</text>
    <text x="180" y="380" font-size="14" font-weight="700" fill="#2563EB">↗</text>
  </g>

  <!-- Right Side: High-Resolution Monochrome ASCII Portrait -->
  <g class="ascii-grid">
    {ascii_rows}
  </g>
</svg>"""
    return svg


def main():
    svg_content = render_hero_svg(AVATAR_PATH)

    # Save to both assets/hero.svg and cards/hero.svg
    for target in [OUTPUT_HERO_ASSETS, OUTPUT_HERO_CARDS]:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(svg_content)
        size_kb = len(svg_content.encode("utf-8")) / 1024
        print(f"✔ Rendered {os.path.basename(target):<16} ({size_kb:4.1f} KB) -> {target}")


if __name__ == "__main__":
    main()
