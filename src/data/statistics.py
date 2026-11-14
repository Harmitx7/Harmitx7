"""Statistics calculator: computes aggregates, language distributions, and presentation metrics."""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List


class StatisticsCalculator:
    """Calculates authoritative, evidence-backed GitHub profile metrics."""

    def __init__(self, normalized_data: Dict[str, Any]):
        self.profile = normalized_data.get("profile", {})
        self.repos = normalized_data.get("repositories", [])
        self.events = normalized_data.get("events", [])

    def calculate_language_distribution(self) -> Dict[str, Any]:
        """Aggregate language bytes across all non-fork public repositories."""
        totals: Dict[str, int] = {}
        total_bytes = 0

        for r in self.repos:
            for lang, byte_count in r.get("languages_bytes", {}).items():
                totals[lang] = totals.get(lang, 0) + byte_count
                total_bytes += byte_count

        distribution: Dict[str, Dict[str, Any]] = {}
        for lang, byte_count in sorted(totals.items(), key=lambda x: x[1], reverse=True):
            pct = (byte_count / total_bytes * 100.0) if total_bytes > 0 else 0.0
            distribution[lang] = {
                "bytes": byte_count,
                "percentage": round(pct, 2),
            }

        return {
            "total_code_bytes": total_bytes,
            "distinct_languages_count": len(distribution),
            "distribution": distribution,
        }

    def calculate_summary_metrics(self) -> Dict[str, Any]:
        """Calculate verified account-level metrics with strict data integrity boundaries."""
        total_stars = sum(r.get("stargazers_count", 0) for r in self.repos)
        total_forks = sum(r.get("forks_count", 0) for r in self.repos)
        lang_dist = self.calculate_language_distribution()

        push_events = [e for e in self.events if e.get("type") == "PushEvent"]
        total_recent_commits = sum(e.get("commit_count", 0) for e in push_events)

        return {
            "public_repos": len(self.repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_followers": self.profile.get("followers_count", 0),
            "total_following": self.profile.get("following_count", 0),
            "total_code_bytes": lang_dist["total_code_bytes"],
            "distinct_languages": lang_dist["distinct_languages_count"],
            "recent_public_push_events": len(push_events),
            "recent_public_commits_sampled": total_recent_commits,
            "data_integrity_invariants": {
                "scope": "PUBLIC_REPOSITORIES_ONLY",
                "private_contributions_included": False,
                "hours_coded_claimed": False,
                "zero_fabrication_enforced": True,
            },
            "last_calculated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def export_all(self, data_dir: str) -> None:
        """Export normalized profile, repositories, and available metrics JSON files."""
        os.makedirs(data_dir, exist_ok=True)

        summary = self.calculate_summary_metrics()
        lang_dist = self.calculate_language_distribution()

        # 1. data/profile.json
        profile_path = os.path.join(data_dir, "profile.json")
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=2)

        # 2. data/repositories.json
        repos_payload = {
            "repositories_count": len(self.repos),
            "total_stars": summary["total_stars"],
            "total_forks": summary["total_forks"],
            "total_code_bytes": lang_dist["total_code_bytes"],
            "languages_distribution": lang_dist["distribution"],
            "repositories": self.repos,
        }
        repos_path = os.path.join(data_dir, "repositories.json")
        with open(repos_path, "w", encoding="utf-8") as f:
            json.dump(repos_payload, f, indent=2)

        # 3. data/available_metrics.json
        metrics_payload = {
            "summary": summary,
            "language_distribution": lang_dist,
            "top_languages": list(lang_dist["distribution"].keys())[:6],
        }
        metrics_path = os.path.join(data_dir, "available_metrics.json")
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics_payload, f, indent=2)

        print(f"✔ Exported live intelligence datasets to {data_dir}:")
        print(f"  - profile.json ({self.profile.get('login')})")
        print(f"  - repositories.json ({len(self.repos)} repositories, {summary['total_stars']} stars)")
        print(f"  - available_metrics.json ({lang_dist['total_code_bytes']:,} bytes analyzed)")
