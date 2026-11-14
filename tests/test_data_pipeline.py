"""Unit tests for the data normalization and statistical computation pipeline."""

import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.data.normalizer import DataNormalizer, parse_utc_timestamp
from src.data.statistics import StatisticsCalculator


class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_raw_data = {
            "user": {
                "login": "Harmitx7",
                "name": "Harmit Kalal",
                "bio": None,  # Explicitly null
                "company": None,
                "public_repos": 15,
                "public_gists": 0,  # Explicitly zero
                "followers": 7,
                "following": 4,
                "created_at": "2022-09-14T12:58:44Z",
                "updated_at": "2026-11-12T12:22:08Z",
            },
            "repositories": [
                {
                    "name": "tribunal-kit",
                    "full_name": "Harmitx7/tribunal-kit",
                    "description": "Multi-Agent AI Framework",
                    "fork": False,
                    "language": "JavaScript",
                    "stargazers_count": 6,
                    "forks_count": 1,
                    "topics": ["ai-agents", "mcp-server"],
                    "pushed_at": "2026-11-05T10:40:02Z",
                },
                {
                    "name": "ClashVision-v3.0",
                    "full_name": "Harmitx7/ClashVision-v3.0",
                    "description": "AI Battle Predictor",
                    "fork": False,
                    "language": "Python",
                    "stargazers_count": 2,
                    "forks_count": 0,
                    "topics": ["ml", "rl"],
                    "pushed_at": "2025-10-24T11:56:17Z",
                },
                # Duplicate record to test deduplication
                {
                    "name": "tribunal-kit",
                    "full_name": "Harmitx7/tribunal-kit",
                    "stargazers_count": 6,
                },
            ],
            "languages_by_repo": {
                "tribunal-kit": {"JavaScript": 6000000, "Rust": 300000},
                "ClashVision-v3.0": {"Python": 2000000},
            },
            "events": [
                {
                    "id": "ev_1",
                    "type": "PushEvent",
                    "repo": {"name": "Harmitx7/tribunal-kit"},
                    "payload": {"commits": [{"sha": "a1"}, {"sha": "a2"}]},
                    "created_at": "2026-11-05T10:40:00Z",
                },
                {
                    "id": "ev_2",
                    "type": "WatchEvent",
                    "repo": {"name": "Harmitx7/tribunal-kit"},
                    "payload": {},
                    "created_at": "2026-11-04T08:00:00Z",
                },
            ],
        }

    def test_timestamp_parser(self):
        ts = parse_utc_timestamp("2026-11-14T07:38:00Z")
        self.assertEqual(ts, "2026-11-14T07:38:00Z")
        self.assertIsNone(parse_utc_timestamp(None))

    def test_normalizer_profile_null_vs_zero(self):
        norm = DataNormalizer(self.mock_raw_data)
        profile = norm.normalize_profile()
        self.assertEqual(profile["login"], "Harmitx7")
        self.assertIsNone(profile["bio"])
        self.assertEqual(profile["public_gists_count"], 0)
        self.assertEqual(profile["followers_count"], 7)

    def test_normalizer_deduplication(self):
        norm = DataNormalizer(self.mock_raw_data)
        repos = norm.normalize_repositories()
        self.assertEqual(len(repos), 2, "Expected duplicate tribunal-kit to be pruned.")
        self.assertEqual(repos[0]["name"], "tribunal-kit")
        self.assertEqual(repos[0]["total_code_bytes"], 6300000)

    def test_statistics_calculator(self):
        norm = DataNormalizer(self.mock_raw_data)
        normalized_data = norm.normalize_all()
        calc = StatisticsCalculator(normalized_data)

        summary = calc.calculate_summary_metrics()
        self.assertEqual(summary["public_repos"], 2)
        self.assertEqual(summary["total_stars"], 8)
        self.assertEqual(summary["total_forks"], 1)
        self.assertEqual(summary["recent_public_push_events"], 1)
        self.assertEqual(summary["recent_public_commits_sampled"], 2)

        lang_dist = calc.calculate_language_distribution()
        dist = lang_dist["distribution"]
        self.assertIn("JavaScript", dist)
        self.assertIn("Python", dist)
        self.assertIn("Rust", dist)
        self.assertEqual(lang_dist["total_code_bytes"], 8300000)

    def test_contribution_fetcher_parser(self):
        from src.data.contribution_fetcher import ContributionFetcher
        mock_html = """
        <td data-date="2026-01-01" data-level="1" id="c-1" class="ContributionCalendar-day"></td>
        <td data-date="2026-01-02" data-level="2" id="c-2" class="ContributionCalendar-day"></td>
        <td data-date="2026-01-03" data-level="0" id="c-3" class="ContributionCalendar-day"></td>
        <tool-tip for="c-1">3 contributions on Jan 1</tool-tip>
        <tool-tip for="c-2">5 contributions on Jan 2</tool-tip>
        <tool-tip for="c-3">No contributions on Jan 3</tool-tip>
        """
        fetcher = ContributionFetcher(username="TestUser")
        data = fetcher.parse_contributions(mock_html)
        self.assertEqual(data["total_contributions"], 8)
        self.assertEqual(data["active_days"], 2)
        self.assertEqual(data["total_calendar_days"], 3)
        self.assertEqual(data["longest_streak"]["days"], 2)
        self.assertEqual(data["busiest_day"]["count"], 5)


if __name__ == "__main__":
    unittest.main()
