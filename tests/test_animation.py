"""Unit tests for the SVG Motion Design System and AnimationEngine."""

import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.svg.animation import (
    AnimationEngine,
    create_beacon_pulse_animation,
    create_orbital_animation,
    create_wave_flow_animation,
    register_card_glow_pulse,
    register_progress_reveal,
    register_starlight_twinkle,
    register_terminal_cursor_blink,
)


class TestAnimationEngine(unittest.TestCase):
    def test_empty_engine_animated(self):
        engine = AnimationEngine(animated=True)
        css = engine.generate_style_block()
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("ui-monospace", css)

    def test_static_engine_mode(self):
        engine = AnimationEngine(animated=False)
        css = engine.generate_style_block()
        self.assertIn("STATIC ACCESSIBILITY MODE", css)
        self.assertIn("animation: none !important", css)
        self.assertNotIn("@keyframes", css)

    def test_orbital_physics_registration(self):
        engine = AnimationEngine(animated=True)
        create_orbital_animation(engine, center_x=770, center_y=195)
        css = engine.generate_style_block()

        self.assertIn("@keyframes orbitA", css)
        self.assertIn("@keyframes orbitB", css)
        self.assertIn("@keyframes orbitC", css)
        self.assertIn("transform-box: view-box;", css)
        self.assertIn("transform-origin: 770px 195px;", css)
        self.assertIn(".orbit-a {", css)
        self.assertIn(".orbit-a { animation: none !important; opacity: 1 !important; }", css)

    def test_beacon_pulse_registration(self):
        engine = AnimationEngine(animated=True)
        create_beacon_pulse_animation(engine, cycle_seconds=2.4)
        css = engine.generate_style_block()

        self.assertIn("@keyframes sonarRipple", css)
        self.assertIn("@keyframes nodeGlow", css)
        self.assertIn(".sonar {", css)
        self.assertIn(".beacon-node {", css)
        self.assertIn("cubic-bezier(0.16, 1, 0.3, 1)", css)

    def test_wave_flow_registration(self):
        engine = AnimationEngine(animated=True)
        create_wave_flow_animation(engine)
        css = engine.generate_style_block()

        self.assertIn("@keyframes wavePhaseA", css)
        self.assertIn("stroke-dasharray: 14 8;", css)
        self.assertIn(".wave-a {", css)

    def test_starlight_and_progress_presets(self):
        engine = AnimationEngine(animated=True)
        register_starlight_twinkle(engine)
        register_progress_reveal(engine)
        register_card_glow_pulse(engine)
        register_terminal_cursor_blink(engine)
        css = engine.generate_style_block()

        self.assertIn("@keyframes starTwinkle", css)
        self.assertIn("@keyframes barScaleReveal", css)
        self.assertIn("@keyframes cardBorderBreath", css)
        self.assertIn("@keyframes terminalCursor", css)


if __name__ == "__main__":
    unittest.main()
