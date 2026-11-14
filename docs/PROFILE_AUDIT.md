# GitHub Intelligence & Reconnaissance Audit: @Harmitx7

**Audit Timestamp**: 2026-11-14T07:38:00Z  
**Target Profile**: [github.com/Harmitx7](https://github.com/Harmitx7)  
**Target Repository**: `Harmitx7/Harmitx7`  
**Analyst**: Senior Software Architect & GitHub Data Analyst  
**Epistemic Baseline**: L1 Evidence-Backed (Public GitHub API & Repository Inspection)

---

## 1. Executive Summary

An exhaustive reconnaissance of GitHub account `Harmitx7` was conducted across public REST and GraphQL endpoints, HTML profile rendering, and repository metadata. 

The audit establishes:
- **15 public repositories** totaling **12,050,494 bytes** of source code.
- **Polyglot codebase distribution** dominated by JavaScript (54.98%) and Python (23.17%), followed by TypeScript (8.23%), Java (5.72%), and Rust (2.67%).
- **Primary Flagship System**: `tribunal-kit` (Anti-Hallucination Multi-Agent AI Framework), with 16 engineering topics, active November 2026 commits, and public npm distribution.
- **Accurate Metric Boundaries**: Public stars sum to **11**, forks sum to **1**, followers count is **7**, and public gists are **0**. Total annual contributions and private stats require authenticated GraphQL scoping and must not be fabricated or approximated.
- **Pinned Repositories**: The user has **0 pinned repositories** configured on their public GitHub profile.

---

## 2. Profile Data: Available vs. Missing / Unknown

| Profile Field | Value in Public API | Status / Classification | Notes |
| :--- | :--- | :--- | :--- |
| **Username (`login`)** | `Harmitx7` | **Available** (L1) | Verified primary handle |
| **Display Name (`name`)** | `Harmit Kalal` | **Available** (L1) | Verified |
| **User ID** | `113524673` | **Available** (L1) | Numeric account ID |
| **Account Created** | `2022-09-14T12:58:44Z` | **Available** (L1) | ~4.1 years on GitHub |
| **Account Updated** | `2026-11-12T12:22:08Z` | **Available** (L1) | Active within past 48 hours |
| **Public Repositories** | `15` | **Available** (L1) | Verified across `/users/Harmitx7/repos` |
| **Followers** | `7` | **Available** (L1) | Exact count |
| **Following** | `4` | **Available** (L1) | Exact count |
| **Public Gists** | `0` | **Zero** (L1) | Exact zero count |
| **Bio** | `null` | **Unavailable** | Not populated on GitHub profile |
| **Company** | `null` | **Unavailable** | Not populated on GitHub profile |
| **Location (API)** | `null` | **Unavailable via API** | Profile README indicates `Ahmedabad, IN` |
| **Blog / Website** | `https://harmit.vercel.app/` | **Available** (L1) | Verified personal portfolio domain |
| **Twitter / X** | `null` | **Unavailable** | Not connected |
| **Pinned Repositories** | `[]` (Empty) | **Empty / Unconfigured** | No pinned items present in DOM |
| **Annual Contributions** | `Requires Token` | **Unknown without Auth** | Requires authenticated GraphQL call |

---

## 3. Repository Analysis & Catalog Breakdown

### Comprehensive Public Repository Inventory (15 Repositories)

| Repository | Primary Lang | Stars | Forks | Status / Topics | Description Highlights |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`tribunal-kit`** | JavaScript / Rust | **6** | **1** | Active (16 topics: `ai-agents`, `anti-hallucination`, `mcp-server`, `sdd`) | A universal, native-Rust governance layer for AI coding agents. Enforces Subagent-Driven Development (SDD) to stop hallucinations before they hit disk. |
| **`ClashVision-v3.0-PCI-RL-Kaggle-Season18-Dataset`** | Python | **2** | 0 | Public | AI cheat sheet for Clash Royale: predicts battles, scores PCI consistency, suggests card swaps, and serves tactics. |
| **`odoo`** | TypeScript | **2** | 0 | Public | Modular enterprise/business extensions. |
| **`SmartSplitApp`** | Java / Kotlin | **1** | 0 | Public | Privacy-first expense tracker. P2P Wi-Fi sync, QR join, PDF export, Bottle Green UI. |
| **`F1-TELEMETRY-DASHBOARD`** | Python | 0 | 0 | Public | Web dashboard for F1 telemetry analysis: speed, throttle, brake, RPM traces, sector delta, Plotly/Dash. |
| **`AI-Life-Simulator`** | Python | 0 | 0 | Public | Autonomous virtual human simulation: emergent habits, socialization, decision dynamics. |
| **`DeckReactor`** | JavaScript | 0 | 0 | Public | Live metrics and deck comparison for Clash Royale. |
| **`TransitOps`** | TypeScript | 0 | 0 | Public | Transportation / transit operations tooling. |
| **`ChronoDots`** | Python | 0 | 0 | Public | Visual utility for time tracking and scheduling. |
| **`SmartSplit_2.0`** | Python | 0 | 0 | Public | Second-generation expense distribution engine. |
| **`SmartSplit`** | JavaScript | 0 | 0 | Public | Early multi-party debt settlement tracker. |
| **`Gym-Forge`** | TypeScript | 0 | 0 | Public | Fitness tracking & workout logging interface. |
| **`harmit`** | HTML / JS | 0 | 0 | Public | Source repository for Vercel portfolio site. |
| **`Harmitx7`** | Markdown / SVG | 0 | 0 | Public | Special GitHub profile repository. |
| **`ClashVision--The-Live-Battle-Dashboard-For-Clash-Royal`** | Python | 0 | 0 | Public | Predecessor version of ClashVision battle engine. |

### Note on `ARGUS-X`
`ARGUS-X` (Hypothesis-Driven Mobile Malware Analysis Framework, Bank of India × IIT Hyderabad Hackathon Winner) is heavily featured in the user's profile README, but is **not** in the list of 15 public repositories. It is either an internal/private repository, housed under an institutional hackathon organization, or pending public release. In data-driven visualizations, it must be recognized as an external hackathon achievement rather than a public open-source repository with active GitHub stars/forks.

---

## 4. Aggregated Codebase Language Telemetry

Total audited code volume: **12,050,494 bytes (~12.05 MB)** across 15 repositories.

| Language | Volume (Bytes) | Share (%) | Primary Association |
| :--- | :---: | :---: | :--- |
| **JavaScript** | 6,625,968 | **54.98%** | `tribunal-kit`, `DeckReactor`, `SmartSplit` |
| **Python** | 2,792,707 | **23.17%** | `ClashVision`, `F1-TELEMETRY-DASHBOARD`, `AI-Life-Simulator` |
| **TypeScript** | 992,141 | **8.23%** | `TransitOps`, `odoo`, `Gym-Forge` |
| **Java** | 689,191 | **5.72%** | `SmartSplitApp` (Android Native P2P) |
| **Rust** | 321,836 | **2.67%** | `tribunal-kit` (Native core governance engine) |
| **CSS** | 261,461 | **2.17%** | Web frontends & dashboards |
| **HTML** | 217,620 | **1.81%** | Portfolio & dashboard templates |
| **Kotlin** | 83,591 | **0.69%** | `SmartSplitApp` Android extensions |
| **Shell** | 34,234 | **0.28%** | CI/CD, build tooling, installation scripts |
| **Other (<0.2%)** | 32,245 | **0.28%** | PHP, PowerShell, PLpgSQL, Batchfile, Mako |

---

## 5. Projects Deserving Featured Attention

Based on architectural depth, technological novelty, community traction, and verified descriptions, the top tier projects are:

1. **`tribunal-kit` (Tier 1 Flagship)**:
   - *Domain*: Agentic AI Governance, Multi-Agent Systems, Native Rust / Node.js
   - *Evidence*: 6 stars, 1 fork, 16 GitHub topics, active npm package, `.acf` context distillation engine, 52 specialist agents.
   - *Role*: Central anchor of the developer's identity.

2. **`ClashVision-v3.0` (Tier 2 High Innovation)**:
   - *Domain*: Applied Machine Learning, RL Policy Engines, Game Analytics
   - *Evidence*: 2 stars, Python/PyTorch, integration with Kaggle Season 18 dataset and NVIDIA LocateAnything-3B, computes Play Consistency Index (PCI).

3. **`F1-TELEMETRY-DASHBOARD` (Tier 2 Applied Engineering)**:
   - *Domain*: High-frequency telemetry, Deterministic Physics Simulation, Data Visualization
   - *Evidence*: Python, Dash, Plotly, Pandas, Fast/DuckDB telemetry processing.

4. **`SmartSplitApp` (Tier 2 Native Mobile & Decentralized Systems)**:
   - *Domain*: Privacy-First Mobile Security, Decentralized Local P2P Systems
   - *Evidence*: 1 star, Java/Kotlin, local Wi-Fi direct sync with zero cloud dependency.

---

## 6. Activity & Contribution Telemetry

- **Public Event Log**: 12 recent public events captured via REST `/users/Harmitx7/events/public`.
- **Event Breakdown**:
  - `PushEvent`: 8 (66.7%) — primary commit velocity directed toward `tribunal-kit`.
  - `CreateEvent`: 1 (8.3%) — branch/tag creation.
  - `DeleteEvent`: 2 (16.7%) — cleanup of temporary branches.
  - `WatchEvent`: 1 (8.3%) — repository starred.
- **Contribution History Caveat**: The contribution graph (green squares) cannot be computed with 100% historical accuracy from unauthenticated public REST endpoints alone, because private contributions and historical commit graphs require authenticated GraphQL access. The SVG snake workflow (`.github/workflows/snake.yml`) currently handles contribution snake generation through GitHub Actions where token permissions are granted.

---

## 7. Accurate Statistics That Can Safely Be Displayed

To adhere strictly to **Non-Negotiable Principle 1 (Never fabricate statistics)**:

| Statistic | Exact Value | Display Feasibility | Safe Visualization Format |
| :--- | :---: | :--- | :--- |
| **Public Repositories** | `15` | **100% Accurate** | Direct counter / HUD metric badge |
| **Total Public Stars** | `11` | **100% Accurate** | Cumulative star counter across public repos |
| **Total Public Forks** | `1` | **100% Accurate** | Secondary telemetry indicator |
| **Followers** | `7` | **100% Accurate** | Social proof node |
| **Primary Code Focus** | JS (55%), Python (23%), TS (8%) | **100% Accurate** | Proportional Polyglot Spectrum / Byte distribution bar |
| **Account Longevity** | Since Sept 2022 (~4 yrs) | **100% Accurate** | Architectural timeline timestamp |
| **Active Push Velocity** | `8` recent pushes | **100% Accurate** | Live heartbeat / activity status |
| **Third-Party Streak / Private Commits** | Variable / Unverified | **Brittle / Avoid** | Do not display unverifiable external badges |

---

## 8. Summary of Findings & Transition to Constraints

1. **Profile Character**: Harmit Kalal is an AI systems architect and creative engineer working at the intersection of Multi-Agent AI (`tribunal-kit`), Applied ML / RL (`ClashVision`), High-Frequency Telemetry (`F1 Telemetry`), and Decentralized Systems (`SmartSplitApp`).
2. **Current Deficiencies**: The repository previously relied on third-party Heroku/Vercel stats services that show generic cards, break under rate limits, and do not reflect the developer's bespoke aesthetic.
3. **Actionable Directive**: Replace third-party dynamic widgets with an in-house Python SVG generation engine running inside GitHub Actions, producing verified, data-driven SVGs that reflect exact public metrics.
