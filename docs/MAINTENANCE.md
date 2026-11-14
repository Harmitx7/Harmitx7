# Maintenance & Operations Playbook — Harmitx7 Profile Architecture

**Target Repository**: `Harmitx7/Harmitx7`  
**Audience**: Maintainers, Creative Developers, DevOps Engineers  
**Document**: `docs/MAINTENANCE.md`  
**Status**: Active Production Playbook

---

## 1. Routine Operations & Common Tasks

### 1.1 Forcing Live GitHub Data Refresh

By default, the engine caches API responses in `data/cache/` to operate quickly and avoid hitting GitHub's rate limits (60 req/hr unauthenticated, 1,000 req/hr authenticated).

To force a fresh synchronization against the live GitHub API:

```bash
# Option A: Run the master build with force-fetch
python scripts/build.py --sync-assets --force-fetch

# Option B: Run standalone data sync
python scripts/sync_github_data.py --force
```

If testing locally and experiencing HTTP 403 (Rate Limit), export a GitHub Personal Access Token in your terminal:
```bash
# Linux / macOS
export GITHUB_TOKEN="ghp_yourPersonalAccessTokenHere"

# Windows PowerShell
$env:GITHUB_TOKEN="ghp_yourPersonalAccessTokenHere"
```

---

### 1.2 Adding a New Flagship Project

When releasing a new major project, update it in two places:

1. **`README.md` Flagship Table**:
   - Open [README.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/README.md).
   - In `## ⟶ flagship_systems // active_engineering`, add or update a `<td>` cell in the markdown table.
   - Include project title, concise elevator pitch, tech stack badges, and verified GitHub link.
2. **`src/generators/projects.py` (Visual Showcase Card)**:
   - In `generate_projects_svg()`, inspect the list of showcased project tuples.
   - Adjust the title, description, or metrics.
   - Re-run `python scripts/build.py --sync-assets` to re-render [assets/projects.svg](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/assets/projects.svg).

---

### 1.3 Adding or Updating Skills in the Skill Tree Matrix

The 4-tier skill matrix in [assets/skill-tree.svg](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/assets/skill-tree.svg) is defined in [src/generators/skill_matrix.py](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/src/generators/skill_matrix.py).

To add a new skill node:
1. Open `src/generators/skill_matrix.py`.
2. Locate the `TIERS` configuration dictionary:
   - `TIER 1 — CORE PROTOCOLS`: System-level and foundation skills.
   - `TIER 2 — AI & MULTI-AGENT GOVERNANCE`: Agent frameworks, LLM evals, prompt defenses.
   - `TIER 3 — SYSTEMS, TELEMETRY & RUNTIMES`: High-frequency backends, telemetry, physics sim.
   - `TIER 4 — REVERSE ENGINEERING & DEFENSE`: Malware analysis, trigger-graphs, deception layers.
3. Add or update items within the target tier array.
4. Run:
   ```bash
   python src/main.py --section skill-tree --sync-assets
   python scripts/validate.py
   ```

---

### 1.4 Customizing the Color Palette & Design Tokens

All colors across all 9 SVG components are centralized in:
- Design Token Spec: [design/tokens.json](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/design/tokens.json)
- Python Color Library: [src/utils/colors.py](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/src/utils/colors.py)

To adjust a theme accent (e.g. changing the primary glow from Electric Cyan `#00F0FF` to Emerald Neon `#10B981`):
1. Update `COLOR_ACCENT_CYAN` in `src/utils/colors.py`.
2. Update the corresponding token in `design/tokens.json`.
3. Run the automated visual contrast audit to ensure the new color satisfies WCAG 2.2 AA (>= 4.5:1 text, >= 3.0:1 graphical):
   ```bash
   python scripts/visual_audit.py
   ```
4. Re-compile all components:
   ```bash
   python scripts/build.py --sync-assets
   ```

---

### 1.5 Adding a New SVG Component Generator

To add a new custom profile widget (e.g. `certification_radar.svg`):
1. Create `src/generators/certification_radar.py` implementing `generate_certification_radar_svg() -> str`.
2. Import reusable layout and shape primitives from `src.svg.primitives`, `src.svg.typography`, and `src.svg.animation`.
3. Register the new generator in [src/main.py](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/src/main.py) inside `GENERATORS`.
4. Add a unit test in [tests/test_generators.py](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/tests/test_generators.py).
5. Run the build suite:
   ```bash
   python scripts/build.py --sync-assets
   python -m unittest discover -s tests -v
   ```

---

## 2. Troubleshooting & Diagnostics

### Problem 1: GitHub Actions Fails with 403 Forbidden
- **Cause**: GitHub API secondary rate limits or unauthenticated IP throttles.
- **Remedy**: Ensure the GitHub Actions workflow contains `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`. The engine is programmed to gracefully serve cached data from `data/cache/` when rate-limited, preventing build failure.

### Problem 2: SVG Image Fails to Render on GitHub (Broken Image Icon)
- **Checklist**:
  1. Verify the file is under 50 KB (`ls -lh assets/`).
  2. Run `python scripts/validate.py` to ensure valid XML without `<script>`, `onload`, or `<foreignObject>`.
  3. Ensure the markdown reference in `README.md` uses a relative path: `<img src="./assets/filename.svg" ... />`.
  4. Note that GitHub Camo caches images for up to 24 hours. To verify raw rendering immediately, test via `https://raw.githubusercontent.com/Harmitx7/Harmitx7/main/assets/filename.svg`.

### Problem 3: Animated Circles or Paths Drift Off-Center
- **Cause**: Browser SVG CSS transform bug when `transform-box` is missing.
- **Remedy**: Always ensure animated elements have `transform-box: view-box;` and explicit `transform-origin: {cx}px {cy}px;`. Inspect [src/svg/animation.py](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/src/svg/animation.py) for the standard orbital animation helper.

### Problem 4: Git Push Fails in GitHub Actions (Permission Denied)
- **Cause**: Repository workflow settings do not grant write permissions.
- **Remedy**:
  1. Open repository on GitHub -> **Settings** -> **Actions** -> **General**.
  2. Scroll down to **Workflow permissions**.
  3. Select **Read and write permissions** and check **Allow GitHub Actions to create and approve pull requests**.
  4. Save changes.

---

## 3. Pre-Commit Validation Checklist

Before pushing any changes to `main`, execute this 3-step verification loop:

```bash
# 1. Run unit tests
python -m unittest discover -s tests -v

# 2. Run automated build & sync
python scripts/build.py --sync-assets

# 3. Run visual and security audits
python scripts/validate.py
python scripts/visual_audit.py
```

If all three commands exit with code `0`, your changes are guaranteed production-safe.
