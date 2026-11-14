"""GitHub REST and GraphQL API client with rate limiting, retries, and file caching."""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


class GitHubClient:
    """Production GitHub API client designed for automation pipelines."""

    def __init__(
        self,
        token: Optional[str] = None,
        cache_dir: Optional[str] = None,
        max_retries: int = 3,
        timeout_seconds: int = 15,
    ):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.max_retries = max_retries
        self.timeout = timeout_seconds

        if cache_dir:
            self.cache_dir = os.path.abspath(cache_dir)
        else:
            self.cache_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")
            )
        os.makedirs(self.cache_dir, exist_ok=True)

        self.last_rate_limit_remaining: Optional[int] = None
        self.last_rate_limit_reset: Optional[int] = None

    def _get_cache_path(self, cache_key: str) -> str:
        """Derive a safe cache file path from key."""
        hashed = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()[:16]
        clean_key = "".join([c if c.isalnum() or c in "-_" else "_" for c in cache_key])[:32]
        return os.path.join(self.cache_dir, f"{clean_key}_{hashed}.json")

    def _read_cache(self, cache_key: str, max_age_seconds: int = 3600) -> Optional[Any]:
        """Read cached JSON payload if fresh."""
        cache_file = self._get_cache_path(cache_key)
        if not os.path.exists(cache_file):
            return None
        try:
            mtime = os.path.getmtime(cache_file)
            if time.time() - mtime > max_age_seconds:
                return None
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _write_cache(self, cache_key: str, data: Any) -> None:
        """Write JSON payload to cache."""
        cache_file = self._get_cache_path(cache_key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to write cache for {cache_key}: {e}", file=sys.stderr)

    def _build_request(self, url: str, method: str = "GET", payload: Optional[Dict] = None) -> urllib.request.Request:
        """Build HTTP request with required headers (never leaks token in logs)."""
        headers = {
            "User-Agent": "Harmitx7-Live-Intelligence-Engine/1.0",
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        data_bytes = None
        if payload is not None:
            data_bytes = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        return urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

    def _execute_http(self, req: urllib.request.Request, cache_key: str) -> Tuple[Optional[Any], bool]:
        """Execute HTTP request with bounded retry and rate limit tracking."""
        attempt = 0
        backoff = 1.0

        while attempt < self.max_retries:
            attempt += 1
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    # Update rate limit tracking headers
                    rem = resp.headers.get("x-ratelimit-remaining")
                    rst = resp.headers.get("x-ratelimit-reset")
                    if rem is not None:
                        try:
                            self.last_rate_limit_remaining = int(rem)
                        except ValueError:
                            pass
                    if rst is not None:
                        try:
                            self.last_rate_limit_reset = int(rst)
                        except ValueError:
                            pass

                    body = resp.read().decode("utf-8")
                    data = json.loads(body)
                    self._write_cache(cache_key, data)
                    return data, True

            except urllib.error.HTTPError as he:
                status = he.code
                # Check rate limit on 403
                if status == 403:
                    print("Notice: GitHub API returned 403 (Rate Limit or Forbidden). Checking cache.", file=sys.stderr)
                    cached = self._read_cache(cache_key, max_age_seconds=86400 * 7)  # allow up to 7-day stale on 403
                    if cached is not None:
                        return cached, False
                    return None, False

                # Retry on 5xx or 429
                if status in (500, 502, 503, 504, 429) and attempt < self.max_retries:
                    time.sleep(backoff)
                    backoff *= 2.0
                    continue

                print(f"HTTPError {status} on {req.full_url}", file=sys.stderr)
                # Try stale cache on terminal failure
                cached = self._read_cache(cache_key, max_age_seconds=86400 * 7)
                return cached, False

            except (urllib.error.URLError, TimeoutError) as ue:
                if attempt < self.max_retries:
                    time.sleep(backoff)
                    backoff *= 2.0
                    continue
                print(f"Network error on {req.full_url}: {ue}. Attempting cache fallback.", file=sys.stderr)
                cached = self._read_cache(cache_key, max_age_seconds=86400 * 7)
                return cached, False

        return None, False

    def get_user(self, username: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """Fetch public profile metadata for user."""
        cache_key = f"user_{username}"
        if use_cache:
            cached = self._read_cache(cache_key)
            if cached is not None:
                return cached

        url = f"https://api.github.com/users/{urllib.parse.quote(username)}"
        req = self._build_request(url)
        data, _ = self._execute_http(req, cache_key)
        return data

    def get_repositories(self, username: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Fetch all public repositories with pagination handling."""
        cache_key = f"repos_{username}"
        if use_cache:
            cached = self._read_cache(cache_key)
            if cached is not None:
                return cached

        all_repos: List[Dict[str, Any]] = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/users/{urllib.parse.quote(username)}/repos?page={page}&per_page={per_page}&sort=pushed"
            page_key = f"repos_{username}_p{page}"
            req = self._build_request(url)
            page_data, ok = self._execute_http(req, page_key)

            if not ok or not page_data or not isinstance(page_data, list):
                if not all_repos:
                    # Attempt older aggregated cache
                    stale = self._read_cache(cache_key, max_age_seconds=86400 * 7)
                    if stale:
                        return stale
                break

            all_repos.extend(page_data)
            if len(page_data) < per_page:
                break
            page += 1

        if all_repos:
            self._write_cache(cache_key, all_repos)
        return all_repos

    def get_repo_languages(self, owner: str, repo: str, use_cache: bool = True) -> Dict[str, int]:
        """Fetch language byte breakdown for a specific repository."""
        cache_key = f"langs_{owner}_{repo}"
        if use_cache:
            cached = self._read_cache(cache_key)
            if cached is not None:
                return cached

        url = f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/languages"
        req = self._build_request(url)
        data, ok = self._execute_http(req, cache_key)
        if ok and isinstance(data, dict):
            return data
        return {}

    def get_user_events(self, username: str, max_pages: int = 2, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Fetch recent public events with bounded pagination."""
        cache_key = f"events_{username}"
        if use_cache:
            cached = self._read_cache(cache_key, max_age_seconds=1800)  # 30 min freshness
            if cached is not None:
                return cached

        all_events: List[Dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            url = f"https://api.github.com/users/{urllib.parse.quote(username)}/events/public?page={page}&per_page=100"
            page_key = f"events_{username}_p{page}"
            req = self._build_request(url)
            data, ok = self._execute_http(req, page_key)
            if not ok or not data or not isinstance(data, list):
                break
            all_events.extend(data)
            if len(data) < 100:
                break

        if all_events:
            self._write_cache(cache_key, all_events)
        return all_events

    def execute_graphql(self, query: str, variables: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Execute a GraphQL query (requires token; returns None if unauthenticated)."""
        if not self.token:
            return None

        cache_key = f"graphql_{hashlib.sha256(query.encode('utf-8')).hexdigest()[:16]}"
        cached = self._read_cache(cache_key, max_age_seconds=3600)
        if cached is not None:
            return cached

        url = "https://api.github.com/graphql"
        req = self._build_request(url, method="POST", payload={"query": query, "variables": variables or {}})
        data, ok = self._execute_http(req, cache_key)
        if ok and isinstance(data, dict):
            return data
        return None
