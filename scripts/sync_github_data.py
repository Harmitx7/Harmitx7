"""End-to-end synchronization script: GitHub API -> Normalized Data -> SVG Generation."""

import argparse
import os
import sys

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.api.github_client import GitHubClient
from src.data.collector import DataCollector
from src.data.normalizer import DataNormalizer
from src.data.statistics import StatisticsCalculator
from src.main import build_all


def sync_pipeline(username: str = "Harmitx7", use_cache: bool = True, rebuild_svgs: bool = True) -> bool:
    """Run the complete live intelligence pipeline."""
    print("=" * 70)
    print(f"HARMITX7 LIVE INTELLIGENCE PIPELINE: @{username}")
    print("=" * 70)

    # 1. Collection
    client = GitHubClient()
    collector = DataCollector(client=client, username=username)
    raw_data = collector.collect_all(use_cache=use_cache)

    # 2. Normalization
    normalizer = DataNormalizer(raw_data)
    normalized = normalizer.normalize_all()
    print(f"✔ Normalized {len(normalized['repositories'])} repositories and {len(normalized['events'])} events.")

    # 3. Statistical Computation & Export
    data_dir = os.path.join(REPO_ROOT, "data")
    calculator = StatisticsCalculator(normalized)
    calculator.export_all(data_dir=data_dir)

    # 4. Rebuild SVGs
    if rebuild_svgs:
        print("\nRebuilding all SVG components with updated data...")
        generated_dir = os.path.join(REPO_ROOT, "generated")
        ok = build_all(generated_dir, animated=True)
        if ok:
            import shutil
            assets_gen = os.path.join(REPO_ROOT, "assets", "generated")
            os.makedirs(assets_gen, exist_ok=True)
            for fname in os.listdir(generated_dir):
                if fname.endswith(".svg"):
                    shutil.copy2(os.path.join(generated_dir, fname), os.path.join(assets_gen, fname))
            print("✔ Rebuilt and synced all SVGs to assets/generated/")
            return True
        else:
            print("✖ Failed to rebuild SVGs.", file=sys.stderr)
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync live GitHub intelligence and regenerate profile SVGs.")
    parser.add_argument("--user", type=str, default="Harmitx7", help="GitHub username")
    parser.add_argument("--no-cache", action="store_true", help="Bypass local cache and force API fetch")
    parser.add_argument("--no-rebuild", action="store_true", help="Skip SVG rebuilding")

    args = parser.parse_args()
    success = sync_pipeline(username=args.user, use_cache=not args.no_cache, rebuild_svgs=not args.no_rebuild)
    if not success:
        sys.exit(1)
