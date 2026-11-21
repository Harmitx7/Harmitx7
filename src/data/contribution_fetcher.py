"""
Live Contribution Fetcher & Calendar Parser.
Scrapes real daily contribution counts from GitHub's public contribution fragment:
https://github.com/users/{USERNAME}/contributions
Calculates 53-week calendar, streaks, monthly distributions, and weekday activity.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE_DIR = os.path.join(REPO_ROOT, "data", "cache")
OUT_PATH = os.path.join(REPO_ROOT, "data", "contributions.json")


class ContributionFetcher:
    def __init__(self, username: str = "Harmitx7", cache_dir: str = CACHE_DIR):
        self.username = username
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, f"contrib_raw_{username}.html")

    def fetch_raw_html(self, force: bool = False) -> str:
        """Fetch raw HTML fragment with caching and user-agent headers."""
        is_ci = bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))
        if not force and not is_ci and os.path.exists(self.cache_file):
            # Check cache age (1 hour max for local development, never in CI)
            age = (datetime.utcnow() - datetime.utcfromtimestamp(os.path.getmtime(self.cache_file))).total_seconds()
            if age < 3600:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return f.read()

        url = f"https://github.com/users/{self.username}/contributions"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                html = res.read().decode("utf-8")
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    f.write(html)
                return html
        except Exception as e:
            if os.path.exists(self.cache_file):
                print(f"⚠ Warning: Could not fetch live contributions ({e}). Serving cached snapshot.", file=sys.stderr)
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return f.read()
            raise RuntimeError(f"Failed to fetch contributions for @{self.username}: {e}")

    def parse_contributions(self, html: str) -> Dict[str, Any]:
        """Parse raw HTML into structured contribution calendar and metrics."""
        tooltip_map = {}
        for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.DOTALL):
            tid = m.group(1)
            text = m.group(2)
            if "No contribution" in text or "no contribution" in text:
                tooltip_map[tid] = 0
            else:
                num_match = re.search(r'(\d+)\s+contribution', text)
                tooltip_map[tid] = int(num_match.group(1)) if num_match else 0

        days = []
        for m in re.finditer(r'<td[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>', html):
            tag = m.group(0)
            date_m = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
            level_m = re.search(r'data-level="(\d+)"', tag)
            id_m = re.search(r'id="([^"]+)"', tag)
            if date_m and level_m:
                date_str = date_m.group(1)
                level = int(level_m.group(1))
                cell_id = id_m.group(1) if id_m else None
                count = tooltip_map.get(cell_id, 0)
                # Fallback: if count was 0 but level was positive
                if count == 0 and level > 0:
                    count = level
                days.append({"date": date_str, "level": level, "count": count})

        days.sort(key=lambda d: d["date"])
        if not days:
            raise ValueError("No contribution days parsed from HTML.")

        # Compute Streaks
        idx = len(days) - 1
        if days[idx]["count"] == 0:
            idx -= 1
        current_streak = 0
        c_end = days[idx]["date"] if idx >= 0 and days[idx]["count"] > 0 else None
        while idx >= 0 and days[idx]["count"] > 0:
            current_streak += 1
            idx -= 1
        c_start = days[idx + 1]["date"] if current_streak > 0 else None

        longest_streak = 0
        l_start = l_end = None
        cur_run = 0
        cur_run_start = None
        for i, d in enumerate(days):
            if d["count"] > 0:
                if cur_run == 0:
                    cur_run_start = d["date"]
                cur_run += 1
                if cur_run > longest_streak:
                    longest_streak = cur_run
                    l_start = cur_run_start
                    l_end = d["date"]
            else:
                cur_run = 0

        # Monthly Totals
        monthly_dict: Dict[str, int] = {}
        for d in days:
            m_key = d["date"][:7]
            monthly_dict[m_key] = monthly_dict.get(m_key, 0) + d["count"]

        monthly_totals = []
        for m_key in sorted(monthly_dict.keys()):
            dt = datetime.strptime(m_key, "%Y-%m")
            monthly_totals.append({
                "key": m_key,
                "label": dt.strftime("%b"),
                "year": dt.year,
                "count": monthly_dict[m_key]
            })

        # Weekdays
        weekdays_count = [0] * 7
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for d in days:
            dt = datetime.strptime(d["date"], "%Y-%m-%d")
            weekdays_count[dt.weekday()] += d["count"]

        busiest_wd_idx = weekdays_count.index(max(weekdays_count))
        busiest_weekday = {
            "name": weekday_names[busiest_wd_idx],
            "short": weekday_names[busiest_wd_idx][:3],
            "count": weekdays_count[busiest_wd_idx]
        }

        # Busiest Day
        busiest_day_record = max(days, key=lambda d: d["count"])
        b_dt = datetime.strptime(busiest_day_record["date"], "%Y-%m-%d")
        busiest_day = {
            "date": busiest_day_record["date"],
            "count": busiest_day_record["count"],
            "weekday": weekday_names[b_dt.weekday()][:3]
        }

        total_contributions = sum(d["count"] for d in days)
        active_days = sum(1 for d in days if d["count"] > 0)

        # 53 Weeks Array (Sun to Sat)
        weeks = []
        current_week = []
        first_dt = datetime.strptime(days[0]["date"], "%Y-%m-%d")
        first_sun_offset = (first_dt.weekday() + 1) % 7

        for _ in range(first_sun_offset):
            current_week.append(None)

        for d in days:
            current_week.append(d)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        if current_week:
            while len(current_week) < 7:
                current_week.append(None)
            weeks.append(current_week)

        # Highest month
        highest_month = max(monthly_totals, key=lambda m: m["count"]) if monthly_totals else None

        return {
            "username": self.username,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "total_contributions": total_contributions,
            "active_days": active_days,
            "total_calendar_days": len(days),
            "current_streak": {
                "days": current_streak,
                "start": c_start,
                "end": c_end
            },
            "longest_streak": {
                "days": longest_streak,
                "start": l_start,
                "end": l_end
            },
            "highest_month": highest_month,
            "busiest_day": busiest_day,
            "busiest_weekday": busiest_weekday,
            "monthly_totals": monthly_totals,
            "weeks_count": len(weeks),
            "weeks": weeks,
            "days": days
        }

    def run(self, force: bool = False, out_path: str = OUT_PATH) -> Dict[str, Any]:
        """Fetch, parse, and export contributions data to JSON."""
        html = self.fetch_raw_html(force=force)
        data = self.parse_contributions(html)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✔ Exported contributions to {out_path} ({data['total_contributions']} contributions across {data['weeks_count']} weeks).")
        return data
