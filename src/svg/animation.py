"""
SVG Motion Design System: Hardware-accelerated CSS keyframe animations,
timing tokens, easing curves, and strict accessibility fallbacks for GitHub.
"""

import os
from typing import Dict, List, Optional


class AnimationEngine:
    """
    Manages CSS animation generation for SVG components.
    Enforces GitHub rendering compatibility:
    - Pure CSS @keyframes (no JavaScript, no SMIL)
    - Hardware-accelerated properties only (transform, opacity, stroke-dashoffset)
    - Zero layout thrashing (no width, height, x, y animations)
    - Mandatory @media (prefers-reduced-motion: reduce) fallback
    - Deterministic, collision-free CSS class and keyframe generation
    - Supports STATIC=1 environment variable for instant static final-frame mode
    """

    def __init__(self, animated: Optional[bool] = None):
        if animated is None:
            # STATIC=1 environment override
            self.animated = os.environ.get("STATIC") != "1"
        else:
            if os.environ.get("STATIC") == "1":
                self.animated = False
            else:
                self.animated = animated

        self.keyframes: Dict[str, str] = {}
        self.classes: Dict[str, str] = {}
        self.reduced_motion_overrides: Dict[str, str] = {}

    def add_keyframe(self, name: str, css_body: str) -> "AnimationEngine":
        """Register a unique @keyframes definition."""
        self.keyframes[name] = css_body.strip()
        return self

    def add_class(
        self,
        selector: str,
        properties: str,
        reduced_motion_override: Optional[str] = "animation: none !important; opacity: 1 !important;",
    ) -> "AnimationEngine":
        """Register a CSS class selector with animation properties and reduced-motion fallback."""
        self.classes[selector] = properties.strip()
        if reduced_motion_override:
            self.reduced_motion_overrides[selector] = reduced_motion_override.strip()
        return self

    def generate_style_block(self) -> str:
        """
        Generate the complete <style> block.
        If animated=False, emits a pure static stylesheet ensuring 100% visibility.
        """
        if not self.animated:
            return """
    /* ═══════════════════════════════════════════════════════════
       STATIC ACCESSIBILITY MODE: Animations disabled
       ═══════════════════════════════════════════════════════════ */
    * { animation: none !important; opacity: 1 !important; }
    text { font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Consolas, monospace; }
"""

        lines: List[str] = []

        # 1. Base typography declaration
        lines.append("text { font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Consolas, monospace; }")

        # 2. Keyframe definitions
        for name, body in sorted(self.keyframes.items()):
            lines.append(f"@keyframes {name} {{ {body} }}")

        # 3. Class animation attachments
        for selector, props in sorted(self.classes.items()):
            lines.append(f"{selector} {{ {props} }}")

        # 4. Mandatory Accessibility Barrier: prefers-reduced-motion
        lines.append("@media (prefers-reduced-motion: reduce) {")
        for selector, override in sorted(self.reduced_motion_overrides.items()):
            lines.append(f"  {selector} {{ {override} }}")
        lines.append("}")

        return "\n    ".join(lines)


# ═════════════════════════════════════════════════════════════════════════
# PRE-ENGINEERED MOTION PRESETS
# ═════════════════════════════════════════════════════════════════════════

def create_orbital_animation(
    engine: AnimationEngine,
    center_x: float,
    center_y: float,
    durations: List[float] = [22.0, 15.0, 32.0],
) -> None:
    """
    Celestial orbital revolution presets with transform-box: view-box.
    Ensures anchor stability across fluid viewports without center drift.
    """
    engine.add_keyframe("orbitA", "0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);}")
    engine.add_keyframe("orbitB", "0%{transform:rotate(360deg);} 100%{transform:rotate(0deg);}")
    engine.add_keyframe("orbitC", "0%{transform:rotate(180deg);} 100%{transform:rotate(540deg);}")

    engine.add_class(
        ".orbit-a",
        f"transform-origin: {center_x}px {center_y}px; transform-box: view-box; animation: orbitA {durations[0]}s linear infinite;",
    )
    engine.add_class(
        ".orbit-b",
        f"transform-origin: {center_x}px {center_y}px; transform-box: view-box; animation: orbitB {durations[1]}s linear infinite;",
    )
    engine.add_class(
        ".orbit-c",
        f"transform-origin: {center_x}px {center_y}px; transform-box: view-box; animation: orbitC {durations[2]}s linear infinite;",
    )


def create_beacon_pulse_animation(engine: AnimationEngine, cycle_seconds: float = 2.4) -> None:
    """
    Live operational sonar radar beacon with expanding concentric ripple ring.
    Communicates live system heartbeat without aggressive distraction.
    """
    engine.add_keyframe("sonarRipple", "0%{r:4;opacity:0.9;} 100%{r:16;opacity:0;}")
    engine.add_keyframe("nodeGlow", "0%,100%{opacity:0.6;r:3;} 50%{opacity:1;r:4.5;}")

    engine.add_class(".sonar", f"animation: sonarRipple {cycle_seconds}s cubic-bezier(0.16, 1, 0.3, 1) infinite;")
    engine.add_class(".beacon-node", f"animation: nodeGlow {cycle_seconds}s ease-in-out infinite;")


def create_wave_flow_animation(engine: AnimationEngine, period_a: float = 9.0, period_b: float = 12.0) -> None:
    """
    Animated SVG path stroke drawing via stroke-dasharray and stroke-dashoffset.
    Produces a continuous, fluid telemetry waveform.
    """
    engine.add_keyframe("wavePhaseA", "0%{stroke-dashoffset:0;} 100%{stroke-dashoffset:-500;}")
    engine.add_keyframe("wavePhaseB", "0%{stroke-dashoffset:-500;} 100%{stroke-dashoffset:0;}")

    engine.add_class(".wave-a", f"stroke-dasharray: 14 8; animation: wavePhaseA {period_a}s linear infinite;")
    engine.add_class(".wave-b", f"stroke-dasharray: 10 12; animation: wavePhaseB {period_b}s linear infinite;")


def register_starlight_twinkle(engine: AnimationEngine, period: float = 4.0) -> None:
    """Subtle starlight twinkle for micro-grid coordinate constellations."""
    engine.add_keyframe("starTwinkle", "0%,100%{opacity:0.25;} 50%{opacity:0.85;}")
    engine.add_class(".bg-star", f"animation: starTwinkle {period}s ease-in-out infinite;")


def register_card_glow_pulse(engine: AnimationEngine, period: float = 4.0) -> None:
    """Subtle hairline border glow breathing cycle for active project dossiers."""
    engine.add_keyframe("cardBorderBreath", "0%,100%{stroke-opacity:0.25;} 50%{stroke-opacity:0.65;}")
    engine.add_class(".glow-border", f"animation: cardBorderBreath {period}s ease-in-out infinite;")


def register_progress_reveal(engine: AnimationEngine, duration: float = 0.6) -> None:
    """Horizontal scale reveal for data visualization progress bars."""
    engine.add_keyframe("barScaleReveal", "0%{opacity:0;transform:scaleX(0.85);} 100%{opacity:1;transform:scaleX(1);}")
    engine.add_class(".spectrum-bar", f"animation: barScaleReveal {duration}s cubic-bezier(0.16, 1, 0.3, 1) forwards;")


def register_terminal_cursor_blink(engine: AnimationEngine, period: float = 0.85) -> None:
    """Monospace terminal block cursor blink cycle."""
    engine.add_keyframe("terminalCursor", "0%,49%{opacity:1;} 50%,100%{opacity:0;}")
    engine.add_class(".term-cur", f"animation: terminalCursor {period}s step-end infinite;")
