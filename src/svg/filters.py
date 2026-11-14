"""Controlled SVG filter primitives."""

from src.svg.primitives import SvgElement


class GlowFilter(SvgElement):
    """Subtle luminous optical glow filter."""

    def __init__(self, id_name: str, std_deviation: float = 2.5):
        self.id_name = id_name
        self.std_deviation = std_deviation

    def render(self) -> str:
        return f"""<filter id="{self.id_name}" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="{self.std_deviation}" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>"""


class DropShadowFilter(SvgElement):
    """Hardware-friendly drop shadow filter."""

    def __init__(
        self,
        id_name: str,
        dx: float = 0,
        dy: float = 4,
        std_deviation: float = 6,
        flood_color: str = "#000000",
        flood_opacity: float = 0.5,
    ):
        self.id_name = id_name
        self.dx = dx
        self.dy = dy
        self.std_deviation = std_deviation
        self.flood_color = flood_color
        self.flood_opacity = flood_opacity

    def render(self) -> str:
        return f"""<filter id="{self.id_name}" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="{self.dx}" dy="{self.dy}" stdDeviation="{self.std_deviation}" flood-color="{self.flood_color}" flood-opacity="{self.flood_opacity:.2f}"/>
</filter>"""
