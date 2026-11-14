# SVG Component Directory & Visual Architecture Catalog

**Target Repository**: `Harmitx7/Harmitx7`  
**System**: `Harmitx7 Profile Architecture (Reference-Inspired Portfolio Release)`  
**Document**: `docs/COMPONENT_CATALOG.md`  
**Version**: `2.0.0-PORTFOLIO`  
**Total Production Cards**: 13 Handcrafted SVG Cards in `cards/`

---

## Architectural Inspiration & Reference Analysis

This component suite was architected with inspiration from **Avi Vashishta's** profile architecture (`AVIVASHISHTA29/AVIVASHISHTA29`), featuring:
- Dedicated standalone SVG cards compiled into `cards/`.
- Embedded subsetted Base64 WOFF typography (`Geist Mono`, `Geist`).
- 53-week live contribution calendar and 12-month activity spectrum.
- Three horizontal signature visual cards arranged with `width="33.333%"` for desktop multi-column snapping.
- Bespoke **Editorial Dark OS / Cyber Observatory** identity tailored specifically to **Harmit Kalal** (`@Harmitx7`).

---

## Production Cards Index (`cards/`)

| Card Asset | Module / Function | Dimensions | Size | Primary Function & Motion |
|---|---|:---:|:---:|---|
| **[`cards/hero.svg`](#1-cardsherosvg--signature-cyber-hud-hero)** | `render_hero_card()` | `880 × 310` | ~27.5 KB | Identity header, radar beacon, rotating orbital constellation |
| **[`cards/heatmap.svg`](#2-cardsheatmapsvg--53-week-contribution-calendar)** | `render_heatmap_card()` | `880 × 205` | ~46.9 KB | 53-week contribution calendar, 250 commits, staggered cell cascade |
| **[`cards/activity.svg`](#3-cardsactivitysvg--monthly-activity-spectrum)** | `render_activity_card()` | `880 × 250` | ~17.3 KB | 13-month contribution bars, peak month highlight (Mar: 42), streaks |
| **[`cards/build.svg`](#4-three-signature-horizontal-tiles)** | `render_tile_build()` | `286 × 240` | ~12.6 KB | 04A // BUILD: tribunal-kit multi-agent framework & .acf engine |
| **[`cards/secure.svg`](#4-three-signature-horizontal-tiles)** | `render_tile_secure()` | `286 × 240` | ~12.0 KB | 04B // SECURE: ARGUS-X mobile malware analysis & shadow deception |
| **[`cards/simulate.svg`](#4-three-signature-horizontal-tiles)** | `render_tile_simulate()` | `286 × 240` | ~12.0 KB | 04C // SIMULATE: F1 telemetry dashboard & ClashVision RL policy |
| **[`cards/title-systems-dark.svg`](#5-adaptive-section-title-banners)** | `render_title_card(dark)` | `880 × 70` | ~11.1 KB | Flagship repository section title (dark theme) |
| **[`cards/title-systems-light.svg`](#5-adaptive-section-title-banners)** | `render_title_card(light)`| `880 × 70` | ~11.1 KB | Flagship repository section title (light theme) |
| **[`cards/repo-tribunal-kit.svg`](#6-featured-repository-cards)** | `render_repo_card(...)` | `286 × 210` | ~12.2 KB | Showcase card: tribunal-kit (JavaScript / Rust, 6 stars) |
| **[`cards/repo-clashvision.svg`](#6-featured-repository-cards)** | `render_repo_card(...)` | `286 × 210` | ~12.2 KB | Showcase card: ClashVision v3.0 (Python / RL, 2 stars) |
| **[`cards/repo-f1-telemetry.svg`](#6-featured-repository-cards)** | `render_repo_card(...)` | `286 × 210` | ~12.2 KB | Showcase card: F1-TELEMETRY (Python / Physics, 0 stars) |
| **[`cards/developer-panel.svg`](#7-cardsdeveloper-panelsvg--developer-console-dossier)**| `render_developer_panel()` | `880 × 250` | ~14.0 KB | Terminal & neofetch architectural dossier with blinking prompt |
| **[`cards/footer.svg`](#8-cardsfootersvg--closing-cryptographic-signature)** | `render_footer_card()` | `880 × 90` | ~11.2 KB | Cryptographic signature HUD & SHA-256 telemetry stamp |

---

## 1. `cards/hero.svg` — Signature Cyber-HUD Hero

- **Dimensions**: ViewBox `0 0 880 310` (Fluid `width="100%"`).
- **Embedded Fonts**: `Geist Mono` (Base64 WOFF) & `Geist` Sans.
- **Visual Structure**:
  - Top: Coordinates telemetry (`LAT 19.0760 LON 72.8777`), pulsating emerald beacon, system status.
  - Left: Headline typography `Harmit Kalal`, professional mandate `AI Systems Engineer & System Architect`, mission narrative, and 3 high-contrast pill badges (`tribunal-kit`, `BOI × IIT-H Winner`, `12.05 MB Code`).
  - Right: Bespoke Cyber Architect Constellation Orb featuring rotating dual elliptical orbits (`animation: orbit 24s linear infinite`), coordinate compass grids, and central glowing nucleus.
- **Entrance**: Staggered `rise` keyframes (0.1s to 0.4s).

---

## 2. `cards/heatmap.svg` — 53-Week Contribution Calendar

- **Dimensions**: ViewBox `0 0 880 205` (Fluid `width="100%"`).
- **Data Source**: Scraped live from `https://github.com/users/Harmitx7/contributions` (371 days parsed).
- **Features**:
  - 53 weekly columns × 7 day rows.
  - Exact 250 verified contributions across 100 active days.
  - 5-level Cyber Cyan intensity palette (`#101622` to `#00F0FF`).
  - Column-grouped CSS fade-in cascade (`0.05s` to `0.45s`).
  - Dynamic month labels (`Nov` to `Nov`) and weekday indicators (`M`, `W`, `F`).
  - Less-to-more intensity legend and active cadence badge.

---

## 3. `cards/activity.svg` — Monthly Activity Spectrum

- **Dimensions**: ViewBox `0 0 880 250` (Fluid `width="100%"`).
- **Features**:
  - 13 monthly bars with proportional height scaling.
  - Peak velocity highlighted in Electric Cyan: **March 2026 (42 commits)**.
  - Staggered CSS `grow` bar animation (`transform-origin: bottom; animation-delay: ...`).
  - 4 bottom telemetry pods:
    1. Total Contributions: `250 COMMITS`
    2. Longest Streak: `5 DAYS CONSECUTIVE`
    3. Busiest Weekday: `Monday (51 COMMITS)`
    4. Active Days Velocity: `100 / 371 DAYS (27%)`

---

## 4. Three Signature Horizontal Tiles

Arranged in `README.md` on one continuous HTML line with `width="33.333%"` each:

```html
<a href="https://github.com/Harmitx7/tribunal-kit"><img src="./cards/build.svg" width="33.333%" /></a><a href="mailto:harmitkalal7@gmail.com"><img src="./cards/secure.svg" width="33.333%" /></a><a href="https://github.com/Harmitx7/F1-TELEMETRY-DASHBOARD"><img src="./cards/simulate.svg" width="33.333%" /></a>
```

### Tile Specifications (`286 × 240` each)
- **`cards/build.svg`**:
  - Header: `04A // BUILD`
  - System: `tribunal-kit` (Anti-Hallucination AI)
  - Glyph: Interconnected multi-agent neural DAG mesh.
  - Metric: `27x Context Compression · TypeScript · Rust`
- **`cards/secure.svg`**:
  - Header: `04B // SECURE`
  - System: `ARGUS-X` (Malware Deception)
  - Glyph: Cyber shield with threat radar vector.
  - Metric: `BOI × IIT-H Winner · Python · MITRE`
- **`cards/simulate.svg`**:
  - Header: `04C // SIMULATE`
  - System: `F1 & ClashVision` (Telemetry & RL Policy)
  - Glyph: High-frequency telemetry sine trace.
  - Metric: `Sub-ms Physics Interpolation · FastAPI · DuckDB`

---

## 5. Adaptive Section Title Banners

- **`cards/title-systems-dark.svg` & `cards/title-systems-light.svg`**:
  - Dimensions: `880 × 70`.
  - Rendered via `<picture>` tag in GitHub Markdown to automatically shift contrast between GitHub Dark/Dimmed and GitHub Light themes.

---

## 6. Featured Repository Cards

Arranged horizontally at `width="33.333%"`:
- **`cards/repo-tribunal-kit.svg`**: JavaScript / Rust · 6 stars · 1 fork · Anti-hallucination multi-agent framework.
- **`cards/repo-clashvision.svg`**: Python · 2 stars · 0 forks · AI battle predictor & RL policy engine.
- **`cards/repo-f1-telemetry.svg`**: Python · 0 stars · 0 forks · Formula 1 high-frequency telemetry simulation.

---

## 7. `cards/developer-panel.svg` — Developer Console Dossier

- **Dimensions**: ViewBox `0 0 880 250` (Fluid `width="100%"`).
- **Visual Style**: macOS/Linux terminal console with red/yellow/green control pips.
- **Left Column**: System specs, operating entity, framework runtimes, code volume analyzed (12.05 MB across 15 repos), and uptime target.
- **Right Column**: Polyglot languages, framework specializations, cyber defense techniques, hackathon honors, and active command prompt with blinking cursor `_`.

---

## 8. `cards/footer.svg` — Closing Cryptographic Signature

- **Dimensions**: ViewBox `0 0 880 90` (Fluid `width="100%"`).
- **Details**:
  - Verification signature: `HARMIT KALAL // ARCHITECTURAL IDENTITY VERIFIED`
  - Telemetry hash: `SHA-256: 7e9b8f2d4c01a5e39b74f0a2d1e8c9b3`
  - Status indicator: `0 THIRD-PARTY WIDGETS // 100% CAMO COMPLIANT`
  - Automation schedule: `SCHEDULED GITHUB ACTIONS AUTOMATION ACTIVE · SYNCHRONIZED TWICE DAILY`
