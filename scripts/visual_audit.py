"""
Visual, Accessibility, Link Integrity, and SVG Architecture Auditor.
Performs comprehensive quality assurance checks across README.md, SVGs, and tokens.
"""

import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.utils.colors import hex_to_rgb
from src.utils.validation import validate_svg_file


def get_relative_luminance(hex_code: str) -> float:
    """Calculate relative luminance for WCAG contrast calculation."""
    r, g, b = hex_to_rgb(hex_code)
    rgb = [c / 255.0 for c in (r, g, b)]
    lum = []
    for c in rgb:
        if c <= 0.03928:
            lum.append(c / 12.92)
        else:
            lum.append(math.pow((c + 0.055) / 1.055, 2.4))
    return 0.2126 * lum[0] + 0.7152 * lum[1] + 0.0722 * lum[2]


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG 2.2 contrast ratio between two hex colors."""
    l1 = get_relative_luminance(hex1)
    l2 = get_relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class VisualAuditor:
    def __init__(self, repo_root: str = REPO_ROOT):
        self.root = repo_root
        self.issues: List[Dict[str, str]] = []

    def record_issue(self, severity: str, category: str, location: str, message: str, fix: str) -> None:
        self.issues.append({
            "severity": severity,
            "category": category,
            "location": location,
            "message": message,
            "fix": fix,
        })

    def audit_contrast_ratios(self) -> None:
        """Audit design token color pairs against WCAG 2.2 AA (4.5:1 body, 3:1 graphical)."""
        bg_void = "#05070B"
        bg_surface = "#0C1017"

        test_pairs = [
            ("Text Primary on Void", "#F8FAFC", bg_void, 4.5),
            ("Text Secondary on Surface", "#CBD5E1", bg_surface, 4.5),
            ("Text Muted on Surface", "#64748B", bg_surface, 3.0),
            ("Cyan Accent on Void", "#00F0FF", bg_void, 3.0),
            ("Mint Accent on Void", "#00E676", bg_void, 3.0),
            ("Tangerine Accent on Void", "#FF6B00", bg_void, 3.0),
            ("Amber Accent on Surface", "#FBBF24", bg_surface, 3.0),
            ("Coral Accent on Surface", "#F43F5E", bg_surface, 3.0),
        ]

        for label, fg, bg, min_ratio in test_pairs:
            ratio = calculate_contrast_ratio(fg, bg)
            if ratio < min_ratio:
                self.record_issue(
                    severity="HIGH",
                    category="Accessibility",
                    location=f"Color Token ({label})",
                    message=f"Contrast ratio {ratio:.2f}:1 is below required {min_ratio}:1.",
                    fix=f"Increase lightness of foreground {fg} or darkness of background {bg}."
                )

    def audit_readme_references(self) -> None:
        """Scan README.md for broken local assets and third-party widget dependencies."""
        readme_path = os.path.join(self.root, "README.md")
        if not os.path.exists(readme_path):
            self.record_issue("CRITICAL", "Structure", "README.md", "README.md not found.", "Create README.md.")
            return

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for brittle third-party dynamic widgets
        third_party_patterns = [
            (r"github-readme-stats\.vercel\.app", "github-readme-stats.vercel.app"),
            (r"streak-stats\.demolab\.com", "streak-stats.demolab.com"),
            (r"profile-counter\.glitch\.me", "profile-counter.glitch.me"),
        ]

        for pattern, domain in third_party_patterns:
            if re.search(pattern, content):
                self.record_issue(
                    severity="HIGH",
                    category="Reliability",
                    location="README.md",
                    message=f"README relies on brittle external third-party widget from '{domain}'.",
                    fix=f"Replace '{domain}' widget with self-hosted, Python-generated SVG from assets/generated/."
                )

        # Audit local image and picture source references (e.g. src="./cards/hero-light.svg?v=...", srcset="./cards/hero-dark.svg?v=...")
        img_srcs = re.findall(r'<(?:img|source)\s+[^>]*(?:src|srcset)="([^"]+)"', content)
        for src in img_srcs:
            if src.startswith("./") or not src.startswith("http"):
                # Strip URL query parameters (?v=...) and hash fragments before path resolution
                path_only = src.split("?")[0].split("#")[0]
                clean_src = path_only.lstrip("./").replace("/", os.sep)
                target_path = os.path.join(self.root, clean_src)
                if not os.path.exists(target_path):
                    self.record_issue(
                        severity="CRITICAL",
                        category="Broken Asset",
                        location="README.md",
                        message=f"Referenced local asset '{src}' does not exist on disk.",
                        fix=f"Generate or copy '{src}' into expected path {target_path}."
                    )

    def audit_svg_assets(self) -> None:
        """Audit all SVG assets across assets/ and generated/ directories."""
        dirs_to_scan = [
            os.path.join(self.root, "assets"),
            os.path.join(self.root, "assets", "generated"),
            os.path.join(self.root, "generated"),
        ]

        for d in dirs_to_scan:
            if not os.path.exists(d):
                continue
            for fname in os.listdir(d):
                if fname.endswith(".svg"):
                    fpath = os.path.join(d, fname)
                    rel_path = os.path.relpath(fpath, self.root)
                    is_valid, errors = validate_svg_file(fpath)
                    if not is_valid:
                        for err in errors:
                            self.record_issue(
                                severity="CRITICAL" if "Security" in err else "HIGH",
                                category="SVG Compliance",
                                location=rel_path,
                                message=err,
                                fix="Correct XML or remove forbidden attribute/tag."
                            )

    def run_full_audit(self) -> List[Dict[str, str]]:
        """Run complete quality audit."""
        self.audit_contrast_ratios()
        self.audit_readme_references()
        self.audit_svg_assets()
        return self.issues


def main():
    auditor = VisualAuditor()
    issues = auditor.run_full_audit()

    print("=" * 76)
    print("HARMITX7 COMPREHENSIVE QUALITY ASSURANCE & VISUAL AUDIT")
    print("=" * 76)

    critical_count = sum(1 for i in issues if i["severity"] == "CRITICAL")
    high_count = sum(1 for i in issues if i["severity"] == "HIGH")
    med_count = sum(1 for i in issues if i["severity"] == "MEDIUM")
    low_count = sum(1 for i in issues if i["severity"] == "LOW")

    print(f"Total Issues Detected: {len(issues)} (Critical: {critical_count}, High: {high_count}, Medium: {med_count}, Low: {low_count})")
    print("-" * 76)

    for idx, iss in enumerate(issues, 1):
        print(f"[{iss['severity']}] #{idx} ({iss['category']}) in {iss['location']}:")
        print(f"  Issue: {iss['message']}")
        print(f"  Fix:   {iss['fix']}\n")

    if critical_count > 0:
        print("✖ Audit FAILED: Critical issues must be resolved.", file=sys.stderr)
        sys.exit(1)
    else:
        print("✔ No Critical blockers detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
