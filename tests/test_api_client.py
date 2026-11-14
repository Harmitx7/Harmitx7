"""Unit tests for GitHubClient with mocked HTTP requests and cache validation."""

import io
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.api.github_client import GitHubClient


class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.temp_cache = os.path.join(REPO_ROOT, "data", "test_cache")
        os.makedirs(self.temp_cache, exist_ok=True)
        self.client = GitHubClient(token="test_mock_token", cache_dir=self.temp_cache, max_retries=2)

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_cache):
            shutil.rmtree(self.temp_cache, ignore_errors=True)

    @patch("urllib.request.urlopen")
    def test_get_user_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "login": "Harmitx7",
            "name": "Harmit Kalal",
            "public_repos": 15,
            "followers": 7
        }).encode("utf-8")
        mock_response.headers = {"x-ratelimit-remaining": "50", "x-ratelimit-reset": "1794645302"}
        mock_urlopen.return_value.__enter__.return_value = mock_response

        user = self.client.get_user("Harmitx7", use_cache=False)
        self.assertIsNotNone(user)
        self.assertEqual(user["login"], "Harmitx7")
        self.assertEqual(self.client.last_rate_limit_remaining, 50)

    @patch("urllib.request.urlopen")
    def test_token_header_attached(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"login": "Harmitx7"}).encode("utf-8")
        mock_response.headers = {}
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.client.get_user("Harmitx7", use_cache=False)
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        self.assertEqual(req.headers.get("Authorization"), "Bearer test_mock_token")

    @patch("urllib.request.urlopen")
    def test_get_repositories_pagination(self, mock_urlopen):
        # Return page 1 with 100 items, page 2 with 5 items
        page1 = [{"name": f"repo_{i}", "stargazers_count": 0} for i in range(100)]
        page2 = [{"name": "repo_101", "stargazers_count": 5}]

        resp1 = MagicMock()
        resp1.read.return_value = json.dumps(page1).encode("utf-8")
        resp1.headers = {}

        resp2 = MagicMock()
        resp2.read.return_value = json.dumps(page2).encode("utf-8")
        resp2.headers = {}

        mock_urlopen.return_value.__enter__.side_effect = [resp1, resp2]

        repos = self.client.get_repositories("Harmitx7", use_cache=False)
        self.assertEqual(len(repos), 101)
        self.assertEqual(repos[-1]["name"], "repo_101")


if __name__ == "__main__":
    unittest.main()
