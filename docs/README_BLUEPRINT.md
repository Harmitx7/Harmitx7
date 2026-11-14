# Complete README Architecture Blueprint: Editorial OS

**Target Profile**: Harmit Kalal (@Harmitx7)  
**System Architecture**: Spatial Editorial HUD  
**Document**: `docs/README_BLUEPRINT.md`  
**Status**: Approved Architecture Blueprint

---

## 1. ASCII Wireframe: Full-Page Composition

### Desktop Viewport (~896px - 1012px Container Width)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ SECTION 1 & 2: SIGNATURE ANIMATED INTRO & IDENTITY (hero.svg)                 │
│ ┌──────────────────────────────────────────────────┬────────────────────────┐ │
│ │ 23.02°N, 72.57°E // AHMEDABAD, IN                │                        │ │
│ │                                                  │     ORBITAL HUD        │ │
│ │ Harmit Kalal                                     │     CELESTIAL REACTOR  │ │
│ │ AI SYSTEMS ARCHITECT // DISTRIBUTED INFRA        │                        │ │
│ │                                                  │     (cx=770, cy=195)   │ │
│ │ ◈ AGENTIC GOVERNANCE   ◈ TELEMETRY SIMULATION    │     3 Planetary Rings  │ │
│ │ ◈ MALWARE DECEPTION    ◈ COUNTERFACTUAL AI       │     Continuous Orbit   │ │
│ └──────────────────────────────────────────────────┴────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 10: SOCIAL NAVIGATION DOCK (Editorial High-Contrast Badges)           │
│ [LinkedIn] [GitHub] [Portfolio: harmit.vercel.app] [npm: tribunal-kit] [Email]│
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 5 & 9: ACTIVE SHIPPING TELEMETRY TICKER (status-bar.svg)              │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ (◉) SYSTEM STATUS: OPERATIONAL  | SPRINT: tribunal-kit v3.0 | WINNER: BoI │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 2 & 9: DEVELOPER CONSOLE MANIFEST (terminal-boot.svg)                 │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ ● ● ● harmit@system-architect: ~/tribunal-kit/manifest.json  BUILD: PASS  │ │
│ │ 01 {                                                                      │ │
│ │ 02   "architect": "Harmit Kalal",                                         │ │
│ │ 03   "flagship": "tribunal-kit",                                          │ │
│ │ 04   "subagent_driven_development": true,                                 │ │
│ │ 05   "agents": 52, "reviewers": 21,                                       │ │
│ │ 06   "acf_metrics": { "compression": "27x", "hallucination_rate": "0.0%" }│ │
│ │ 07 }                                                                      │ │
│ │ [ ✔ AUDIT PASSED // 0 HALLUCINATIONS DETECTED // ZERO-TRUST ACTIVE ]      │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 4: FEATURED PROJECT DOSSIERS (2-Column Markdown Architecture Grid)    │
│ ┌─────────────────────────────────────┬─────────────────────────────────────┐ │
│ │ 🎯 tribunal-kit                     │ 🏆 ARGUS-X                          │ │
│ │ Anti-Hallucination Multi-Agent AI   │ Hypothesis-Driven Mobile Malware    │ │
│ │ 52 Agents · 40 Workflows · Rust/Node│ Bank of India Hackathon Winner      │ │
│ │ `npx tribunal-kit init`             │ Python · Shadow-Data Deception      │ │
│ ├─────────────────────────────────────┼─────────────────────────────────────┤ │
│ │ 🃏 ClashVision v3.0                 │ 🏎️ F1 Telemetry Dashboard           │ │
│ │ AI Battle Predictor & RL Policy     │ High-Frequency F1 Telemetry Engine  │ │
│ │ PyTorch · Kaggle S18 · Locate3B     │ FastAPI · DuckDB · Deterministic Sim│ │
│ └─────────────────────────────────────┴─────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 8: REAL GITHUB DEVELOPMENT TELEMETRY (assets/generated/metrics-hud.svg│
│ ┌───────────────────┬───────────────────┬───────────────────┬───────────────┐ │
│ │ 15                │ 11                │ 1                 │ 7             │ │
│ │ PUBLIC REPOSITORIES│ TOTAL STARS       │ TOTAL FORKS       │ FOLLOWERS     │ │
│ └───────────────────┴───────────────────┴───────────────────┴───────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 7: LANGUAGE POLYGLOT SPECTRUM (assets/generated/languages.svg)        │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ LANGUAGE POLYGLOT SPECTRUM (12.05 MB Audited Source Code)                 │ │
│ │ [JS: 54.98%] [Python: 23.17%] [TS: 8.23%] [Java: 5.72%] [Rust: 2.67%] ... │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 3: 4-TIER SKILL ARCHITECTURE MATRIX (skill-tree.svg)                  │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ TIER 1: AI & AGENTIC INFRASTRUCTURE (LLM Orchestration, SDD, MCP, .acf)   │ │
│ │ TIER 2: SYSTEMS & BACKEND (FastAPI, Rust Engines, Node.js, DuckDB, Async) │ │
│ │ TIER 3: WEB & INTERACTIVE (Next.js 15, React, tRPC, 60fps Physics, SVG)  │ │
│ │ TIER 4: CYBERSECURITY & DEVOPS (Threat Analysis, Docker, CI/CD, Linux)    │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 9: ARCHITECTURAL PRINCIPLES & DESIGN SYSTEM TABLE                     │
│ ┌──────────────────────┬───────────────────────────────┬────────────────────┐ │
│ │ Pillar               │ Engineering Mechanism         │ Impact Metric      │ │
│ ├──────────────────────┼───────────────────────────────┼────────────────────┤ │
│ │ Semantic Distillation│ .acf token compression        │ 27x context shrink │ │
│ │ Shadow-Data Deception│ Dynamic malware trigger-graphs│ 0 false positives  │ │
│ │ Deterministic Sim    │ High-frequency interpolation  │ Sub-ms lap compare │ │
│ │ Counterfactual AI    │ NVIDIA Locate3B + RL scoring  │ PCI Battle Predict │ │
│ └──────────────────────┴───────────────────────────────┴────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 6: CONTRIBUTION SNAKE TELEMETRY (Platane snk / <picture> dark-light)  │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ ░░▒▒▓▓██ [Contribution Snake Animation: Dark / Light Auto-Switch] ██▓▓▒▒░░│ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│ SECTION 11: CYBER TELEMETRY FOOTER (footer.svg)                               │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ ~~~ Harmonic Coordinate Waves ~~~                                         │ │
│ │ AHMEDABAD, IN (23.02°N, 72.57°E) · COMPUTER ENGINEERING · INDUS UNIVERSITY│ │
│ │                          ●   ●   ●   ●                                    │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Specifications for all 11 Required Sections

### Section 1: Signature Animated Introduction
- **Purpose**: Establishes high-craft artistic authority immediately upon landing.
- **Component**: `assets/hero.svg` (viewBox: `0 0 1000 400`).
- **Content Source**: Verified identity facts (`Harmit Kalal`, GPS coordinates, architectural pillars).
- **Visual Mechanics**: Ultra-wide cosmic capsule with multi-stop radial void gradients and triple-ring continuous orbital mechanics (`cx=770, cy=195`).
- **Responsive Behavior**: Scalable vector with `preserveAspectRatio="xMidYMid meet"`, fluid `width="100%"`.
- **Fallback Strategy**: `@media (prefers-reduced-motion: reduce)` halts rotation at statically balanced angles with 100% opacity.

### Section 2: Personal Identity & Professional Positioning
- **Purpose**: Articulates core engineering identity as an AI Systems Architect & Creative Engineer.
- **Component**: Embedded in `hero.svg` and `terminal-boot.svg`.
- **Content Source**: `docs/PROFILE_AUDIT.md`, `data/profile.json`.
- **Visual Mechanics**: High-contrast typography hierarchy (44px display, 13px monospace subtitle, 14-line JSON manifest).
- **Responsive Behavior**: Monospace text scales proportionally within SVG viewBox; line heights remain fixed relative to coordinate canvas.

### Section 3: Technical Expertise Visualization
- **Purpose**: Demonstrates depth across 4 full-stack architectural disciplines (26 verified modules).
- **Component**: `assets/skill-tree.svg` (viewBox: `0 0 960 500`).
- **Content Source**: Audited code repositories (`tribunal-kit`, `ClashVision`, `F1-Telemetry`, `SmartSplitApp`).
- **Visual Mechanics**: 4 tiered horizontal capsules with color-coded signal beacons (Cyan, Tangerine, Mint, Coral) and constellation link vectors.
- **Responsive Behavior**: 11.5px minimum font size guarantees mobile legibility even at 50% scale (360px viewport).

### Section 4: Featured Projects
- **Purpose**: Directs technical recruiters and open-source contributors to the 4 flagship systems.
- **Component**: 2x2 Markdown table grid (`<td width="50%" valign="top">`).
- **Content Source**: `data/repositories.json` + hackathon records.
- **Visual Mechanics**: Side-by-side balanced card layout with emoji anchors, concise blockquote descriptions, technology tags, and syntax-highlighted quick starts (`npx tribunal-kit init`).
- **Responsive Behavior**: On desktop renders as 2 columns (50%/50%); GitHub mobile app automatically stacks `<td>` cells into a readable single-column flow.

### Section 5: GitHub Activity Visualization
- **Purpose**: Demonstrates active shipping telemetry and current development focus.
- **Component**: `assets/status-bar.svg` (viewBox: `0 0 960 72`).
- **Content Source**: Recent GitHub push events (`tribunal-kit v3.0`, active sprint).
- **Visual Mechanics**: Slim horizontal capsule with pulsing sonar radar beacon (`@keyframes sonarRipple`) and operational status indicators.
- **Fallback Strategy**: Static beacon and solid status text for reduced-motion.

### Section 6: Contribution History
- **Purpose**: Visualizes contribution density and streak momentum.
- **Component**: HTML5 `<picture>` wrapping Platane contribution snake SVGs.
- **Content Source**: GitHub Actions workflow (`.github/workflows/snake.yml`).
- **Visual Mechanics**: Dark and light theme auto-switching via `<source media="(prefers-color-scheme: dark)">`.
- **Responsive Behavior**: Fluid 100% width.

### Section 7: Language Distribution
- **Purpose**: Transparent, evidence-backed proof of polyglot engineering mastery.
- **Component**: `assets/generated/languages.svg` (viewBox: `0 0 960 180`).
- **Content Source**: Python script calculating real bytes from GitHub REST API (12.05 MB audited code).
- **Visual Mechanics**: Multi-segment proportional horizontal spectrum bar + high-density legend with exact byte counts and percentages.
- **Responsive Behavior**: Pure SVG, self-scaling.

### Section 8: Development Statistics
- **Purpose**: Displays verified account-level metrics without third-party rate limits or downtime.
- **Component**: `assets/generated/metrics-hud.svg` (viewBox: `0 0 960 170`).
- **Content Source**: Aggregated metrics from `data/available_metrics.json` (15 repos, 11 stars, 1 fork, 7 followers).
- **Visual Mechanics**: 4 modular dark pods with tabular numerals and last-sync timestamp.
- **Fallback Strategy**: Cached local JSON fixture prevents broken images if API is rate-limited.

### Section 9: Current Focus & Interests
- **Purpose**: Communicates architectural methodology, research principles, and engineering philosophy.
- **Component**: Architectural Principles Markdown Table + Dev Philosophy Blockquote.
- **Content Source**: `.acf` semantic distillation, shadow-data deception, deterministic physics simulation.
- **Visual Mechanics**: Clean 3-column table with bold impact metrics + collapsible `<details>` for historical quests.

### Section 10: Contact & Social Links
- **Purpose**: Clear, accessible conversion paths for collaboration, networking, and hiring.
- **Component**: Social Navigation Dock.
- **Content Source**: LinkedIn (`harmitkalal`), Portfolio (`harmit.vercel.app`), npm (`tribunal-kit`), Email (`harmitkalal7@gmail.com`).
- **Visual Mechanics**: Centered high-contrast badge capsules with brand logos.

### Section 11: Custom Closing Signature
- **Purpose**: Professional geographic and institutional anchor closing the profile narrative.
- **Component**: `assets/footer.svg` (viewBox: `0 0 1000 140`).
- **Content Source**: Ahmedabad, IN coordinates (23.02°N, 72.57°E), Indus University Computer Engineering.
- **Visual Mechanics**: Harmonic wave vectors, starlight crosshairs, and quad-color verification nodes.
