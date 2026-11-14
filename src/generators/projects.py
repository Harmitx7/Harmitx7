"""Generator for the Featured Projects Architecture Grid SVG (projects.svg)."""

from typing import List
from src.svg.animation import AnimationEngine
from src.svg.filters import GlowFilter
from src.svg.gradients import create_luminous_rim_gradient, create_void_surface_gradient
from src.svg.primitives import Circle, Group, Line, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, FONT_SANS, Text, Tspan
from src.utils.colors import (
    COLOR_ACCENT_AMBER,
    COLOR_ACCENT_CORAL,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_SKY,
    COLOR_ACCENT_TANGERINE,
    COLOR_BG_SURFACE,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


def generate_projects_svg(animated: bool = True) -> str:
    """Generate the Featured Projects architectural dossier SVG."""
    root = SvgRoot(
        view_box="0 0 960 480",
        width="100%",
        title="Featured Architectural Projects — Harmit Kalal",
        desc="4 flagship engineering systems: tribunal-kit, ARGUS-X, ClashVision v3.0, and F1 Telemetry.",
    )

    # Gradients & Filters
    root.add_def(create_void_surface_gradient("projVoid"))
    root.add_def(create_luminous_rim_gradient("projRim"))
    root.add_def(GlowFilter("optGlowProj", std_deviation=2.0))

    # Animations
    anim = AnimationEngine(animated=animated)
    if animated:
        anim.add_keyframe("cardGlow", "0%,100%{stroke-opacity:0.25;} 50%{stroke-opacity:0.65;}")
        anim.add_class(".glow-border", "animation: cardGlow 4s ease-in-out infinite;")
    root.style_block = anim.generate_style_block()

    # Outer Container
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=480,
            rx=14,
            fill="url(#projVoid)",
            stroke="url(#projRim)",
            stroke_width=1.2,
        )
    )

    # Header Bar
    root.add(
        Text(
            text="// FEATURED_PRODUCTION_SYSTEMS",
            x=32,
            y=42,
            font_size=12.0,
            font_weight="700",
            fill=COLOR_ACCENT_CYAN,
            letter_spacing=1.5,
        )
    )
    root.add(
        Text(
            text="4 FLAGSHIP ENGINES // REAL CODEBASE PROVENANCE",
            x=928,
            y=42,
            font_size=11.0,
            font_weight="600",
            text_anchor="end",
            fill=COLOR_TEXT_FAINT,
            letter_spacing=1.0,
        )
    )
    root.add(Line(x1=32, y1=56, x2=928, y2=56, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))

    # 2x2 Grid Coordinates:
    # Cell 1: (32, 72, 436, 180)
    # Cell 2: (492, 72, 436, 180)
    # Cell 3: (32, 272, 436, 180)
    # Cell 4: (492, 272, 436, 180)
    cards = [
        {
            "x": 32,
            "y": 72,
            "title": "tribunal-kit",
            "tag": "MULTI-AGENT AI GOVERNANCE",
            "accent": COLOR_ACCENT_CYAN,
            "desc": "Anti-Hallucination Multi-Agent AI Framework for Cursor, Windsurf & Antigravity IDEs. 52 agents, 40 workflows, 21 Tribunal reviewers, and .acf semantic distillation engine.",
            "stack": "TypeScript · Rust Core · MCP · .acf Spec",
            "stat": "27x Context Shrink // 0% Hallucination",
        },
        {
            "x": 492,
            "y": 72,
            "title": "ARGUS-X",
            "tag": "CYBERSECURITY & THREAT ISOLATION",
            "accent": COLOR_ACCENT_TANGERINE,
            "desc": "Hypothesis-driven mobile malware analysis framework with dynamic shadow-data deception layer, trigger-graph reasoning, and MITRE ATT&CK mapping.",
            "stack": "Python · Mobile Security · Deception Layer",
            "stat": "Bank of India × IIT-H Hackathon Winner",
        },
        {
            "x": 32,
            "y": 272,
            "title": "ClashVision v3.0",
            "tag": "MACHINE LEARNING & RL POLICIES",
            "accent": COLOR_ACCENT_MINT,
            "desc": "AI Battle Predictor & Real-time Policy Engine for Clash Royale. Computes PCI (Play Consistency Index), predicts counters, and serves tactics via NVIDIA LocateAnything-3B.",
            "stack": "Python · PyTorch · Kaggle S18 · RL Policy",
            "stat": "Play Consistency Index (PCI) Engine",
        },
        {
            "x": 492,
            "y": 272,
            "title": "F1 Telemetry Dashboard",
            "tag": "HIGH-FREQUENCY TELEMETRY",
            "accent": COLOR_ACCENT_SKY,
            "desc": "Formula 1 telemetry analysis engine. Upload, compare, and simulate lap telemetry: speed, throttle, brake, and RPM traces sector-by-sector with deterministic physics.",
            "stack": "Python · FastAPI · DuckDB · Plotly · Sim",
            "stat": "Sub-millisecond Deterministic Sim",
        },
    ]

    for c in cards:
        cx, cy = c["x"], c["y"]
        w, h = 436, 180
        cg = Group()

        # Card Background
        cg.add(
            Rect(
                x=cx,
                y=cy,
                width=w,
                height=h,
                rx=10,
                fill=COLOR_BG_SURFACE,
                stroke=c["accent"],
                stroke_width=0.8,
                opacity=0.9,
                class_name="glow-border" if animated else None,
            )
        )

        # Top Accent Header
        cg.add(
            Text(
                text=c["title"],
                x=cx + 18,
                y=cy + 28,
                font_family=FONT_SANS,
                font_size=17.0,
                font_weight="800",
                fill=COLOR_TEXT_PRIMARY,
            )
        )
        cg.add(
            Text(
                text=c["tag"],
                x=cx + w - 18,
                y=cy + 26,
                font_size=9.5,
                font_weight="700",
                text_anchor="end",
                fill=c["accent"],
                letter_spacing=1.0,
            )
        )

        # Divider
        cg.add(Line(x1=cx + 18, y1=cy + 38, x2=cx + w - 18, y2=cy + 38, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.6))

        # Description (split into two readable lines)
        desc_line1 = c["desc"][:68]
        desc_line2 = c["desc"][68:140]
        cg.add(Text(text=desc_line1, x=cx + 18, y=cy + 58, font_family=FONT_SANS, font_size=11.5, fill=COLOR_TEXT_SECONDARY))
        cg.add(Text(text=desc_line2, x=cx + 18, y=cy + 76, font_family=FONT_SANS, font_size=11.5, fill=COLOR_TEXT_SECONDARY))

        # Stack Tags Box
        cg.add(Rect(x=cx + 18, y=cy + 96, width=w - 36, height=28, rx=5, fill="#141B26"))
        cg.add(Text(text=c["stack"], x=cx + 28, y=cy + 114, font_size=11.0, font_weight="600", fill=COLOR_ACCENT_SKY))

        # Bottom Verification Metric
        cg.add(Circle(cx=cx + 24, cy=cy + 148, r=3.5, fill=c["accent"]))
        cg.add(Text(text=c["stat"], x=cx + 36, y=cy + 152, font_size=10.5, font_weight="700", fill=c["accent"]))

        root.add(cg)

    return root.render()
