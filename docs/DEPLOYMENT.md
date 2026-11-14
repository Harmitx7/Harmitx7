# Automated Build & Deployment Architecture

**Target Repository**: `Harmitx7/Harmitx7`  
**Document**: `docs/DEPLOYMENT.md`  
**Pipeline**: GitHub Actions (`.github/workflows/update-profile.yml`)

---

## 1. Automated Generation Workflow Overview

The GitHub Profile README relies on live, automated data synchronization without brittle client-side widgets or runtime JavaScript. The entire build, validation, and deployment pipeline runs deterministically within GitHub Actions:

```
┌────────────────────────────────────────────────────────┐
│ 1. TRIGGERS                                            │
│    • Scheduled Execution: Every 12 hours (0 */12 * * *)│
│    • Manual Trigger: workflow_dispatch via GitHub UI   │
│    • Code Push: Triggers on src/ or scripts/ changes   │
│      (ignoring assets/** and data/** to prevent loops) │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. ENVIRONMENT INITIALIZATION                          │
│    • Ubuntu Latest / Python 3.11                       │
│    • Pip dependency cache from requirements.txt        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. TEST GATES (Strict Failure Barrier)                 │
│    • python -m unittest discover -s tests -v           │
│    • 38 Automated Unit & Integration Tests             │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. LIVE INTELLIGENCE INGESTION & DATA EXPORT           │
│    • Fetches public profile, repos, languages, events  │
│    • Applies 3-attempt bounded retry backoff           │
│    • Normalizes data and exports to data/              │
│    • Rate Limit Immunity: Preserves cache on 403       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. SVG GENERATION & ASSET SYNCHRONIZATION              │
│    • Generates all 9 SVG components via src/main.py    │
│    • Synchronizes to assets/ and assets/generated/     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 6. ASSET SECURITY & XML INTEGRITY AUDIT                │
│    • python scripts/validate.py                        │
│    • Validates XML well-formedness, viewBox, & sizes   │
│    • Strict zero-tolerance for <script> or event tags  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 7. IDEMPOTENT GIT COMMIT & PUSH                        │
│    • Evaluates git diff --staged --quiet               │
│    • Commits ONLY if generated files have changed      │
│    • Appends [skip ci] to prevent recursive triggers   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Security & Least Privilege Boundaries

1. **Token Scoping**:
   - The workflow uses standard `${{ secrets.GITHUB_TOKEN }}` provided by GitHub Actions.
   - Minimal required permission is `contents: write` to allow committing updated SVG assets and JSON cache records.
   - No personal access tokens (PAT) or external secrets are required.
2. **Token Secrecy**:
   - `src/api/github_client.py` never logs or prints the token.
   - In standard stdout/stderr logs, all authorization headers are concealed.
3. **Infinite Loop Prevention**:
   - `paths-ignore` blocks changes to `assets/**`, `generated/**`, `data/**`, `docs/**`, and `README.md` from triggering workflow runs.
   - Automated commits specify `[skip ci]` in the commit message.

---

## 3. Resilience & Rate-Limit Cache Fallback

- **GitHub API Quota**: Unauthenticated requests are limited to 60/hr; within GitHub Actions, `${{ secrets.GITHUB_TOKEN }}` provides **1,000 requests/hr**.
- **Graceful Fallback**: If GitHub APIs return `403 Forbidden` (rate limit exceeded) or network timeouts occur, `src/api/github_client.py` transparently serves cached snapshots from `data/cache/` (retaining valid data for up to 7 days).
- **Last Known Good Assets**: The pipeline never deletes or overwrites existing SVGs with empty or corrupt files. If generation fails, existing assets are preserved.

---

## 4. Local Execution & Verification

To run the complete build and validation suite locally:

```bash
# 1. Run unit test suite
python -m unittest discover -s tests -v

# 2. Run full automated build & asset synchronization
python scripts/build.py --sync-assets

# 3. Validate all SVG assets
python scripts/validate.py

# 4. Generate static fallbacks (optional)
python src/main.py --all --static --out-dir generated/static
```

---

## 5. Manual Regeneration via GitHub UI

1. Navigate to repository on GitHub: `https://github.com/Harmitx7/Harmitx7`
2. Click on the **Actions** tab.
3. Select **Update Profile Telemetry & SVGs** from the left workflow menu.
4. Click **Run workflow** -> select branch `main` -> click green **Run workflow** button.
5. Inspect the execution logs. If data has changed, the bot commits updated SVGs within ~45 seconds.
