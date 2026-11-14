# Component & Asset Architecture Map

**System**: Harmitx7 Editorial OS  
**Document**: `docs/COMPONENT_MAP.md`

---

## 1. Master Component Registry

| Sec # | Section Name | Physical Implementation Path | Component Architecture | Primary Data Source | Refresh Mechanism | Fallback Mechanism |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Signature Intro | `assets/hero.svg` | Handcrafted Vector SVG | Static Identity Metadata | Manual / Asset Update | `@media (prefers-reduced-motion)` static state |
| **02** | Personal Positioning | `assets/hero.svg` & `terminal-boot.svg` | Handcrafted Vector SVG | `docs/PROFILE_AUDIT.md` | Manual / Asset Update | Static text in SVG canvas |
| **03** | Technical Expertise | `assets/skill-tree.svg` | Handcrafted Vector SVG | 26 Audited Modules | Manual / Asset Update | Static vector capsules |
| **04** | Featured Projects | `README.md` (Table Grid) | Semantic Markdown Table | `data/repositories.json` | Manual / Markdown Update | Native Markdown text flow |
| **05** | GitHub Activity | `assets/status-bar.svg` | Handcrafted Vector SVG | Live Sprint & Hackathon Data| Manual / Asset Update | Static sonar beacon |
| **06** | Contribution History| Remote `output` branch | `<picture>` + Platane SVG | GitHub Commit Graph | CI/CD 12-hour cron (`snake.yml`)| Dark/Light static SVG |
| **07** | Language Spectrum | `assets/generated/languages.svg` | Python-Generated SVG | GitHub REST `/languages` | CI/CD 12-hour cron (`profile-telemetry.yml`)| `data/repositories.json` cached fixture |
| **08** | Development Metrics| `assets/generated/metrics-hud.svg` | Python-Generated SVG | GitHub REST `/users` & `/repos` | CI/CD 12-hour cron (`profile-telemetry.yml`)| `data/available_metrics.json` cached fixture |
| **09** | Focus & Philosophy | `README.md` (Tables & Details) | Markdown Tables & Details | System Architecture Pillars | Manual / Markdown Update | Pure Markdown native rendering |
| **10** | Contact & Social | `README.md` (Badge Anchor Dock) | Markdown Anchors + Badges | Social & Deployment URLs | Manual / Markdown Update | Direct Markdown text links |
| **11** | Closing Signature | `assets/footer.svg` | Handcrafted Vector SVG | GPS & Academic Coordinates | Manual / Asset Update | Static harmonic wave |

---

## 2. Data Flow & Automation Architecture

```
                                  GITHUB ECOSYSTEM
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
         [GitHub REST API]                             [GitHub Commit Graph]
      /users/Harmitx7, /repos, /languages                        │
                 │                                               │
                 ▼                                               ▼
     [.github/workflows/profile-telemetry.yml]          [.github/workflows/snake.yml]
                 │                                               │
                 ▼                                               ▼
     [scripts/generate_profile_svgs.py]                 [Platane/snk Generator]
                 │                                               │
        ┌────────┴────────┐                                      │
        ▼                 ▼                                      ▼
  [languages.svg]  [metrics-hud.svg]                     [github-snake.svg]
  assets/generated/ assets/generated/                     output branch
        │                 │                                      │
        └─────────────────┼──────────────────────────────────────┘
                          │
                          ▼
                  [Harmitx7/README.md]
              Served via GitHub Camo Proxy
              Zero External Runtime Failures
```
