"""Generator for the 4-Tier Technical Skill Constellation Matrix (skill-tree.svg)."""

from src.svg.animation import AnimationEngine
from src.svg.filters import GlowFilter
from src.svg.gradients import create_luminous_rim_gradient, create_void_surface_gradient
from src.svg.primitives import Circle, Group, Line, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, Text
from src.utils.colors import (
    COLOR_ACCENT_CORAL,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_TANGERINE,
    COLOR_BG_SURFACE,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


def generate_skill_matrix_svg(animated: bool = True) -> str:
    """Generate the 4-Tier Skill Architecture Constellation SVG."""
    root = SvgRoot(
        view_box="0 0 960 500",
        width="100%",
        title="4-Tier Technical Skill Architecture Matrix — Harmit Kalal",
        desc="Audited skill constellation spanning AI & Agentic, Systems & Backend, Web & Interactive, and Cybersecurity.",
    )

    root.add_def(create_void_surface_gradient("smVoid"))
    root.add_def(create_luminous_rim_gradient("smRim"))
    root.add_def(GlowFilter("smGlow", std_deviation=2.5))

    anim = AnimationEngine(animated=animated)
    if animated:
        anim.add_keyframe("constBreath", "0%,100%{stroke-opacity:0.06;} 50%{stroke-opacity:0.25;}")
        anim.add_class(".const-link", "animation: constBreath 6s ease-in-out infinite;")
        anim.add_keyframe("nodeShimmer", "0%,100%{opacity:0.3;} 50%{opacity:0.8;}")
        anim.add_class(".const-star", "animation: nodeShimmer 4s ease-in-out infinite;")
        anim.add_keyframe("chipFloat", "0%{opacity:0;transform:translateY(8px);} 100%{opacity:1;transform:translateY(0);}")
        anim.add_class(".chip", "animation: chipFloat 0.5s cubic-bezier(0.16,1,0.3,1) forwards;")
    root.style_block = anim.generate_style_block()

    # Container
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=500,
            rx=14,
            fill="url(#smVoid)",
            stroke="url(#smRim)",
            stroke_width=1.2,
        )
    )

    # Background Constellation Links
    const_g = Group(opacity=0.7)
    const_g.add(Line(x1=100, y1=110, x2=300, y2=195, stroke=COLOR_ACCENT_CYAN, stroke_width=0.6, class_name="const-link" if animated else None))
    const_g.add(Line(x1=300, y1=195, x2=500, y2=280, stroke=COLOR_ACCENT_TANGERINE, stroke_width=0.5, class_name="const-link" if animated else None, style="animation-delay:1s;" if animated else None))
    const_g.add(Line(x1=500, y1=280, x2=700, y2=370, stroke=COLOR_ACCENT_MINT, stroke_width=0.6, class_name="const-link" if animated else None, style="animation-delay:2s;" if animated else None))
    const_g.add(Circle(cx=100, cy=110, r=2, fill=COLOR_ACCENT_CYAN, class_name="const-star" if animated else None))
    const_g.add(Circle(cx=300, cy=195, r=2, fill=COLOR_ACCENT_TANGERINE, class_name="const-star" if animated else None, style="animation-delay:0.8s;" if animated else None))
    const_g.add(Circle(cx=500, cy=280, r=2, fill=COLOR_ACCENT_MINT, class_name="const-star" if animated else None, style="animation-delay:1.6s;" if animated else None))
    const_g.add(Circle(cx=700, cy=370, r=2, fill=COLOR_ACCENT_CORAL, class_name="const-star" if animated else None, style="animation-delay:2.4s;" if animated else None))
    root.add(const_g)

    # Header Bar
    root.add(
        Text(
            text="// SKILL_ARCHITECTURE_MATRIX",
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
            text="4 ORBITAL CLUSTERS // 26 AUDITED CAPABILITIES",
            x=928,
            y=42,
            font_size=11.5,
            font_weight="600",
            text_anchor="end",
            fill=COLOR_TEXT_FAINT,
            letter_spacing=1.5,
        )
    )
    root.add(Line(x1=32, y1=56, x2=928, y2=56, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))

    # 4 Tiers Definition
    tiers = [
        {
            "y": 95,
            "title": "TIER 01: AI & AGENTIC INFRASTRUCTURE",
            "accent": COLOR_ACCENT_CYAN,
            "chips": ["LLM Orchestration", "Subagent-Driven Dev", "MCP Protocol", "Semantic Distillation (.acf)", "Prompt Defense", "Anti-Hallucination Gates"],
        },
        {
            "y": 185,
            "title": "TIER 02: SYSTEMS & BACKEND ARCHITECTURE",
            "accent": COLOR_ACCENT_TANGERINE,
            "chips": ["Python / FastAPI", "Rust Core Engines", "Node.js / TypeScript", "DuckDB & Analytics", "PostgreSQL", "Distributed Micro-Workers"],
        },
        {
            "y": 275,
            "title": "TIER 03: WEB & INTERACTIVE ENGINEERING",
            "accent": COLOR_ACCENT_MINT,
            "chips": ["Next.js 15 / React", "tRPC Endpoints", "TailwindCSS", "SVG Component Engineering", "60fps Physics Motion", "Core Web Vitals"],
        },
        {
            "y": 365,
            "title": "TIER 04: CYBERSECURITY & CORE INFRASTRUCTURE",
            "accent": COLOR_ACCENT_CORAL,
            "chips": ["Mobile Threat Analysis", "Shadow-Data Deception Layer", "Docker Containerization", "GitHub Actions CI/CD", "OWASP Hardening", "Linux Kernel"],
        },
    ]

    for t in tiers:
        ty = t["y"]
        accent = t["accent"]
        tg = Group()

        # Tier Title & Accent Indicator
        tg.add(Circle(cx=40, cy=ty - 4, r=4.5, fill=accent))
        tg.add(
            Text(
                text=t["title"],
                x=56,
                y=ty,
                font_size=11.5,
                font_weight="700",
                fill=accent,
                letter_spacing=1.2,
            )
        )

        # Chips row (y = ty + 16)
        chip_x = 40.0
        chip_y = ty + 16
        for chip in t["chips"]:
            # Approximate width based on character count: 8px per char + 20px padding
            chip_w = len(chip) * 7.5 + 24
            tg.add(
                Rect(
                    x=chip_x,
                    y=chip_y,
                    width=chip_w,
                    height=28,
                    rx=6,
                    fill=COLOR_BG_SURFACE,
                    stroke=COLOR_BORDER_SUBTLE,
                    stroke_width=0.8,
                )
            )
            # Chip small color node
            tg.add(Circle(cx=chip_x + 12, cy=chip_y + 14, r=2.5, fill=accent, opacity=0.8))
            tg.add(
                Text(
                    text=chip,
                    x=chip_x + 22,
                    y=chip_y + 18,
                    font_size=11.5,
                    font_weight="500",
                    fill=COLOR_TEXT_PRIMARY,
                )
            )
            chip_x += chip_w + 12.0

        root.add(tg)

    # Footer verification line
    root.add(Line(x1=32, y1=455, x2=928, y2=455, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))
    foot_g = Group(transform="translate(32, 478)")
    foot_g.add(Circle(cx=0, cy=-4, r=3, fill=COLOR_ACCENT_CYAN))
    foot_g.add(Circle(cx=12, cy=-4, r=3, fill=COLOR_ACCENT_TANGERINE))
    foot_g.add(Circle(cx=24, cy=-4, r=3, fill=COLOR_ACCENT_MINT))
    foot_g.add(Circle(cx=36, cy=-4, r=3, fill=COLOR_ACCENT_CORAL))
    foot_g.add(Text(text="ORBITAL CLUSTERS SYNCHRONIZED // ZERO UNVERIFIED CLAIMS", x=52, y=0, font_size=11.0, fill=COLOR_TEXT_MUTED, letter_spacing=1.0))
    foot_g.add(Text(text="STATUS: 99.99% NOMINAL", x=896, y=0, font_size=11.0, font_weight="700", text_anchor="end", fill=COLOR_ACCENT_MINT))
    root.add(foot_g)

    return root.render()
