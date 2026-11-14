"""Unit and integration tests for all 9 profile SVG generators."""

import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.generators.contributions import generate_contributions_svg
from src.generators.footer import generate_footer_svg
from src.generators.hero import generate_hero_svg
from src.generators.languages import generate_languages_svg
from src.generators.projects import generate_projects_svg
from src.generators.skill_matrix import generate_skill_matrix_svg
from src.generators.statistics import generate_statistics_svg
from src.generators.status_bar import generate_status_bar_svg
from src.generators.terminal_boot import generate_terminal_boot_svg
from src.utils.formatting import reset_id_registry
from src.utils.validation import validate_svg_content


class TestGenerators(unittest.TestCase):
    def setUp(self):
        reset_id_registry()

    def test_hero_generator_animated(self):
        svg = generate_hero_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"hero.svg (animated) failed validation: {errors}")
        self.assertIn("Harmit Kalal", svg)
        self.assertIn("@keyframes orbitA", svg)
        self.assertIn("@media (prefers-reduced-motion: reduce)", svg)

    def test_hero_generator_static(self):
        svg = generate_hero_svg(animated=False)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"hero.svg (static) failed validation: {errors}")
        self.assertIn("Harmit Kalal", svg)
        self.assertIn("STATIC ACCESSIBILITY MODE", svg)

    def test_projects_generator(self):
        svg = generate_projects_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"projects.svg failed validation: {errors}")
        self.assertIn("tribunal-kit", svg)
        self.assertIn("ARGUS-X", svg)
        self.assertIn("ClashVision", svg)
        self.assertIn("F1 Telemetry", svg)

    def test_statistics_generator(self):
        svg = generate_statistics_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"statistics.svg failed validation: {errors}")
        self.assertIn("PUBLIC REPOS", svg)
        self.assertIn("TOTAL STARS", svg)
        self.assertIn("15", svg)

    def test_contributions_generator(self):
        svg = generate_contributions_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"contributions.svg failed validation: {errors}")
        self.assertIn("SHIPPING_VELOCITY", svg)

    def test_languages_generator(self):
        svg = generate_languages_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"languages.svg failed validation: {errors}")
        self.assertIn("JavaScript", svg)
        self.assertIn("Python", svg)

    def test_footer_generator(self):
        svg = generate_footer_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"footer.svg failed validation: {errors}")
        self.assertIn("AHMEDABAD, IN", svg)
        self.assertIn("INDUS UNIVERSITY", svg)

    def test_skill_matrix_generator(self):
        svg = generate_skill_matrix_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"skill-tree.svg failed validation: {errors}")
        self.assertIn("SKILL_ARCHITECTURE_MATRIX", svg)
        self.assertIn("AI &amp; AGENTIC", svg)
        self.assertIn("LLM Orchestration", svg)

    def test_status_bar_generator(self):
        svg = generate_status_bar_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"status-bar.svg failed validation: {errors}")
        self.assertIn("OPERATIONAL", svg)
        self.assertIn("tribunal-kit", svg)
        self.assertIn("BOI HACKATHON", svg)

    def test_terminal_boot_generator(self):
        svg = generate_terminal_boot_svg(animated=True)
        ok, errors = validate_svg_content(svg)
        self.assertTrue(ok, f"terminal-boot.svg failed validation: {errors}")
        self.assertIn("manifest.json", svg)
        self.assertIn("tribunal-kit", svg)
        self.assertIn("AUDIT PASSED", svg)

    def test_deterministic_rendering(self):
        """Verify calling a generator with identical inputs produces identical outputs."""
        reset_id_registry()
        run1 = generate_footer_svg(animated=False)
        reset_id_registry()
        run2 = generate_footer_svg(animated=False)
        self.assertEqual(run1, run2)

    def test_readme_cards_compiler(self):
        """Test compilation of all 13 reference-inspired animated SVG cards."""
        from scripts.render_readme_cards import compile_all_cards
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            cards = compile_all_cards(out_dir=tmp_dir)
            self.assertIn("hero.svg", cards)
            self.assertIn("heatmap.svg", cards)
            self.assertIn("activity.svg", cards)
            self.assertIn("build.svg", cards)
            self.assertIn("secure.svg", cards)
            self.assertIn("simulate.svg", cards)
            self.assertIn("developer-panel.svg", cards)

            # Validate XML of each compiled card
            for name, path in cards.items():
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                ok, errs = validate_svg_content(content)
                self.assertTrue(ok, f"Card {name} failed validation: {errs}")


    def test_single_render_cards_script(self):
        """Test execution of scripts/render_cards.py (the single master card renderer)."""
        from scripts.render_cards import compile_cards
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            cards = compile_cards(out_dir=tmp_dir)
            self.assertIn("hero.svg", cards)
            self.assertIn("heatmap.svg", cards)
            self.assertIn("activity.svg", cards)
            self.assertIn("build.svg", cards)
            self.assertIn("secure.svg", cards)
            self.assertIn("simulate.svg", cards)
            self.assertIn("repo-tribunal-kit.svg", cards)
            self.assertIn("repo-clashvision.svg", cards)
            self.assertIn("repo-f1-telemetry.svg", cards)
            self.assertIn("footer.svg", cards)

            # Validate each card
            for name, path in cards.items():
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                ok, errs = validate_svg_content(content)
                self.assertTrue(ok, f"Card {name} from render_cards failed validation: {errs}")


if __name__ == "__main__":
    unittest.main()
