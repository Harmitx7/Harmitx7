"""SVG gradient definitions and preset constructors."""

from typing import List, Tuple
from src.svg.primitives import SvgElement


class LinearGradient(SvgElement):
    """SVG <linearGradient> definition."""

    def __init__(
        self,
        id_name: str,
        x1: str = "0%",
        y1: str = "0%",
        x2: str = "100%",
        y2: str = "0%",
        stops: List[Tuple[str, str, float]] = None,  # (offset, stop-color, stop-opacity)
    ):
        self.id_name = id_name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stops = stops or []

    def render(self) -> str:
        attrs = [
            f'id="{self.id_name}"',
            f'x1="{self.x1}"',
            f'y1="{self.y1}"',
            f'x2="{self.x2}"',
            f'y2="{self.y2}"',
        ]
        lines = [f'<linearGradient {" ".join(attrs)}>']
        for offset, color, opacity in self.stops:
            stop_attrs = [f'offset="{offset}"', f'stop-color="{color}"']
            if opacity < 1.0:
                stop_attrs.append(f'stop-opacity="{opacity:.3f}"')
            lines.append(f'  <stop {" ".join(stop_attrs)}/>')
        lines.append("</linearGradient>")
        return "\n".join(lines)


class RadialGradient(SvgElement):
    """SVG <radialGradient> definition."""

    def __init__(
        self,
        id_name: str,
        cx: str = "50%",
        cy: str = "50%",
        r: str = "50%",
        fx: str = None,
        fy: str = None,
        stops: List[Tuple[str, str, float]] = None,
    ):
        self.id_name = id_name
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fx = fx or cx
        self.fy = fy or cy
        self.stops = stops or []

    def render(self) -> str:
        attrs = [
            f'id="{self.id_name}"',
            f'cx="{self.cx}"',
            f'cy="{self.cy}"',
            f'r="{self.r}"',
            f'fx="{self.fx}"',
            f'fy="{self.fy}"',
        ]
        lines = [f'<radialGradient {" ".join(attrs)}>']
        for offset, color, opacity in self.stops:
            stop_attrs = [f'offset="{offset}"', f'stop-color="{color}"']
            if opacity < 1.0:
                stop_attrs.append(f'stop-opacity="{opacity:.3f}"')
            lines.append(f'  <stop {" ".join(stop_attrs)}/>')
        lines.append("</radialGradient>")
        return "\n".join(lines)


# Presets
def create_void_surface_gradient(id_name: str) -> LinearGradient:
    """Create a deep obsidian capsule surface gradient."""
    return LinearGradient(
        id_name=id_name,
        x1="0%",
        y1="0%",
        x2="100%",
        y2="100%",
        stops=[
            ("0%", "#030509", 1.0),
            ("50%", "#090E1A", 1.0),
            ("100%", "#030509", 1.0),
        ],
    )


def create_luminous_rim_gradient(id_name: str) -> LinearGradient:
    """Create a high-precision hairline border gradient (Cyan -> Muted Dark -> Tangerine)."""
    return LinearGradient(
        id_name=id_name,
        x1="0%",
        y1="0%",
        x2="100%",
        y2="100%",
        stops=[
            ("0%", "#00F0FF", 0.6),
            ("35%", "#0F172A", 0.15),
            ("70%", "#1E293B", 0.15),
            ("100%", "#FF6B00", 0.6),
        ],
    )


def create_stream_gradient(id_name: str) -> LinearGradient:
    """Create a multi-stop harmonic waveform gradient."""
    return LinearGradient(
        id_name=id_name,
        x1="0%",
        y1="0%",
        x2="100%",
        y2="0%",
        stops=[
            ("0%", "#00F0FF", 0.8),
            ("40%", "#38BDF8", 0.8),
            ("70%", "#FF9100", 0.8),
            ("100%", "#FF5722", 0.8),
        ],
    )
