"""Generator for the cinematic Hero Cyber-HUD banner (hero.svg)."""

from src.svg.animation import AnimationEngine, create_orbital_animation
from src.svg.filters import GlowFilter
from src.svg.gradients import (
    LinearGradient,
    RadialGradient,
    create_luminous_rim_gradient,
    create_void_surface_gradient,
)
from src.svg.primitives import Circle, Group, Line, Path, Rect, SvgRoot
from src.svg.typography import FONT_MONOSPACE, FONT_SANS, Text
from src.utils.colors import (
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_TANGERINE,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


def generate_hero_svg(animated: bool = True) -> str:
    """Generate the Hero Cyber-HUD SVG component."""
    root = SvgRoot(
        view_box="0 0 1000 400",
        width="100%",
        title="Harmit Kalal — AI Systems Architect & Creative Engineer",
        desc="Cinematic Editorial HUD banner with celestial orbital physics, geographic coordinates, and engineering mandate.",
    )

    # Gradients & Filters
    root.add_def(create_void_surface_gradient("heroVoid"))
    root.add_def(create_luminous_rim_gradient("heroRim"))

    # Core Glow Radial Gradient
    root.add_def(
        RadialGradient(
            id_name="coreGlow",
            cx="50%",
            cy="50%",
            r="50%",
            stops=[
                ("0%", COLOR_ACCENT_CYAN, 0.4),
                ("40%", COLOR_ACCENT_CYAN, 0.1),
                ("100%", COLOR_ACCENT_CYAN, 0.0),
            ],
        )
    )

    # Name Iridescent Gradient
    root.add_def(
        LinearGradient(
            id_name="nameGrad",
            x1="0%",
            y1="0%",
            x2="100%",
            y2="0%",
            stops=[
                ("0%", "#FFFFFF", 1.0),
                ("40%", "#F1F5F9", 1.0),
                ("75%", "#CBD5E1", 1.0),
                ("100%", "#64748B", 1.0),
            ],
        )
    )

    root.add_def(GlowFilter("optGlow", std_deviation=2.5))

    # Animation
    anim = AnimationEngine(animated=animated)
    if animated:
        create_orbital_animation(anim, center_x=770.0, center_y=195.0, durations=[22.0, 15.0, 32.0])
        anim.add_keyframe("pulseNode", "0%,100%{opacity:0.7;r:6;} 50%{opacity:1;r:8.5;}")
        anim.add_class(".core-node", "animation: pulseNode 3s ease-in-out infinite;")
        anim.add_keyframe("starTwinkle", "0%,100%{opacity:0.25;} 50%{opacity:0.85;}")
        anim.add_class(".bg-star", "animation: starTwinkle 4s ease-in-out infinite;")
    root.style_block = anim.generate_style_block()

    # 1. Main Capsule Canvas
    root.add(
        Rect(
            x=0,
            y=0,
            width=1000,
            height=400,
            rx=14,
            fill="url(#heroVoid)",
            stroke="url(#heroRim)",
            stroke_width=1.2,
        )
    )

    # 2. Subtle Micro-Grid & Constellation Points
    grid_g = Group(opacity=0.6)
    stars = [
        (80, 60), (220, 85), (450, 45), (150, 330), (380, 340), (560, 310),
        (650, 80), (890, 65), (920, 320), (620, 220)
    ]
    for i, (sx, sy) in enumerate(stars):
        cls = "bg-star" if animated else None
        delay = f"animation-delay: {i * 0.4:.1f}s;" if animated else None
        grid_g.add(Circle(cx=sx, cy=sy, r=1.5, fill="#38BDF8", opacity=0.4, class_name=cls, style=delay))
    root.add(grid_g)

    # 3. Left Zone: Technical Identity & Mandate
    id_g = Group()

    # Location & Coordinate Stamp
    id_g.add(
        Text(
            text="23.02°N, 72.57°E // AHMEDABAD, IN",
            x=60,
            y=68,
            font_size=10.5,
            font_weight="600",
            fill=COLOR_TEXT_MUTED,
            letter_spacing=2.0,
        )
    )

    # Primary Display Name
    id_g.add(
        Text(
            text="Harmit Kalal",
            x=60,
            y=132,
            font_family=FONT_SANS,
            font_size=46.0,
            font_weight="800",
            fill="url(#nameGrad)",
            letter_spacing=-1.2,
        )
    )

    # Architectural Mandate
    id_g.add(
        Text(
            text="AI SYSTEMS ARCHITECT // DISTRIBUTED INFRASTRUCTURE",
            x=62,
            y=175,
            font_size=12.5,
            font_weight="700",
            fill=COLOR_ACCENT_CYAN,
            letter_spacing=1.5,
        )
    )

    # Subtitle Manifesto
    id_g.add(
        Text(
            text="Engineering deterministic agents, zero-trust governance, and sub-millisecond telemetry.",
            x=62,
            y=208,
            font_family=FONT_SANS,
            font_size=13.5,
            fill=COLOR_TEXT_SECONDARY,
        )
    )

    # Core Engineering Pillars (Pill Matrix)
    pillars = [
        ("◈ AGENTIC GOVERNANCE", "tribunal-kit // 52 agents // SDD", COLOR_ACCENT_CYAN),
        ("◈ MALWARE DECEPTION", "ARGUS-X // BoI × IIT-H Winner", COLOR_ACCENT_TANGERINE),
        ("◈ TELEMETRY SIMULATION", "F1 Engine // Sub-ms physics", COLOR_ACCENT_MINT),
    ]

    p_y = 254
    for title, desc, color in pillars:
        # Indicator tick
        id_g.add(Rect(x=62, y=p_y - 10, width=3, height=14, rx=1.5, fill=color))
        id_g.add(Text(text=title, x=74, y=p_y, font_size=11.0, font_weight="700", fill=color, letter_spacing=0.8))
        id_g.add(Text(text=f"— {desc}", x=270, y=p_y, font_size=11.0, font_weight="400", fill=COLOR_TEXT_MUTED))
        p_y += 32

    root.add(id_g)

    # 4. Right Zone: Orbital Celestial Engine (cx=770, cy=195)
    cx, cy = 770.0, 195.0
    orbit_g = Group()

    # Ambient Background Radial Glow
    orbit_g.add(Circle(cx=cx, cy=cy, r=140, fill="url(#coreGlow)", opacity=0.8))

    # Fixed Orbital Paths
    orbit_g.add(
        Path(
            d=f"M {cx-130} {cy} a 130 52 0 1 0 260 0 a 130 52 0 1 0 -260 0",
            fill="none",
            stroke=COLOR_ACCENT_CYAN,
            stroke_width=1.0,
            opacity=0.35,
            style="transform: rotate(-28deg); transform-origin: 770px 195px;",
        )
    )
    orbit_g.add(
        Path(
            d=f"M {cx-105} {cy} a 105 44 0 1 0 210 0 a 105 44 0 1 0 -210 0",
            fill="none",
            stroke=COLOR_ACCENT_TANGERINE,
            stroke_width=1.0,
            opacity=0.35,
            style="transform: rotate(38deg); transform-origin: 770px 195px;",
        )
    )
    orbit_g.add(
        Path(
            d=f"M {cx-155} {cy} a 155 64 0 1 0 310 0 a 155 64 0 1 0 -310 0",
            fill="none",
            stroke=COLOR_ACCENT_MINT,
            stroke_width=0.8,
            opacity=0.3,
            style="transform: rotate(-72deg); transform-origin: 770px 195px;",
        )
    )

    # Rotating Electron Pods
    cls_a = "orbit-a" if animated else None
    cls_b = "orbit-b" if animated else None
    cls_c = "orbit-c" if animated else None

    # Electron A (Cyan)
    orbit_g.add(
        Group(
            children=[Circle(cx=cx + 130, cy=cy, r=4.5, fill=COLOR_ACCENT_CYAN, filter_id="optGlow")],
            class_name=cls_a,
            style="transform-box: view-box; transform: rotate(-28deg);",
        )
    )

    # Electron B (Tangerine)
    orbit_g.add(
        Group(
            children=[Circle(cx=cx - 105, cy=cy, r=4.5, fill=COLOR_ACCENT_TANGERINE, filter_id="optGlow")],
            class_name=cls_b,
            style="transform-box: view-box; transform: rotate(38deg);",
        )
    )

    # Electron C (Mint)
    orbit_g.add(
        Group(
            children=[Circle(cx=cx + 155, cy=cy, r=4.0, fill=COLOR_ACCENT_MINT, filter_id="optGlow")],
            class_name=cls_c,
            style="transform-box: view-box; transform: rotate(-72deg);",
        )
    )

    # Core Central Node
    cls_core = "core-node" if animated else None
    orbit_g.add(Circle(cx=cx, cy=cy, r=7.0, fill=COLOR_ACCENT_CYAN, filter_id="optGlow", class_name=cls_core))
    orbit_g.add(Circle(cx=cx, cy=cy, r=2.5, fill="#FFFFFF"))

    root.add(orbit_g)

    # 5. Bottom Verification Border
    root.add(
        Text(
            text="STATUS: 99.99% UPTIME // SUBAGENT-DRIVEN DEVELOPMENT ACTIVE // 0 HALLUCINATIONS DETECTED",
            x=62,
            y=372,
            font_size=10.0,
            font_weight="600",
            fill=COLOR_TEXT_FAINT,
            letter_spacing=1.5,
        )
    )

    return root.render()
