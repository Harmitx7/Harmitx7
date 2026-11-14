"""
Standalone CI/CD SVG Validation Runner.
Verifies: XML well-formedness, zero script tags, zero event listeners, viewBox presence, and size limits.
"""

import os
import sys

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.utils.validation import validate_svg_file


def run_validation() -> bool:
    """Scan and validate all SVG assets across production directories."""
    print("=" * 70)
    print("HARMITX7 SVG ASSET SECURITY & WELL-FORMEDNESS AUDIT")
    print("=" * 70)

    directories_to_scan = [
        os.path.join(REPO_ROOT, "cards"),
    ]

    total_inspected = 0
    total_passed = 0
    failures = []

    for d in directories_to_scan:
        if not os.path.exists(d):
            continue
        print(f"\nInspecting directory: {os.path.relpath(d, REPO_ROOT)}")
        for fname in sorted(os.listdir(d)):
            if fname.endswith(".svg"):
                total_inspected += 1
                fpath = os.path.join(d, fname)
                size_kb = os.path.getsize(fpath) / 1024
                is_valid, errors = validate_svg_file(fpath)

                if is_valid:
                    total_passed += 1
                    print(f"  ✔ {fname:<24} ({size_kb:>5.1f} KB) — PASS")
                else:
                    failures.append((fpath, errors))
                    print(f"  ✖ {fname:<24} ({size_kb:>5.1f} KB) — FAILED", file=sys.stderr)
                    for err in errors:
                        print(f"    - {err}", file=sys.stderr)

    print("\n" + "-" * 70)
    print(f"Audit Complete: {total_passed}/{total_inspected} SVG assets nominal.")
    if failures:
        print(f"✖ Total Failures: {len(failures)}", file=sys.stderr)
        return False
    print("✔ All assets conform to GitHub Camo, XML, and Security specifications.")
    return True


if __name__ == "__main__":
    success = run_validation()
    if not success:
        sys.exit(1)
