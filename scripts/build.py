"""
Automated Production Build Script for Harmitx7 Profile Architecture.
Orchestrates: Data Ingestion -> Statistical Computation -> SVG Generation -> Asset Sync -> Validation
"""

import argparse
import os
import re
import shutil
import sys
import time
from typing import Optional

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.utils.validation import validate_svg_file


def update_readme_cache_busters(readme_path: Optional[str] = None, version_tag: Optional[str] = None) -> bool:
    """Update cache-busting query strings on SVG references in README.md to purge Camo edge caching."""
    if not readme_path:
        readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.exists(readme_path):
        return False

    tag = version_tag or str(int(time.time()))
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r'(\./cards/[a-zA-Z0-9_\-]+\.svg)(?:\?v=[a-zA-Z0-9_\-]+)?',
        rf'\1?v={tag}',
        content
    )

    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✔ Updated README.md SVG cache-busters to ?v={tag} for Camo edge invalidation.")
        return True
    return False


def run_build(
    username: str = "Harmitx7",
    force_fetch: bool = True,
    animated: bool = True,
    sync_assets: bool = True,
    update_readme: bool = True,
) -> bool:
    """Execute complete production build cycle."""
    start_time = time.time()
    print("=" * 76)
    print("HARMITX7 PROFILE ARCHITECTURE // PRODUCTION AUTOMATED BUILD PIPELINE")
    print("=" * 76)

    # 1. Data Intelligence Sync (Profile, Repos, and Contributions)
    use_cache = not force_fetch
    try:
        from src.api.github_client import GitHubClient
        from src.data.collector import DataCollector
        from src.data.normalizer import DataNormalizer
        from src.data.statistics import StatisticsCalculator
        from src.data.contribution_fetcher import ContributionFetcher

        print(f"\n[1/4] Syncing live GitHub intelligence for @{username} (use_cache={use_cache})...")
        client = GitHubClient()
        collector = DataCollector(client=client, username=username)
        raw_data = collector.collect_all(use_cache=use_cache)

        normalizer = DataNormalizer(raw_data)
        normalized = normalizer.normalize_all()

        data_dir = os.path.join(REPO_ROOT, "data")
        calc = StatisticsCalculator(normalized)
        calc.export_all(data_dir=data_dir)

        # Sync live 53-week contribution calendar
        fetcher = ContributionFetcher(username=username)
        fetcher.run(force=force_fetch)
        print("✔ Data intelligence & contribution models synchronized.")
    except Exception as e:
        print(f"⚠ Warning: Data synchronization encountered an issue: {e}", file=sys.stderr)
        print("  Preserving last known good datasets in data/ and continuing with build.", file=sys.stderr)

    # 2. Compile Active Editorial Profile Cards
    cards_dir = os.path.join(REPO_ROOT, "cards")
    print(f"\n[2/3] Rendering 10 active editorial SVG cards (animated={animated})...")
    try:
        from scripts.render_cards import compile_cards
        compiled = compile_cards(out_dir=cards_dir)
        print(f"✔ Successfully rendered {len(compiled)} editorial SVG cards into cards/.")
    except Exception as e:
        print(f"✖ Error compiling editorial cards: {e}", file=sys.stderr)
        return False

    # 3. Final Validation Audit
    print("\n[3/3] Validating all production SVG cards...")
    total_audited = 0
    validation_failures = 0

    scan_targets = [
        cards_dir,
    ]

    for target_dir in scan_targets:
        if not os.path.exists(target_dir):
            continue
        for fname in os.listdir(target_dir):
            if fname.endswith(".svg"):
                fpath = os.path.join(target_dir, fname)
                is_valid, errors = validate_svg_file(fpath)
                total_audited += 1
                if not is_valid:
                    validation_failures += 1
                    print(f"  ✖ Validation error in {fpath}:", file=sys.stderr)
                    for err in errors:
                        print(f"    - {err}", file=sys.stderr)

    duration = time.time() - start_time
    print("-" * 76)
    if validation_failures == 0:
        print(f"✔ BUILD PASSED: {total_audited} assets verified in {duration:.2f}s. All contracts nominal.")
        # 4. Cache-Buster Update for GitHub Camo CDN Invalidation
        if update_readme:
            update_readme_cache_busters()
        return True
    else:
        print(f"✖ BUILD FAILED: {validation_failures} assets failed validation.", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and validate all profile assets.")
    parser.add_argument("--user", type=str, default="Harmitx7", help="Target GitHub username")
    parser.add_argument("--force-fetch", action="store_true", default=True, help="Bypass local cache and force fresh API fetch (default: True)")
    parser.add_argument("--use-cache", dest="force_fetch", action="store_false", help="Allow using local disk cache if fresh")
    parser.add_argument("--static", action="store_true", help="Generate static SVG fallbacks")
    parser.add_argument("--sync-assets", action="store_true", default=True, help="Synchronize generated SVGs to assets/")
    parser.add_argument("--no-sync", dest="sync_assets", action="store_false", help="Skip copying to assets/ directory")
    parser.add_argument("--no-readme-update", dest="update_readme", action="store_false", default=True, help="Skip updating Camo cache-busters in README.md")

    args = parser.parse_args()
    success = run_build(
        username=args.user,
        force_fetch=args.force_fetch,
        animated=not args.static,
        sync_assets=args.sync_assets,
        update_readme=args.update_readme,
    )
    if not success:
        sys.exit(1)
