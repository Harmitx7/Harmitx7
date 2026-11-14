"""Typography and text rendering primitives for SVG generation."""

import base64
import os
from typing import Dict, List, Optional
from src.svg.primitives import SvgElement
from src.utils.formatting import escape_xml

# System font stacks with embedded Geist and Geist Mono precedence
FONT_MONOSPACE = "'Geist Mono', ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Monaco, Consolas, monospace"
FONT_SANS = "Geist, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
FONT_SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"

FONT_MONO = FONT_MONOSPACE

# Cache for base64 encoded woff fonts
_FONT_CACHE: Dict[str, str] = {}
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_font_face_css(fonts: Optional[List[str]] = None) -> str:
    """Generate @font-face CSS rules with embedded Base64 WOFF data URIs.
    Supported keys: 'mono', 'sans', 'serif'
    """
    if fonts is None:
        fonts = ["mono"]

    font_files = {
        "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
        "sans": ("Geist", "normal", 400, "geist-400.woff"),
        "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
    }

    css_blocks = []
    for key in fonts:
        if key not in font_files:
            continue
        family, style, weight, filename = font_files[key]
        if key not in _FONT_CACHE:
            fpath = os.path.join(REPO_ROOT, "fonts", filename)
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    _FONT_CACHE[key] = base64.b64encode(f.read()).decode("ascii")
            else:
                _FONT_CACHE[key] = ""

        b64 = _FONT_CACHE.get(key)
        if b64:
            css_blocks.append(
                f"@font-face {{\n"
                f"  font-family: '{family}';\n"
                f"  font-style: {style};\n"
                f"  font-weight: {weight};\n"
                f"  font-display: swap;\n"
                f"  src: url('data:font/woff;base64,{b64}') format('woff');\n"
                f"}}"
            )

    return "\n".join(css_blocks)


class Tspan(SvgElement):
    """SVG <tspan> element for styled inline text spans."""

    def __init__(
        self,
        text: str,
        fill: Optional[str] = None,
        font_weight: Optional[str] = None,
        font_size: Optional[float] = None,
        class_name: Optional[str] = None,
        dx: Optional[float] = None,
        dy: Optional[float] = None,
    ):
        self.text = text
        self.fill = fill
        self.font_weight = font_weight
        self.font_size = font_size
        self.class_name = class_name
        self.dx = dx
        self.dy = dy

    def render(self) -> str:
        attrs = []
        if self.fill:
            attrs.append(f'fill="{self.fill}"')
        if self.font_weight:
            attrs.append(f'font-weight="{self.font_weight}"')
        if self.font_size:
            attrs.append(f'font-size="{self.font_size}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.dx is not None:
            attrs.append(f'dx="{self.dx}"')
        if self.dy is not None:
            attrs.append(f'dy="{self.dy}"')
        attr_str = f" {' '.join(attrs)}" if attrs else ""
        return f"<tspan{attr_str}>{escape_xml(self.text)}</tspan>"


class Text(SvgElement):
    """SVG <text> element with full system typography controls."""

    def __init__(
        self,
        text: str = "",
        x: float = 0,
        y: float = 0,
        font_family: str = FONT_MONOSPACE,
        font_size: float = 13.0,
        font_weight: str = "400",
        fill: str = "#F8FAFC",
        text_anchor: str = "start",  # start, middle, end
        letter_spacing: Optional[float] = None,
        opacity: float = 1.0,
        class_name: Optional[str] = None,
        filter_id: Optional[str] = None,
        spans: Optional[List[Tspan]] = None,
        style: Optional[str] = None,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight
        self.fill = fill
        self.text_anchor = text_anchor
        self.letter_spacing = letter_spacing
        self.opacity = opacity
        self.class_name = class_name
        self.filter_id = filter_id
        self.spans = spans or []
        self.style = style

    def add_span(self, span: Tspan) -> "Text":
        self.spans.append(span)
        return self

    def render(self) -> str:
        attrs = [
            f'x="{self.x}"',
            f'y="{self.y}"',
            f'fill="{self.fill}"',
            f'font-family="{self.font_family}"',
            f'font-size="{self.font_size}"',
        ]
        if self.font_weight != "400":
            attrs.append(f'font-weight="{self.font_weight}"')
        if self.text_anchor != "start":
            attrs.append(f'text-anchor="{self.text_anchor}"')
        if self.letter_spacing is not None:
            attrs.append(f'letter-spacing="{self.letter_spacing}"')
        if self.opacity < 1.0:
            attrs.append(f'opacity="{self.opacity:.3f}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.filter_id:
            attrs.append(f'filter="url(#{self.filter_id})"')
        if self.style:
            attrs.append(f'style="{self.style}"')

        content = escape_xml(self.text)
        if self.spans:
            content += "".join(s.render() for s in self.spans)

        return f'<text {" ".join(attrs)}>{content}</text>'
