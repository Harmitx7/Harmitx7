#!/usr/bin/env python3
"""
CLI script to scrape live GitHub contributions and update data/contributions.json.
Supports --force to bypass the 7-day local disk cache.
"""

import argparse
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.data.contribution_fetcher import ContributionFetcher


def main():
    parser = argparse.ArgumentParser(description="Fetch and parse live GitHub contributions.")
    parser.add_argument("--username", default="Harmitx7", help="Target GitHub username.")
    parser.add_argument("--force", action="store_true", default=True, help="Force live fetch, bypassing cache (default: True).")
    parser.add_argument("--cache", dest="force", action="store_false", help="Allow reading from local disk cache if fresh.")
    parser.add_argument("--out", default=None, help="Custom output JSON path.")
    args = parser.parse_args()

    fetcher = ContributionFetcher(username=args.username)
    out_path = args.out if args.out else os.path.join(REPO_ROOT, "data", "contributions.json")
    try:
        data = fetcher.run(force=args.force, out_path=out_path)
        print(f"✔ Done: {data['total_contributions']} total contributions recorded.")
    except Exception as e:
        print(f"✖ Error fetching contributions: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
