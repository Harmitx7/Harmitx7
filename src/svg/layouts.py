"""Composite visual layout components: Capsules, Grid Systems, Progress Bars, and HUD Pods."""

from typing import List, Optional, Tuple
from src.svg.primitives import Circle, Group, Line, Rect, SvgElement
from src.svg.typography import FONT_MONOSPACE, FONT_SANS, Text
from src.utils.colors import (
    COLOR_BG_ELEVATED,
    COLOR_BG_SURFACE,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_FAINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
)
from src.utils.formatting import escape_xml, truncate_text


class CardLayout(SvgElement):
    """Encapsulated card container with dark surface and hairline gradient border."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rx: float = 12.0,
        fill_id: str = "cardBg",
        stroke_id: str = "cardRim",
        stroke_width: float = 1.0,
        has_window_controls: bool = False,
        header_title: Optional[str] = None,
        header_right_text: Optional[str] = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.fill_id = fill_id
        self.stroke_id = stroke_id
        self.stroke_width = stroke_width
        self.has_window_controls = has_window_controls
        self.header_title = header_title
        self.header_right_text = header_right_text

    def render(self) -> str:
        g = Group()

        # Background rectangle
        g.add(
            Rect(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                rx=self.rx,
                fill=f"url(#{self.fill_id})",
                stroke=f"url(#{self.stroke_id})",
                stroke_width=self.stroke_width,
            )
        )

        # Optional window controls & header
        if self.has_window_controls or self.header_title:
            header_h = 38.0
            # Header separator line
            g.add(
                Line(
                    x1=self.x,
                    y1=self.y + header_h,
                    x2=self.x + self.width,
                    y2=self.y + header_h,
                    stroke=COLOR_BORDER_SUBTLE,
                    stroke_width=0.8,
                )
            )

            # Window dots
            if self.has_window_controls:
                dot_y = self.y + 19.0
                g.add(Circle(cx=self.x + 24, cy=dot_y, r=5.5, fill="#FB7185", opacity=0.85))
                g.add(Circle(cx=self.x + 40, cy=dot_y, r=5.5, fill="#FBBF24", opacity=0.85))
                g.add(Circle(cx=self.x + 56, cy=dot_y, r=5.5, fill="#34D399", opacity=0.85))

            # Header title
            if self.header_title:
                title_x = self.x + (78.0 if self.has_window_controls else 24.0)
                g.add(
                    Text(
                        text=self.header_title,
                        x=title_x,
                        y=self.y + 23.0,
                        font_size=11.5,
                        font_weight="600",
                        fill=COLOR_TEXT_MUTED,
                    )
                )

            # Header right text
            if self.header_right_text:
                g.add(
                    Text(
                        text=self.header_right_text,
                        x=self.x + self.width - 24.0,
                        y=self.y + 23.0,
                        font_size=11.0,
                        font_weight="500",
                        text_anchor="end",
                        fill=COLOR_TEXT_FAINT,
                    )
                )

        return g.render()


class SegmentedProgressBar(SvgElement):
    """Proportional multi-segment horizontal progress bar (e.g. for language spectrums)."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float = 12.0,
        rx: float = 6.0,
        segments: List[Tuple[str, float, str]] = None,  # (label, percentage_0_to_100, hex_color)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.segments = segments or []

    def render(self) -> str:
        g = Group()

        # Background track
        g.add(
            Rect(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                rx=self.rx,
                fill=COLOR_BG_SURFACE,
                stroke=COLOR_BORDER_SUBTLE,
                stroke_width=0.8,
            )
        )

        # Segments
        current_x = self.x
        for i, (label, pct, color) in enumerate(self.segments):
            seg_w = (pct / 100.0) * self.width
            if seg_w < 1.0:
                continue

            # First and last segments retain corner radii
            r_left = self.rx if i == 0 else 0
            r_right = self.rx if i == len(self.segments) - 1 else 0

            # Render segment rect
            g.add(
                Rect(
                    x=current_x,
                    y=self.y,
                    width=seg_w,
                    height=self.height,
                    rx=r_left,
                    fill=color,
                    opacity=0.92,
                )
            )
            current_x += seg_w

        return g.render()


class MetricPod(SvgElement):
    """Individual modular telemetry pod with label, prominent number, and status subtitle."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        label: str,
        value: str,
        accent_color: str,
        subtitle: Optional[str] = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.value = value
        self.accent_color = accent_color
        self.subtitle = subtitle

    def render(self) -> str:
        g = Group()

        # Background capsule
        g.add(
            Rect(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                rx=10.0,
                fill=COLOR_BG_SURFACE,
                stroke=COLOR_BORDER_SUBTLE,
                stroke_width=1.0,
            )
        )

        # Top indicator accent tick
        g.add(
            Rect(
                x=self.x + 16,
                y=self.y + 14,
                width=24,
                height=2.5,
                rx=1.25,
                fill=self.accent_color,
            )
        )

        # Micro label
        g.add(
            Text(
                text=self.label.upper(),
                x=self.x + 16,
                y=self.y + 34,
                font_size=10.0,
                font_weight="600",
                fill=COLOR_TEXT_MUTED,
                letter_spacing=1.5,
            )
        )

        # Prominent display number
        g.add(
            Text(
                text=self.value,
                x=self.x + 16,
                y=self.y + 70,
                font_size=28.0,
                font_weight="800",
                fill=COLOR_TEXT_PRIMARY,
            )
        )

        # Optional subtitle / context
        if self.subtitle:
            g.add(
                Text(
                    text=self.subtitle,
                    x=self.x + 16,
                    y=self.y + 88,
                    font_size=10.5,
                    font_weight="500",
                    fill=COLOR_TEXT_FAINT,
                )
            )

        return g.render()
