"""Data collector orchestrator: pulls live GitHub intelligence into raw cache."""

import json
import os
import sys
from typing import Any, Dict, List, Optional
from src.api.github_client import GitHubClient


class DataCollector:
    """Orchestrates multi-endpoint GitHub data collection."""

    def __init__(self, client: Optional[GitHubClient] = None, username: str = "Harmitx7"):
        self.client = client or GitHubClient()
        self.username = username

    def collect_all(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Collect complete GitHub data:
        1. User profile
        2. Repositories
        3. Languages per repository
        4. Public events
        """
        print(f"Collecting GitHub data for @{self.username} (use_cache={use_cache})...")

        # 1. User
        user_data = self.client.get_user(self.username, use_cache=use_cache)
        if not user_data:
            print("Warning: Could not fetch user data. Falling back to default record.", file=sys.stderr)
            user_data = {"login": self.username}

        # 2. Repositories
        repos_data = self.client.get_repositories(self.username, use_cache=use_cache)
        print(f"  Found {len(repos_data)} repositories.")

        # 3. Languages per repository
        languages_by_repo: Dict[str, Dict[str, int]] = {}
        for r in repos_data:
            rname = r.get("name")
            if not rname or r.get("fork", False):
                continue
            langs = self.client.get_repo_languages(self.username, rname, use_cache=use_cache)
            if langs:
                languages_by_repo[rname] = langs

        print(f"  Collected languages across {len(languages_by_repo)} owned repositories.")

        # 4. Events
        events_data = self.client.get_user_events(self.username, max_pages=2, use_cache=use_cache)
        print(f"  Collected {len(events_data)} recent public events.")

        raw_payload = {
            "username": self.username,
            "user": user_data,
            "repositories": repos_data,
            "languages_by_repo": languages_by_repo,
            "events": events_data,
            "rate_limit_remaining": self.client.last_rate_limit_remaining,
            "rate_limit_reset": self.client.last_rate_limit_reset,
        }

        # Save raw snapshot
        cache_file = os.path.join(self.client.cache_dir, "raw_intelligence.json")
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(raw_payload, f, indent=2)
            print(f"✔ Saved raw intelligence snapshot to {cache_file}")
        except Exception as e:
            print(f"Warning: Failed to save raw snapshot: {e}", file=sys.stderr)

        return raw_payload
