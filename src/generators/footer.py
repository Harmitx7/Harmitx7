"""Generator for the Geographic & Institutional Coordinate Footer (footer.svg)."""

from src.svg.animation import AnimationEngine, create_wave_flow_animation
from src.svg.filters import GlowFilter
from src.svg.gradients import LinearGradient, create_stream_gradient, create_void_surface_gradient
from src.svg.primitives import Circle, Group, Line, Path, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, Text
from src.utils.colors import (
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_SKY,
    COLOR_ACCENT_TANGERINE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
)


def generate_footer_svg(animated: bool = True) -> str:
    """Generate the Coordinate Footer SVG component."""
    root = SvgRoot(
        view_box="0 0 1000 140",
        width="100%",
        title="Engineering Verification Footer — Harmit Kalal",
        desc="Geographic coordinates (Ahmedabad, IN // 23.02°N, 72.57°E) and Indus University verification nodes.",
    )

    root.add_def(create_void_surface_gradient("footVoid"))
    root.add_def(create_stream_gradient("footStream"))
    root.add_def(GlowFilter("footGlow", std_deviation=2.0))

    anim = AnimationEngine(animated=animated)
    if animated:
        create_wave_flow_animation(anim)
        anim.add_keyframe("starPulse", "0%,100%{opacity:0.2;} 50%{opacity:0.75;}")
        anim.add_class(".f-star", "animation: starPulse 5s ease-in-out infinite;")
    root.style_block = anim.generate_style_block()

    # Outer Container
    root.add(Rect(x=0, y=0, width=1000, height=140, rx=12, fill="url(#footVoid)"))

    # Top Luminous Border
    root.add(Rect(x=0, y=0, width=1000, height=1.5, fill="url(#footStream)", opacity=0.8))

    # Background Micro Constellation Lines
    f_const = Group(opacity=0.4)
    f_const.add(Line(x1=120, y1=30, x2=350, y2=55, stroke=COLOR_ACCENT_CYAN, stroke_width=0.5, opacity=0.3))
    f_const.add(Line(x1=350, y1=55, x2=580, y2=28, stroke=COLOR_ACCENT_CYAN, stroke_width=0.5, opacity=0.3))
    f_const.add(Line(x1=580, y1=28, x2=830, y2=52, stroke=COLOR_ACCENT_TANGERINE, stroke_width=0.5, opacity=0.3))

    f_const.add(Circle(cx=120, cy=30, r=1.5, fill=COLOR_ACCENT_CYAN, class_name="f-star" if animated else None))
    f_const.add(Circle(cx=350, cy=55, r=1.5, fill=COLOR_ACCENT_CYAN, class_name="f-star" if animated else None))
    f_const.add(Circle(cx=580, cy=28, r=1.5, fill=COLOR_ACCENT_TANGERINE, class_name="f-star" if animated else None))
    f_const.add(Circle(cx=830, cy=52, r=1.5, fill=COLOR_ACCENT_MINT, class_name="f-star" if animated else None))
    root.add(f_const)

    # Harmonic Wave Vectors
    cls_wa = "wave-a" if animated else None
    cls_wb = "wave-b" if animated else None
    wave_d1 = "M 0 42 Q 125 16, 250 42 T 500 42 T 750 42 T 1000 42"
    wave_d2 = "M 0 42 Q 125 68, 250 42 T 500 42 T 750 42 T 1000 42"

    root.add(Path(d=wave_d1, fill="none", stroke="url(#footStream)", stroke_width=1.5, opacity=0.45, class_name=cls_wa))
    root.add(Path(d=wave_d2, fill="none", stroke=COLOR_ACCENT_MINT, stroke_width=1.0, opacity=0.25, class_name=cls_wb))

    # Center Location Identity & Academic Credentials
    root.add(
        Text(
            text="AHMEDABAD, IN (23.02°N, 72.57°E) · COMPUTER ENGINEERING · INDUS UNIVERSITY",
            x=500,
            y=84,
            font_size=11.0,
            font_weight="600",
            text_anchor="middle",
            fill=COLOR_TEXT_MUTED,
            letter_spacing=2.0,
        )
    )

    # Bottom Verification Nodes
    nodes_g = Group(transform="translate(500, 116)")
    nodes_g.add(Circle(cx=-24, cy=0, r=2.5, fill=COLOR_ACCENT_CYAN))
    nodes_g.add(Circle(cx=-8, cy=0, r=2.5, fill=COLOR_ACCENT_SKY))
    nodes_g.add(Circle(cx=8, cy=0, r=2.5, fill=COLOR_ACCENT_TANGERINE))
    nodes_g.add(Circle(cx=24, cy=0, r=2.5, fill=COLOR_ACCENT_MINT))
    root.add(nodes_g)

    return root.render()
