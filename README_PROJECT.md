# Harmit Kalal — GitHub Profile Architecture & SVG Engineering Framework

An enterprise-grade, autonomous, data-driven GitHub Profile experience engineered for **Harmit Kalal** (`@Harmitx7`). Built with pure Python 3.11, custom vector graphics primitives, deterministic statistical models, and zero third-party runtime widget dependencies.

---

## ⚡ Key Highlights

- **Zero Third-Party Brittle Widgets**: No dependence on external services like `github-readme-stats.vercel.app`, `streak-stats`, or `profile-counter`. All telemetry cards and charts are native, self-hosted SVGs.
- **Zero Fabrication Guarantee**: 100% of statistics, repositories, code volumes, and language ratios reflect real, verified GitHub API telemetry (15 repositories, 11 stars, 12.05 MB code across 12 languages).
- **Sub-50KB Camo Proxy Compliance**: All vector assets conform strictly to GitHub's Camo caching proxy and sanitization boundaries (zero `<script>`, zero `<foreignObject>`, zero inline event listeners, valid standalone XML).
- **Accessible Motion Design**: Subtle GPU-accelerated CSS keyframe animations with automated `@media (prefers-reduced-motion: reduce)` static fallbacks.
- **Automated CI/CD Synchronization**: GitHub Actions pipeline runs every 12 hours via `.github/workflows/update-profile.yml` with least-privilege permissions (`contents: write`) and loop prevention (`[skip ci]`).

---

## 📁 Repository Directory Structure

```
Harmitx7/
├── .github/
│   └── workflows/
│       ├── snake.yml                  # 12-hour contribution grid snake animation workflow
│       └── update-profile.yml         # Automated telemetry sync, build & validation pipeline
├── assets/                            # Production SVGs referenced directly by README.md
│   ├── contributions.svg              # Shipping cadence & weekly activity waveform
│   ├── footer.svg                     # Cyber telemetry closing badge & signature
│   ├── hero.svg                       # Signature introduction & identity banner
│   ├── languages.svg                  # Polyglot language spectrum & byte breakdown
│   ├── projects.svg                   # Flagship systems engineering showcase
│   ├── skill-tree.svg                 # 4-tier skill architecture matrix
│   ├── statistics.svg                 # Real-time repository metrics & verified telemetry
│   ├── status-bar.svg                 # Live activity ticker & operational status
│   ├── terminal-boot.svg              # Interactive-style developer console manifest
│   └── generated/                     # Duplicate mirror of generated assets for resilient paths
├── data/                              # Normalized data models and API snapshots
│   ├── available_metrics.json         # Aggregated metric summaries & language bytes
│   ├── profile.json                   # Verified GitHub user profile data
│   ├── repositories.json              # Repository metadata, stars, topics, byte counts
│   └── cache/                         # Rate-limit resilient raw API cache (7-day validity)
├── design/                            # Visual identity tokens & component specifications
│   ├── tokens.json                    # OKLCH/HEX color palette, elevation & border tokens
│   ├── typography.json                # Monospace & system sans font hierarchies
│   └── components.md                  # Atomic design specifications
├── docs/                              # Engineering documentation & architectural audits
│   ├── ANIMATION_GUIDE.md             # Motion system, keyframes & accessibility rules
│   ├── ARCHITECTURE.md                # In-depth technical architecture blueprint
│   ├── COMPONENT_CATALOG.md           # API reference & specifications for all 9 SVGs
│   ├── COMPONENT_MAP.md               # Visual mapping of README layout hierarchy
│   ├── CONTENT_HIERARCHY.md           # Content strategy & editorial guidelines
│   ├── DEPLOYMENT.md                  # CI/CD deployment guide & GitHub Actions manual
│   ├── DESIGN_SYSTEM.md               # Complete design philosophy & token spec
│   ├── INTEGRATION_SNIPPETS.md        # Copy-paste markdown & HTML integration snippets
│   ├── MAINTENANCE.md                 # Maintenance playbook & troubleshooting runbook
│   ├── PROFILE_AUDIT.md               # Initial GitHub data audit & profile baseline
│   ├── QA_REPORT.md                   # Comprehensive quality assurance certification
│   ├── README_BLUEPRINT.md            # Structural ASCII wireframe & layout contract
│   └── TECHNICAL_CONSTRAINTS.md       # GitHub Camo & SVG sanitization boundaries
├── generated/                         # Direct output directory from build scripts
├── scripts/                           # Developer utilities & production runners
│   ├── build.py                       # Master build orchestrator (fetch -> gen -> sync -> test)
│   ├── sync_github_data.py            # Standalone API synchronization utility
│   ├── validate.py                    # SVG well-formedness & security auditor
│   └── visual_audit.py                # Contrast, link integrity & broken asset checker
├── src/                               # Pure Python 3.11 core engine
│   ├── api/                           # GitHub REST/GraphQL API integration with backoff
│   │   ├── __init__.py
│   │   └── github_client.py
│   ├── data/                          # Ingestion, normalization & statistics calculations
│   │   ├── __init__.py
│   │   ├── collector.py
│   │   ├── normalizer.py
│   │   └── statistics.py
│   ├── generators/                    # Component-specific SVG layout renderers
│   │   ├── __init__.py
│   │   ├── contributions.py
│   │   ├── footer.py
│   │   ├── hero.py
│   │   ├── languages.py
│   │   ├── projects.py
│   │   ├── skill_matrix.py
│   │   ├── statistics.py
│   │   ├── status_bar.py
│   │   └── terminal_boot.py
│   ├── svg/                           # Reusable SVG primitives, styles, filters & animations
│   │   ├── __init__.py
│   │   ├── animation.py
│   │   ├── filters.py
│   │   ├── gradients.py
│   │   ├── layouts.py
│   │   ├── primitives.py
│   │   └── typography.py
│   ├── utils/                         # Validation, formatting & color math
│   │   ├── __init__.py
│   │   ├── colors.py
│   │   ├── formatting.py
│   │   └── validation.py
│   └── main.py                        # CLI entrypoint for SVG component generation
├── tests/                             # Automated test suite (38 unit & integration tests)
│   ├── test_animation.py
│   ├── test_api_client.py
│   ├── test_data_pipeline.py
│   ├── test_engine.py
│   └── test_generators.py
├── pyproject.toml                     # Python packaging & tool configuration
├── README.md                          # Production GitHub Profile README
├── README_PROJECT.md                  # This developer & architectural manual
└── requirements.txt                   # Pinned developer & testing dependencies
```

