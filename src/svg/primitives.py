"""Reusable, strongly typed SVG geometric primitives."""

from typing import List, Optional
from src.utils.formatting import escape_xml


class SvgElement:
    """Base class for all SVG nodes."""

    def render(self) -> str:
        raise NotImplementedError("Subclasses must implement render().")


class Rect(SvgElement):
    """SVG <rect> element."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rx: float = 0,
        ry: float = 0,
        fill: str = "none",
        stroke: str = "none",
        stroke_width: float = 0,
        opacity: float = 1.0,
        class_name: Optional[str] = None,
        style: Optional[str] = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.opacity = opacity
        self.class_name = class_name
        self.style = style

    def render(self) -> str:
        attrs = [
            f'x="{self.x}"',
            f'y="{self.y}"',
            f'width="{self.width}"',
            f'height="{self.height}"',
        ]
        if self.rx > 0:
            attrs.append(f'rx="{self.rx}"')
        if self.ry > 0:
            attrs.append(f'ry="{self.ry}"')
        if self.fill != "none":
            attrs.append(f'fill="{self.fill}"')
        else:
            attrs.append('fill="none"')
        if self.stroke != "none":
            attrs.append(f'stroke="{self.stroke}"')
            if self.stroke_width > 0:
                attrs.append(f'stroke-width="{self.stroke_width}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        return f'<rect {" ".join(attrs)}/>'


class Circle(SvgElement):
    """SVG <circle> element."""

    def __init__(
        self,
        cx: float,
        cy: float,
        r: float,
        fill: str = "none",
        stroke: str = "none",
        stroke_width: float = 0,
        opacity: float = 1.0,
        class_name: Optional[str] = None,
        style: Optional[str] = None,
        filter_id: Optional[str] = None,
    ):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.opacity = opacity
        self.class_name = class_name
        self.style = style
        self.filter_id = filter_id

    def render(self) -> str:
        attrs = [f'cx="{self.cx}"', f'cy="{self.cy}"', f'r="{self.r}"']
        if self.fill != "none":
            attrs.append(f'fill="{self.fill}"')
        else:
            attrs.append('fill="none"')
        if self.stroke != "none":
            attrs.append(f'stroke="{self.stroke}"')
            if self.stroke_width > 0:
                attrs.append(f'stroke-width="{self.stroke_width}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        if self.filter_id:
            attrs.append(f'filter="url(#{self.filter_id})"')
        return f'<circle {" ".join(attrs)}/>'


class Line(SvgElement):
    """SVG <line> element."""

    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = "#1E293B",
        stroke_width: float = 1.0,
        stroke_dasharray: Optional[str] = None,
        opacity: float = 1.0,
        class_name: Optional[str] = None,
        style: Optional[str] = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.opacity = opacity
        self.class_name = class_name
        self.style = style

    def render(self) -> str:
        attrs = [
            f'x1="{self.x1}"',
            f'y1="{self.y1}"',
            f'x2="{self.x2}"',
            f'y2="{self.y2}"',
            f'stroke="{self.stroke}"',
            f'stroke-width="{self.stroke_width}"',
        ]
        if self.stroke_dasharray:
            attrs.append(f'stroke-dasharray="{self.stroke_dasharray}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        return f'<line {" ".join(attrs)}/>'


class Path(SvgElement):
    """SVG <path> element."""

    def __init__(
        self,
        d: str,
        fill: str = "none",
        stroke: str = "none",
        stroke_width: float = 0,
        stroke_dasharray: Optional[str] = None,
        stroke_dashoffset: Optional[float] = None,
        opacity: float = 1.0,
        class_name: Optional[str] = None,
        style: Optional[str] = None,
    ):
        self.d = d
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.stroke_dashoffset = stroke_dashoffset
        self.opacity = opacity
        self.class_name = class_name
        self.style = style

    def render(self) -> str:
        attrs = [f'd="{self.d}"']
        attrs.append(f'fill="{self.fill}"')
        if self.stroke != "none":
            attrs.append(f'stroke="{self.stroke}"')
            if self.stroke_width > 0:
                attrs.append(f'stroke-width="{self.stroke_width}"')
        if self.stroke_dasharray:
            attrs.append(f'stroke-dasharray="{self.stroke_dasharray}"')
        if self.stroke_dashoffset is not None:
            attrs.append(f'stroke-dashoffset="{self.stroke_dashoffset}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        return f'<path {" ".join(attrs)}/>'


class Group(SvgElement):
    """SVG <g> container element."""

    def __init__(
        self,
        children: Optional[List[SvgElement]] = None,
        id_name: Optional[str] = None,
        class_name: Optional[str] = None,
        transform: Optional[str] = None,
        opacity: float = 1.0,
        style: Optional[str] = None,
    ):
        self.children = children or []
        self.id_name = id_name
        self.class_name = class_name
        self.transform = transform
        self.opacity = opacity
        self.style = style

    def add(self, child: SvgElement) -> "Group":
        self.children.append(child)
        return self

    def render(self) -> str:
        attrs = []
        if self.id_name:
            attrs.append(f'id="{self.id_name}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.transform:
            attrs.append(f'transform="{self.transform}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        attr_str = f" {' '.join(attrs)}" if attrs else ""
        inner = "\n  ".join(child.render() for child in self.children)
        return f"<g{attr_str}>\n  {inner}\n</g>"


class SvgRoot(SvgElement):
    """Root <svg> container with responsive viewBox and accessibility attributes."""

    def __init__(
        self,
        view_box: str,
        width: str = "100%",
        height: Optional[str] = None,
        defs: Optional[List[SvgElement]] = None,
        children: Optional[List[SvgElement]] = None,
        style_block: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
    ):
        self.view_box = view_box
        self.width = width
        self.height = height
        self.defs = defs or []
        self.children = children or []
        self.style_block = style_block
        self.title = title
        self.desc = desc

    def add_def(self, def_element: SvgElement) -> "SvgRoot":
        self.defs.append(def_element)
        return self

    def add(self, child: SvgElement) -> "SvgRoot":
        self.children.append(child)
        return self

    def render(self) -> str:
        attrs = [
            f'width="{self.width}"',
            f'viewBox="{self.view_box}"',
            'fill="none"',
            'xmlns="http://www.w3.org/2000/svg"',
            'role="img"',
        ]
        if self.height:
            attrs.append(f'height="{self.height}"')

        lines = [f'<svg {" ".join(attrs)}>']

        if self.title:
            lines.append(f"  <title>{escape_xml(self.title)}</title>")
        if self.desc:
            lines.append(f"  <desc>{escape_xml(self.desc)}</desc>")

        # <defs> block
        if self.defs:
            lines.append("  <defs>")
            for d in self.defs:
                lines.append(f"    {d.render()}")
            lines.append("  </defs>")

        # <style> block
        if self.style_block:
            lines.append("  <style>")
            lines.append(f"    {self.style_block}")
            lines.append("  </style>")

        # Child elements
        for child in self.children:
            lines.append(f"  {child.render()}")

        lines.append("</svg>")
        return "\n".join(lines)
