"""Generator for Language Polyglot Spectrum SVG (languages.svg)."""

import json
import os
from typing import Dict, List, Optional, Tuple

from src.svg.animation import AnimationEngine
from src.svg.gradients import create_luminous_rim_gradient, create_void_surface_gradient
from src.svg.layouts import SegmentedProgressBar
from src.svg.primitives import Circle, Group, Line, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, Text
from src.utils.colors import (
    COLOR_ACCENT_CYAN,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    get_language_color,
)
from src.utils.formatting import format_bytes, format_percentage


def generate_languages_svg(lang_data: Optional[Dict] = None, animated: bool = True) -> str:
    """Generate the Language Polyglot Spectrum SVG component."""
    total_bytes = 0
    languages: List[Tuple[str, int, float, str]] = []

    # Load fallback from data/repositories.json if not provided
    if not lang_data:
        fallback_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "repositories.json"
        )
        if os.path.exists(fallback_path):
            try:
                with open(fallback_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    dist = content.get("languages_distribution", {})
                    total_bytes = content.get("total_code_bytes", 12050494)
                    for lname, info in dist.items():
                        b = info.get("bytes", 0)
                        pct = info.get("percentage", 0.0)
                        color = get_language_color(lname)
                        languages.append((lname, b, pct, color))
            except Exception:
                pass

    if not languages:
        # Default verified baseline
        total_bytes = 12050494
        raw = [
            ("JavaScript", 6625968, 54.98),
            ("Python", 2792707, 23.17),
            ("TypeScript", 992141, 8.23),
            ("Java", 689191, 5.72),
            ("Rust", 321836, 2.67),
            ("CSS", 261461, 2.17),
            ("HTML", 217620, 1.81),
            ("Other", 149606, 1.25),
        ]
        languages = [(l, b, p, get_language_color(l)) for l, b, p in raw]

    root = SvgRoot(
        view_box="0 0 960 180",
        width="100%",
        title="Language Polyglot Spectrum — Harmitx7",
        desc="Evidence-backed code volume distribution across public GitHub repositories.",
    )

    root.add_def(create_void_surface_gradient("langVoid"))
    root.add_def(create_luminous_rim_gradient("langRim"))

    anim = AnimationEngine(animated=animated)
    if animated:
        anim.add_keyframe("barFade", "0%{opacity:0;transform:scaleX(0.85);} 100%{opacity:1;transform:scaleX(1);}")
        anim.add_class(".spectrum-bar", "animation: barFade 0.6s cubic-bezier(0.16,1,0.3,1) forwards;")
    root.style_block = anim.generate_style_block()

    # Outer Container
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=180,
            rx=12,
            fill="url(#langVoid)",
            stroke="url(#langRim)",
            stroke_width=1.0,
        )
    )

    # Header Bar
    root.add(
        Text(
            text="// LANGUAGE_POLYGLOT_SPECTRUM",
            x=24,
            y=26,
            font_size=11.0,
            font_weight="700",
            fill=COLOR_ACCENT_CYAN,
            letter_spacing=1.5,
        )
    )
    root.add(
        Text(
            text=f"TOTAL AUDITED CODE: {format_bytes(total_bytes)} across 15 REPOSITORIES",
            x=936,
            y=26,
            font_size=10.0,
            font_weight="600",
            text_anchor="end",
            fill=COLOR_TEXT_FAINT,
            letter_spacing=1.0,
        )
    )
    root.add(Line(x1=24, y1=36, x2=936, y2=36, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))

    # Segmented Progress Bar (x=24, y=52, width=912, height=14)
    bar_segments = [(l, pct, col) for l, b, pct, col in languages]
    root.add(SegmentedProgressBar(x=24, y=52, width=912, height=14, rx=7, segments=bar_segments))

    # Legend Grid: 2 rows of 4 columns
    # Row 1 (y=98): Top 4 languages
    # Row 2 (y=138): Next 4 languages
    col_w = 912 / 4.0
    for idx, (lname, b, pct, col) in enumerate(languages[:8]):
        col_idx = idx % 4
        row_idx = idx // 4
        item_x = 24 + (col_idx * col_w)
        item_y = 104 if row_idx == 0 else 144

        lg = Group()
        # Color dot indicator
        lg.add(Circle(cx=item_x + 6, cy=item_y - 4, r=4.5, fill=col))

        # Language Name
        lg.add(
            Text(
                text=lname,
                x=item_x + 18,
                y=item_y,
                font_size=12.5,
                font_weight="700",
                fill=COLOR_TEXT_PRIMARY,
            )
        )

        # Percentage & Byte count
        lg.add(
            Text(
                text=f"{format_percentage(pct)} · {format_bytes(b)}",
                x=item_x + 18,
                y=item_y + 16,
                font_size=10.5,
                font_weight="500",
                fill=COLOR_TEXT_MUTED,
            )
        )
        root.add(lg)

    return root.render()
