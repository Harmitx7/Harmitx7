# SVG Motion Design System & Animation Guide

**System**: Editorial OS Motion Specification  
**Target Repository**: `Harmitx7/Harmitx7`  
**Document**: `docs/ANIMATION_GUIDE.md`  
**Status**: Authoritative Motion Engineering Standard

---

## 1. Core Motion Philosophy

Motion in the **Harmitx7 Editorial OS** serves exclusively as an informational hierarchy and mechanical signifier. It is deliberately understated, purposeful, and mathematically calibrated.

### Principles:
1. **Communicative Intent**: Motion must signal state (active execution, verified status, continuous telemetry) rather than act as decorative visual noise.
2. **Zero Aggressive Flashing**: Flashing rates exceeding 2Hz are strictly banned (WCAG 2.3.1 compliance).
3. **Hardware Acceleration**: Only properties that bypass browser reflow and layout recalculation (`transform`, `opacity`, and `stroke-dashoffset`) are animated.
4. **Non-Essential by Design**: Content must be 100% legible, complete, and understandable with all animations paused or absent.

---

## 2. GitHub Rendering Environment & Compatibility Analysis

GitHub renders SVGs within README documents through the `camo.githubusercontent.com` proxy and renders them inside standard `<img>` or `<picture>` elements.

### Rendering Engine Constraints:

| Technique | GitHub Compatibility | Status | Architectural Decision |
| :--- | :---: | :---: | :--- |
| **CSS `@keyframes` in `<style>`** | **Supported** | **APPROVED** | Primary animation standard across all profile components. |
| **`transform-box: view-box;`** | **Supported** | **APPROVED** | Mandatory for rotation to maintain fixed coordinate anchors. |
| **`stroke-dashoffset` Waves** | **Supported** | **APPROVED** | Used for harmonic waveform telemetry. |
| **SMIL (`<animate>`, `<set>`)** | **Deprecating** | **BANNED** | Inconsistent across Blink/WebKit and deprecated in modern SVG specifications. |
| **JavaScript / Script Tags** | **Stripped** | **BANNED** | Completely stripped by GitHub SVG sanitizer; fails Camo validation. |
| **External Fonts / `@import`** | **Blocked** | **BANNED** | Blocked by GitHub CSP; system font stacks are required. |

---

## 3. Motion Timing & Easing Hierarchy

### Easing Curves:
- **Mechanical Snap Easing** (`cubic-bezier(0.16, 1, 0.3, 1)`): Applied to reveals, sonar ripples, and modal entries. Produces an authoritative, high-precision instrument feel.
- **Organic Breathing** (`ease-in-out`): Applied to starlight pulses, node breathing, and ambient glows.
- **Deterministic Drift** (`linear`): Applied strictly to continuous celestial rotations and harmonic waveforms.

### Duration Tokens:

| Token | Duration | Easing | Applied Component |
| :--- | :--- | :--- | :--- |
| `motion.instant` | `150ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Micro-hover feedback |
| `motion.reveal` | `450ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Progress bar scales, initial text reveal |
| `motion.cursor` | `850ms` | `step-end` | Monospace terminal block cursor |
| `motion.pulse` | `2400ms` | `cubic-bezier(0.16, 1, 0.3, 1)` | Live operational sonar beacon ripple |
| `motion.breath` | `3000ms`–`4000ms` | `ease-in-out` | Core node glow, card border pulse |
| `motion.harmonic`| `9000ms`–`12000ms` | `linear` | Dual flowing wave vectors (footer.svg) |
| `motion.orbit` | `15s`, `22s`, `32s`| `linear` | Inner, core, and outer celestial orbit rings |

---

## 4. Component Motion Inventory

### 1. Hero Celestial Reactor (`assets/hero.svg`)
- **Orbital Revolutions**:
  - Inner Orbit (Tangerine, radius 105px, tilt 38°): 15.0s period counter-clockwise.
  - Core Orbit (Cyan, radius 130px, tilt -28°): 22.0s period clockwise.
  - Outer Orbit (Mint, radius 155px, tilt -72°): 32.0s period clockwise.
  - *Anchor Stability*: `transform-origin: 770px 195px; transform-box: view-box;` guarantees zero precession.
- **Node Breathing**: Central core node cycles between radius 6px and 8.5px over 3.0s.
- **Starlight Constellations**: 10 micro-points twinkle asynchronously using staggered `animation-delay` offsets (0.0s to 3.6s).

### 2. Operational Telemetry Ticker (`assets/status-bar.svg`)
- **Sonar Beacon Ripple**: Concentric ring expands from `r=4` (`opacity=0.9`) to `r=16` (`opacity=0`) over 2.4s.
- **Beacon Node Pulse**: Central green node pulses over 2.4s to signify live system status.

### 3. Developer Console Manifest (`assets/terminal-boot.svg`)
- **Traffic Light Nodes**: Subtle window control glow over 3.0s.
- **Terminal Cursor**: Blinking monospace prompt cursor (`step-end` at 0.85s).
- **Line Revealing**: Staggered translate and opacity fade from line 01 to line 14.

### 4. Language Spectrum (`assets/generated/languages.svg`)
- **Progress Reveal**: Smooth scaleX entry over 0.6s with `transform-origin: left;`.

### 5. Coordinate Wave Footer (`assets/footer.svg`)
- **Dual Harmonic Waves**: Continuous fluid wave with stroke-dasharray `14 8` and `10 12` cycling over 9.0s and 12.0s.

---

## 5. Accessibility & The Reduced-Motion Contract

Under **WCAG 2.2 Criterion 2.3.3 (Animation from Interactions)** and vestibular safety protocols, motion must yield to user operating system preferences.

Every animated stylesheet emitted by `AnimationEngine` includes:
```css
@media (prefers-reduced-motion: reduce) {
  .orbit-a, .orbit-b, .orbit-c, .sonar, .beacon-node,
  .wave-a, .wave-b, .bg-star, .glow-border, .spectrum-bar, .term-cur {
    animation: none !important;
    opacity: 1 !important;
  }
}
```

### Static Build Mode:
When generated with `--static`, the engine completely bypasses all `@keyframes` definitions and emits an authoritative static stylesheet:
```css
/* Static Mode Active */
* { animation: none !important; opacity: 1 !important; }
text { font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Consolas, monospace; }
```
This guarantees that static fallbacks maintain 100% optical balance without reliance on media query evaluation.

---

## 6. Performance & Rendering Budgets

1. **CPU Usage**: Because all animations target GPU compositor layers (`transform` and `opacity`), CPU utilization remains < 1% during active tab inspection.
2. **File Size Impact**: CSS `@keyframes` and class rules add less than **900 bytes** to each SVG document.
3. **Filter Optimization**: `feGaussianBlur` is capped at `stdDeviation="2.5"` and restricted to small visual nodes, preventing memory bloat on mobile WebKit and Chromium rasterizers.
