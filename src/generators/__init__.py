"""SVG generator modules for all profile components."""

from src.generators.contributions import generate_contributions_svg
from src.generators.footer import generate_footer_svg
from src.generators.hero import generate_hero_svg
from src.generators.languages import generate_languages_svg
from src.generators.projects import generate_projects_svg
from src.generators.skill_matrix import generate_skill_matrix_svg
from src.generators.statistics import generate_statistics_svg
from src.generators.status_bar import generate_status_bar_svg
from src.generators.terminal_boot import generate_terminal_boot_svg

__all__ = [
    "generate_hero_svg",
    "generate_projects_svg",
    "generate_statistics_svg",
    "generate_contributions_svg",
    "generate_languages_svg",
    "generate_footer_svg",
    "generate_skill_matrix_svg",
    "generate_status_bar_svg",
    "generate_terminal_boot_svg",
]
