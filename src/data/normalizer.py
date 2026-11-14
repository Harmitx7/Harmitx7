"""Data normalizer: converts raw API responses into structured, validated domain models."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def parse_utc_timestamp(ts_str: Optional[str]) -> Optional[str]:
    """Parse ISO timestamp and normalize to UTC string (YYYY-MM-DDTHH:MM:SSZ)."""
    if not ts_str:
        return None
    try:
        clean_ts = ts_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_ts)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ts_str


class DataNormalizer:
    """Normalizes raw GitHub intelligence into clean, schema-consistent datasets."""

    def __init__(self, raw_data: Dict[str, Any]):
        self.raw = raw_data

    def normalize_profile(self) -> Dict[str, Any]:
        """Normalize public profile record (distinguishing null vs. 0)."""
        u = self.raw.get("user", {})
        return {
            "login": u.get("login", "Harmitx7"),
            "id": u.get("id"),
            "name": u.get("name"),
            "bio": u.get("bio"),
            "company": u.get("company"),
            "blog": u.get("blog") or "https://harmit.vercel.app",
            "location": u.get("location"),
            "email": u.get("email"),
            "hireable": u.get("hireable"),
            "twitter_username": u.get("twitter_username"),
            "public_repos_count": int(u.get("public_repos", 0)),
            "public_gists_count": int(u.get("public_gists", 0)),
            "followers_count": int(u.get("followers", 0)),
            "following_count": int(u.get("following", 0)),
            "created_at": parse_utc_timestamp(u.get("created_at")),
            "updated_at": parse_utc_timestamp(u.get("updated_at")),
            "profile_url": u.get("html_url", "https://github.com/Harmitx7"),
            "avatar_url": u.get("avatar_url"),
            "external_context": {
                "inferred_location": "Ahmedabad, Gujarat, India (23.02°N, 72.57°E)",
                "academic_institution": "Indus University (Computer Engineering)",
                "portfolio_url": "https://harmit.vercel.app",
                "npm_flagship": "https://www.npmjs.com/package/tribunal-kit",
            },
        }

    def normalize_repositories(self) -> List[Dict[str, Any]]:
        """Normalize repository records, eliminate duplicates, and attach verified byte counts."""
        raw_repos = self.raw.get("repositories", [])
        langs_by_repo = self.raw.get("languages_by_repo", {})

        seen_names = set()
        cleaned: List[Dict[str, Any]] = []

        for r in raw_repos:
            rname = r.get("name")
            if not rname or rname in seen_names:
                continue
            seen_names.add(rname)

            rlangs = langs_by_repo.get(rname, {})
            r_bytes = sum(rlangs.values())

            cleaned.append({
                "name": rname,
                "full_name": r.get("full_name", f"Harmitx7/{rname}"),
                "html_url": r.get("html_url", f"https://github.com/Harmitx7/{rname}"),
                "description": r.get("description"),
                "is_fork": bool(r.get("fork", False)),
                "primary_language": r.get("language"),
                "languages_bytes": rlangs,
                "total_code_bytes": r_bytes,
                "stargazers_count": int(r.get("stargazers_count", 0)),
                "forks_count": int(r.get("forks_count", 0)),
                "watchers_count": int(r.get("watchers_count", 0)),
                "open_issues_count": int(r.get("open_issues_count", 0)),
                "topics": list(r.get("topics", [])),
                "created_at": parse_utc_timestamp(r.get("created_at")),
                "updated_at": parse_utc_timestamp(r.get("updated_at")),
                "pushed_at": parse_utc_timestamp(r.get("pushed_at")),
                "archived": bool(r.get("archived", False)),
                "disabled": bool(r.get("disabled", False)),
                "license_name": r.get("license", {}).get("name") if r.get("license") else None,
            })

        # Sort descending by stars, then pushed_at
        cleaned.sort(key=lambda x: (x["stargazers_count"], x["pushed_at"] or ""), reverse=True)
        return cleaned

    def normalize_events(self) -> List[Dict[str, Any]]:
        """Normalize public activity events."""
        raw_events = self.raw.get("events", [])
        seen_ids = set()
        cleaned_events: List[Dict[str, Any]] = []

        for e in raw_events:
            eid = e.get("id")
            if not eid or eid in seen_ids:
                continue
            seen_ids.add(eid)

            etype = e.get("type", "UnknownEvent")
            repo_info = e.get("repo", {})
            payload = e.get("payload", {})

            commit_count = 0
            if etype == "PushEvent":
                commit_count = len(payload.get("commits", [])) or payload.get("size", 1)

            cleaned_events.append({
                "id": str(eid),
                "type": etype,
                "repo_name": repo_info.get("name", ""),
                "created_at": parse_utc_timestamp(e.get("created_at")),
                "commit_count": commit_count,
            })

        return cleaned_events

    def normalize_all(self) -> Dict[str, Any]:
        """Produce the complete normalized dataset."""
        profile = self.normalize_profile()
        repos = self.normalize_repositories()
        events = self.normalize_events()

        return {
            "profile": profile,
            "repositories": repos,
            "events": events,
            "metadata": {
                "normalized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "total_repos_count": len(repos),
                "total_events_count": len(events),
            },
        }
