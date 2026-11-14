"""Generator for the Developer Console Architecture Manifest (terminal-boot.svg)."""

from src.svg.animation import AnimationEngine, register_terminal_cursor_blink
from src.svg.filters import GlowFilter
from src.svg.gradients import (
    LinearGradient,
    create_luminous_rim_gradient,
    create_void_surface_gradient,
)
from src.svg.primitives import Circle, Group, Line, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, Text, Tspan
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
)


def generate_terminal_boot_svg(animated: bool = True) -> str:
    """Generate the Developer Console Manifest SVG component."""
    root = SvgRoot(
        view_box="0 0 960 520",
        width="100%",
        title="Developer Console Manifest — Harmit Kalal",
        desc="System architecture manifest showcasing tribunal-kit specifications and zero-trust contracts.",
    )

    root.add_def(create_void_surface_gradient("tbVoid"))
    root.add_def(create_luminous_rim_gradient("tbRim"))
    root.add_def(GlowFilter("tbGlow", std_deviation=2.0))

    # Header gradient
    root.add_def(
        LinearGradient(
            id_name="tbHeaderGrad",
            x1="0%",
            y1="0%",
            x2="100%",
            y2="0%",
            stops=[("0%", "#0A0F1C", 1.0), ("50%", "#141D30", 1.0), ("100%", "#0A0F1C", 1.0)],
        )
    )

    anim = AnimationEngine(animated=animated)
    if animated:
        register_terminal_cursor_blink(anim, period=0.85)
        anim.add_keyframe("lineReveal", "0%{opacity:0;transform:translateX(-8px);} 100%{opacity:1;transform:translateX(0);}")
        anim.add_class(".ln", "animation: lineReveal 0.35s cubic-bezier(0.16,1,0.3,1) forwards;")
    root.style_block = anim.generate_style_block()

    # Outer Container Frame
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=520,
            rx=14,
            fill="url(#tbVoid)",
            stroke="url(#tbRim)",
            stroke_width=1.2,
        )
    )

    # Window Header Bar (height=38)
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=38,
            rx=14,
            fill="url(#tbHeaderGrad)",
            stroke=COLOR_BORDER_SUBTLE,
            stroke_width=0.8,
        )
    )

    # Window Controls (macOS inspired)
    root.add(Circle(cx=24, cy=19, r=5.5, fill="#FB7185", opacity=0.85))
    root.add(Circle(cx=42, cy=19, r=5.5, fill="#FBBF24", opacity=0.85))
    root.add(Circle(cx=60, cy=19, r=5.5, fill="#34D399", opacity=0.85))

    # Header Title
    root.add(
        Text(
            text="harmit@system-architect: ~/tribunal-kit/manifest.json",
            x=82,
            y=23,
            font_size=11.5,
            font_weight="600",
            fill=COLOR_TEXT_MUTED,
        )
    )

    # Header Right Status
    root.add(
        Text(
            text="BUILD: PASS · AGENTS: 52 · REVIEWERS: 21",
            x=936,
            y=23,
            font_size=10.5,
            font_weight="700",
            text_anchor="end",
            fill=COLOR_ACCENT_MINT,
            letter_spacing=0.8,
        )
    )

    # Code Manifest Lines (x=36, start y=72)
    lines_data = [
        ("01", '{'),
        ("02", '  "system": "tribunal-kit",'),
        ("03", '  "architect": "Harmit Kalal",'),
        ("04", '  "role": "AI Systems Architect · System Architect · Full-Stack",'),
        ("05", '  "location": "Ahmedabad, IN (23.02°N, 72.57°E)",'),
        ("06", '  "flagship_stack": ["TypeScript", "Rust Core", "Node.js", "MCP Protocol"],'),
        ("07", '  "architecture": "Subagent-Driven Development (SDD)",'),
        ("08", '  "agentic_governance": {'),
        ("09", '    "specialist_agents": 52,'),
        ("10", '    "tribunal_reviewers": 21,'),
        ("11", '    "anti_hallucination_gates": "ACTIVE"'),
        ("12", '  },'),
        ("13", '  "acf_metrics": { "compression": "27x", "hallucination_rate": "0.00%" }'),
        ("14", '}'),
    ]

    ly = 72.0
    for num, code in lines_data:
        lt = Text(x=36, y=ly, font_size=12.5)
        lt.add_span(Tspan(text=f"{num}  ", fill=COLOR_TEXT_FAINT, font_size=11.0))

        # Syntax color mapping
        if ":" in code and "{" not in code:
            parts = code.split(":", 1)
            lt.add_span(Tspan(text=parts[0] + ":", fill=COLOR_ACCENT_SKY, font_weight="600"))
            val = parts[1]
            if '"' in val:
                lt.add_span(Tspan(text=val, fill=COLOR_ACCENT_AMBER))
            elif any(d in val for d in "0123456789"):
                lt.add_span(Tspan(text=val, fill=COLOR_ACCENT_CORAL))
            else:
                lt.add_span(Tspan(text=val, fill=COLOR_TEXT_PRIMARY))
        else:
            lt.add_span(Tspan(text=code, fill=COLOR_TEXT_MUTED))

        root.add(lt)
        ly += 25.0

    # Blinking prompt cursor line
    cur_t = Text(x=36, y=ly + 8, font_size=12.5)
    cur_t.add_span(Tspan(text="15  ", fill=COLOR_TEXT_FAINT, font_size=11.0))
    cur_t.add_span(Tspan(text="harmit@system-architect:~$ ", fill=COLOR_ACCENT_CYAN, font_weight="700"))
    cur_t.add_span(Tspan(text="npx tribunal-kit init ", fill=COLOR_TEXT_PRIMARY))
    cur_t.add_span(Tspan(text="█", fill=COLOR_ACCENT_CYAN, class_name="term-cur" if animated else None))
    root.add(cur_t)

    # Bottom Verification Banner (y=452, height=44)
    audit_g = Group(transform="translate(36, 452)")
    audit_g.add(
        Rect(
            x=0,
            y=0,
            width=888,
            height=44,
            rx=8,
            fill="#06121E",
            stroke=COLOR_ACCENT_CYAN,
            stroke_width=0.8,
        )
    )
    audit_g.add(Circle(cx=22, cy=22, r=4, fill=COLOR_ACCENT_MINT, filter_id="tbGlow"))
    audit_g.add(
        Text(
            text="AUDIT PASSED // 0 HALLUCINATIONS DETECTED // ZERO-TRUST CONTRACT NOMINAL",
            x=36,
            y=26,
            font_size=11.0,
            font_weight="700",
            fill=COLOR_ACCENT_MINT,
            letter_spacing=1.0,
        )
    )
    audit_g.add(
        Text(
            text="VERIFIED SDD PROTOCOL",
            x=870,
            y=26,
            font_size=10.0,
            font_weight="700",
            text_anchor="end",
            fill=COLOR_ACCENT_CYAN,
            letter_spacing=1.0,
        )
    )
    root.add(audit_g)

    return root.render()
