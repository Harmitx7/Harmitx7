"""Unit tests for the SVG generation engine primitives and utilities."""

import unittest
import xml.etree.ElementTree as ET
import os
import sys

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.svg.primitives import Rect, Circle, Line, Path, Group, SvgRoot
from src.svg.typography import Text, Tspan
from src.svg.gradients import LinearGradient, RadialGradient
from src.svg.filters import GlowFilter
from src.svg.animation import AnimationEngine
from src.utils.colors import hex_to_rgb, rgba_str
from src.utils.formatting import escape_xml, truncate_text, format_bytes, generate_unique_id, reset_id_registry
from src.utils.validation import validate_svg_content


class TestUtils(unittest.TestCase):
    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb("#00F0FF"), (0, 240, 255))
        self.assertEqual(hex_to_rgb("#FFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))

    def test_rgba_str(self):
        self.assertEqual(rgba_str("#00F0FF", 0.5), "rgba(0, 240, 255, 0.50)")

    def test_escape_xml(self):
        self.assertEqual(escape_xml("A & B < C > 'D' \"E\""), "A &amp; B &lt; C &gt; &#x27;D&#x27; &quot;E&quot;")
        self.assertEqual(escape_xml(None), "")

    def test_truncate_text(self):
        self.assertEqual(truncate_text("Hello World", 5), "He...")
        self.assertEqual(truncate_text("Short", 10), "Short")

    def test_format_bytes(self):
        self.assertEqual(format_bytes(500), "500 B")
        self.assertEqual(format_bytes(2048), "2.0 KB")
        self.assertEqual(format_bytes(1048576 * 5), "5.00 MB")

    def test_unique_id(self):
        reset_id_registry()
        id1 = generate_unique_id("test", "card")
        id2 = generate_unique_id("test", "card")
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("test_card"))
        self.assertTrue(id2.startswith("test_card_1"))


class TestSvgPrimitives(unittest.TestCase):
    def test_rect_rendering(self):
        r = Rect(x=10, y=20, width=100, height=50, rx=5, fill="#000", stroke="#FFF", stroke_width=1)
        xml = r.render()
        self.assertIn('x="10"', xml)
        self.assertIn('y="20"', xml)
        self.assertIn('width="100"', xml)
        self.assertIn('rx="5"', xml)

    def test_circle_rendering(self):
        c = Circle(cx=50, cy=50, r=25, fill="#00F0FF")
        xml = c.render()
        self.assertIn('cx="50"', xml)
        self.assertIn('cy="50"', xml)
        self.assertIn('r="25"', xml)

    def test_text_rendering(self):
        t = Text(text="Test Label", x=10, y=20, font_size=14, font_weight="700", fill="#FFF")
        xml = t.render()
        self.assertIn("Test Label", xml)
        self.assertIn('font-size="14"', xml)
        self.assertIn('font-weight="700"', xml)

    def test_svg_root_well_formedness(self):
        root = SvgRoot(view_box="0 0 100 100", width="100%", title="Unit Test SVG")
        root.add(Rect(x=0, y=0, width=100, height=100, fill="#05070B"))
        root.add(Text(text="Hello", x=10, y=20))
        xml = root.render()

        # Parse with standard ElementTree
        tree = ET.fromstring(xml)
        self.assertIn("svg", tree.tag.lower())
        self.assertEqual(tree.attrib["viewBox"], "0 0 100 100")


class TestValidation(unittest.TestCase):
    def test_valid_svg_passes(self):
        valid = '<svg width="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100"/></svg>'
        ok, errors = validate_svg_content(valid)
        self.assertTrue(ok, f"Expected valid, got errors: {errors}")

    def test_script_tag_fails(self):
        malicious = '<svg width="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        ok, errors = validate_svg_content(malicious)
        self.assertFalse(ok)
        self.assertTrue(any("script" in e.lower() for e in errors))

    def test_onload_event_fails(self):
        malicious = '<svg width="100%" viewBox="0 0 100 100" onload="alert(1)" xmlns="http://www.w3.org/2000/svg"><rect/></svg>'
        ok, errors = validate_svg_content(malicious)
        self.assertFalse(ok)
        self.assertTrue(any("onload" in e.lower() for e in errors))

    def test_missing_viewbox_fails(self):
        no_vb = '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect/></svg>'
        ok, errors = validate_svg_content(no_vb)
        self.assertFalse(ok)
        self.assertTrue(any("viewbox" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
