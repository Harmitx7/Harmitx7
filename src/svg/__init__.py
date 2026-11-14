"""SVG generation primitives, typography, gradients, filters, animation, and layouts."""

from src.svg.primitives import (
    SvgElement,
    Rect,
    Circle,
    Line,
    Path,
    Group,
    SvgRoot,
)

from src.svg.typography import (
    Text,
    Tspan,
    FONT_MONOSPACE,
    FONT_SANS,
)

from src.svg.gradients import (
    LinearGradient,
    RadialGradient,
    create_void_surface_gradient,
    create_luminous_rim_gradient,
    create_stream_gradient,
)

from src.svg.filters import (
    GlowFilter,
    DropShadowFilter,
)

from src.svg.animation import (
    AnimationEngine,
    create_beacon_pulse_animation,
    create_orbital_animation,
    create_wave_flow_animation,
)

from src.svg.layouts import (
    CardLayout,
    SegmentedProgressBar,
    MetricPod,
)

__all__ = [
    "SvgElement",
    "Rect",
    "Circle",
    "Line",
    "Path",
    "Group",
    "SvgRoot",
    "Text",
    "Tspan",
    "FONT_MONOSPACE",
    "FONT_SANS",
    "LinearGradient",
    "RadialGradient",
    "create_void_surface_gradient",
    "create_luminous_rim_gradient",
    "create_stream_gradient",
    "GlowFilter",
    "DropShadowFilter",
    "AnimationEngine",
    "create_beacon_pulse_animation",
    "create_orbital_animation",
    "create_wave_flow_animation",
    "CardLayout",
    "SegmentedProgressBar",
    "MetricPod",
]