---

## 🚀 Quickstart & Local Development

### Prerequisites

- Python 3.11 or newer.
- Git.
- Optional: GitHub Personal Access Token (for local unauthenticated rate limit bypass).

### 1. Clone & Setup

```bash
git clone https://github.com/Harmitx7/Harmitx7.git
cd Harmitx7

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

### 2. Run the Automated Build

The master build script runs data collection, statistical calculation, SVG rendering, asset synchronization, and XML validation in a single command:

```bash
# Full build with asset synchronization
python scripts/build.py --sync-assets

# Build offline (using cached data/ models)
python scripts/build.py --sync-assets

# Force live fetch from GitHub API
python scripts/build.py --sync-assets --force-fetch
```

### 3. Run Automated Tests & Audits

```bash
# Run unit test suite (38 tests)
python -m unittest discover -s tests -v

# Run SVG security & XML well-formedness audit
python scripts/validate.py

# Run comprehensive visual, contrast & link auditor
python scripts/visual_audit.py
```

---

## 🛠️ CLI Utilities Reference

The generation framework provides granular control via `src/main.py`:

```bash
# Generate all 9 SVG components
python src/main.py --all --out-dir generated

# Generate only specific components
python src/main.py --section hero --section statistics

# Generate static fallbacks (animations disabled)
python src/main.py --all --static --out-dir generated/static

# Synchronize generated files into assets/
python src/main.py --all --sync-assets
```

---

## 🔒 Security & Privacy

1. **GitHub Camo Proxy Strictness**: All SVGs contain zero `<script>` tags, zero `on*` inline events, zero `<foreignObject>`, and zero external font `@import` calls.
2. **Secret Hygiene**: Zero tokens or personal access credentials are committed or printed in logs. GitHub Actions leverages `${{ secrets.GITHUB_TOKEN }}` with scoped read/write permissions.
3. **Data Verification**: Statistics are calculated directly from public GitHub API responses. No simulated metrics or fake counters are permitted.

---

## 📖 Extended Documentation Index

- [docs/ARCHITECTURE.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/ARCHITECTURE.md) — System Architecture Blueprint & Data Pipeline Design
- [docs/MAINTENANCE.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/MAINTENANCE.md) — Routine Maintenance, Customization & Troubleshooting Playbook
- [docs/COMPONENT_CATALOG.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/COMPONENT_CATALOG.md) — Component Directory, Dimensions & API Specs
- [docs/DEPLOYMENT.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/DEPLOYMENT.md) — CI/CD Automation, Triggers & GitHub Actions Guide
- [docs/DESIGN_SYSTEM.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/DESIGN_SYSTEM.md) — Visual Identity, Spatial Grid & Token Hierarchy
- [docs/QA_REPORT.md](file:///c:/Users/sunrise/Desktop/pfojects/New%20folder%20(2)/Harmitx7/docs/QA_REPORT.md) — Formal Quality Assurance Audit Certification

---

## 👤 Author & Architecture License

Designed and engineered by **Harmit Kalal** (`@Harmitx7`).  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).
