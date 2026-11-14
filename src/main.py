"""Main build orchestrator and CLI for the Custom SVG Component Engine."""

import argparse
import os
import sys

# Ensure repository root is on sys.path
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

GENERATORS = {
    "hero": ("hero.svg", generate_hero_svg),
    "projects": ("projects.svg", generate_projects_svg),
    "statistics": ("statistics.svg", generate_statistics_svg),
    "contributions": ("contributions.svg", generate_contributions_svg),
    "languages": ("languages.svg", generate_languages_svg),
    "footer": ("footer.svg", generate_footer_svg),
    "skill-tree": ("skill-tree.svg", generate_skill_matrix_svg),
    "status-bar": ("status-bar.svg", generate_status_bar_svg),
    "terminal-boot": ("terminal-boot.svg", generate_terminal_boot_svg),
}


def build_component(name: str, out_dir: str, animated: bool = True) -> bool:
    """Build, validate, and write a single SVG component."""
    if name not in GENERATORS:
        print(f"Error: Unknown generator '{name}'. Available: {list(GENERATORS.keys())}", file=sys.stderr)
        return False

    filename, gen_func = GENERATORS[name]
    reset_id_registry()

    svg_content = gen_func(animated=animated)
    is_valid, errors = validate_svg_content(svg_content)

    if not is_valid:
        print(f"✖ Validation failed for {filename}:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    size_kb = len(svg_content.encode("utf-8")) / 1024
    mode_str = "animated" if animated else "static"
    print(f"✔ Generated {filename:<18} ({size_kb:>5.1f} KB, {mode_str}) -> {out_path}")
    return True


def build_all(out_dir: str, animated: bool = True) -> bool:
    """Build and validate all components."""
    print(f"Building all {len(GENERATORS)} SVG components (animated={animated})...")
    success = True
    for name in GENERATORS.keys():
        if not build_component(name, out_dir, animated=animated):
            success = False
    return success


def main():
    parser = argparse.ArgumentParser(description="Harmitx7 SVG Component Engine")
    parser.add_argument("--all", action="store_true", help="Build all SVG components")
    parser.add_argument("--section", type=str, choices=list(GENERATORS.keys()), help="Build a specific section")
    parser.add_argument("--out-dir", type=str, default=os.path.join(REPO_ROOT, "generated"), help="Output directory")
    parser.add_argument("--static", action="store_true", help="Generate static fallback versions without animations")
    parser.add_argument("--sync-assets", action="store_true", help="Also sync generated SVGs to assets/ and assets/generated/")

    args = parser.parse_args()
    animated = not args.static

    if not args.all and not args.section:
        parser.print_help()
        sys.exit(1)

    out_dir = os.path.abspath(args.out_dir)

    if args.all:
        ok = build_all(out_dir, animated=animated)
    elif args.section:
        ok = build_component(args.section, out_dir, animated=animated)
    else:
        ok = True

    if ok and args.sync_assets:
        import shutil
        target_assets = os.path.join(REPO_ROOT, "assets")
        target_gen = os.path.join(REPO_ROOT, "assets", "generated")
        os.makedirs(target_assets, exist_ok=True)
        os.makedirs(target_gen, exist_ok=True)

        for fname in os.listdir(out_dir):
            if fname.endswith(".svg"):
                src = os.path.join(out_dir, fname)
                # Primary root assets
                if fname in ["hero.svg", "skill-tree.svg", "status-bar.svg", "terminal-boot.svg", "footer.svg"]:
                    dst = os.path.join(target_assets, fname)
                    shutil.copy2(src, dst)
                    print(f"  Synced primary asset -> {dst}")
                # Generated folder
                dst_gen = os.path.join(target_gen, fname)
                shutil.copy2(src, dst_gen)
                print(f"  Synced generated asset -> {dst_gen}")

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
