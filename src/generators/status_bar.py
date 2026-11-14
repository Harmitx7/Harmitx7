"""Generator for the Active Shipping Telemetry Ticker (status-bar.svg)."""

from src.svg.animation import AnimationEngine, create_beacon_pulse_animation
from src.svg.filters import GlowFilter
from src.svg.gradients import create_luminous_rim_gradient, create_void_surface_gradient
from src.svg.primitives import Circle, Group, Line, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, Text, Tspan
from src.utils.colors import (
    COLOR_ACCENT_AMBER,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_TANGERINE,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)


def generate_status_bar_svg(animated: bool = True) -> str:
    """Generate the Active Shipping Telemetry Ticker SVG component."""
    root = SvgRoot(
        view_box="0 0 960 72",
        width="100%",
        title="Active Shipping Telemetry Ticker — Harmitx7",
        desc="Real-time operational status, active sprint focus, and hackathon milestones.",
    )

    root.add_def(create_void_surface_gradient("stBarVoid"))
    root.add_def(create_luminous_rim_gradient("stBarRim"))
    root.add_def(GlowFilter("stBarGlow", std_deviation=2.5))

    anim = AnimationEngine(animated=animated)
    if animated:
        create_beacon_pulse_animation(anim, cycle_seconds=2.4)
        anim.add_keyframe("constellationBreath", "0%,100%{stroke-opacity:0.08;} 50%{stroke-opacity:0.3;}")
        anim.add_class(".const-line", "animation: constellationBreath 5s ease-in-out infinite;")
    root.style_block = anim.generate_style_block()

    # Background Capsule
    root.add(
        Rect(
            x=0,
            y=0,
            width=960,
            height=72,
            rx=12,
            fill="url(#stBarVoid)",
            stroke="url(#stBarRim)",
            stroke_width=1.0,
        )
    )

    # Micro Constellation Lines
    bg_g = Group(opacity=0.5)
    bg_g.add(Line(x1=80, y1=20, x2=260, y2=50, stroke=COLOR_ACCENT_CYAN, stroke_width=0.6, class_name="const-line" if animated else None))
    bg_g.add(Line(x1=340, y1=52, x2=580, y2=22, stroke=COLOR_ACCENT_TANGERINE, stroke_width=0.6, class_name="const-line" if animated else None))
    bg_g.add(Line(x1=680, y1=24, x2=880, y2=48, stroke=COLOR_ACCENT_MINT, stroke_width=0.6, class_name="const-line" if animated else None))
    root.add(bg_g)

    # 1. Pod 1: Operational Status (x=28)
    p1 = Group(transform="translate(28, 22)")
    # Radar ripple ring
    p1.add(Circle(cx=10, cy=14, r=10, stroke=COLOR_ACCENT_MINT, stroke_width=1.0, opacity=0.4, class_name="sonar" if animated else None))
    # Glowing beacon node
    p1.add(Circle(cx=10, cy=14, r=3.5, fill=COLOR_ACCENT_MINT, filter_id="stBarGlow", class_name="beacon-node" if animated else None))
    # Label
    p1_text = Text(x=28, y=18, font_size=11.5)
    p1_text.add_span(Tspan(text="SYSTEM STATUS: ", fill=COLOR_TEXT_MUTED, font_weight="500"))
    p1_text.add_span(Tspan(text="OPERATIONAL", fill=COLOR_ACCENT_MINT, font_weight="700"))
    p1.add(p1_text)
    root.add(p1)

    # Divider 1 (x=285)
    root.add(Line(x1=285, y1=20, x2=285, y2=52, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))

    # 2. Pod 2: Active Sprint (x=305)
    p2 = Group(transform="translate(305, 22)")
    p2.add(Circle(cx=8, cy=14, r=2.5, fill=COLOR_ACCENT_CYAN))
    p2_text = Text(x=22, y=18, font_size=11.5)
    p2_text.add_span(Tspan(text="ACTIVE SPRINT: ", fill=COLOR_TEXT_MUTED, font_weight="500"))
    p2_text.add_span(Tspan(text="tribunal-kit v3.0", fill=COLOR_ACCENT_CYAN, font_weight="700"))
    p2_text.add_span(Tspan(text=" (Anti-Hallucination SDD)", fill=COLOR_TEXT_FAINT))
    p2.add(p2_text)
    root.add(p2)

    # Divider 2 (x=670)
    root.add(Line(x1=670, y1=20, x2=670, y2=52, stroke=COLOR_BORDER_SUBTLE, stroke_width=0.8))

    # 3. Pod 3: Hackathon Milestone (x=690)
    p3 = Group(transform="translate(690, 22)")
    p3.add(Circle(cx=8, cy=14, r=2.5, fill=COLOR_ACCENT_TANGERINE))
    p3_text = Text(x=22, y=18, font_size=11.5)
    p3_text.add_span(Tspan(text="BOI HACKATHON: ", fill=COLOR_TEXT_MUTED, font_weight="500"))
    p3_text.add_span(Tspan(text="WINNER", fill=COLOR_ACCENT_TANGERINE, font_weight="800"))
    p3.add(p3_text)
    root.add(p3)

    # Right Identity Anchor
    root.add(
        Text(
            text="@Harmitx7",
            x=942,
            y=40,
            font_size=10.0,
            font_weight="600",
            text_anchor="end",
            fill=COLOR_TEXT_MUTED,
            letter_spacing=0.5,
        )
    )

    return root.render()
