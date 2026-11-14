# Technical Constraints Specification: GitHub Profile SVG & README Architecture

**Document Version**: 1.0.0  
**Target Repository**: `Harmitx7/Harmitx7`  
**Scope**: GitHub README Markdown Rendering, Camo Image Proxy, SVG Sanitization, Animation Boundaries, Typography, Mobile Responsiveness, and Automation Architecture.

---

## 1. GitHub README Markdown Rendering Boundaries

GitHub processes profile READMEs through a custom rendering pipeline that applies GitHub Flavored Markdown (GFM) and a strict HTML sanitizer (`html-pipeline` / Sanitizer API).

### Permitted vs. Forbidden HTML Elements

| Permitted Elements | Heavily Restricted / Sanitized | Strictly Forbidden (Stripped) |
| :--- | :--- | :--- |
| `<div>`, `<span>`, `<p>`, `<br>` | `<table>`, `<tr>`, `<td>`, `<th>` (limited attributes) | `<script>`, `<style>` (at root level) |
| `<a>` (with `href`, `target`) | `<details>`, `<summary>` (native disclosure widgets) | `<iframe>`, `<embed>`, `<object>`, `<applet>` |
| `<img>` (src, alt, width, height, align) | `<picture>`, `<source>` (prefers-color-scheme) | `<form>`, `<input>`, `<button>`, `<select>` |
| `<code>`, `<pre>`, `<blockquote>`, `<h1>`–`<h6>` | `<ul>`, `<ol>`, `<li>`, `<hr>` | Any element with `onclick`, `onload`, `onerror` |

### Key Markdown Rules:
1. **Zero Runtime JavaScript**: GitHub strips all `<script>` tags, inline event listeners (`onload`, `onclick`, `onmouseover`), and `javascript:` URIs. All interactivity must be pure CSS or declarative SVG.
2. **Style Attributes**: Inline `style="..."` attributes on standard Markdown HTML elements are stripped or severely curtailed. Positioning via `position: absolute`, `z-index`, or arbitrary flexbox in raw Markdown HTML is discarded.
3. **Table Formatting**: Tables are supported for side-by-side card layout (`<td width="50%" valign="top">`), but table borders and cell padding must rely on GitHub's native stylesheet.

---

## 2. GitHub Camo Image Proxy Architecture

When images or SVGs are referenced in a README, GitHub routes them through its caching proxy: `camo.githubusercontent.com`.

### Camo Proxy Behaviors:
- **Header Anonymization**: Strips client `Cookie`, `Authorization`, and `User-Agent` headers before fetching the origin image.
- **Cache Policy**: Camo respects `Cache-Control` headers (e.g. `max-age`, `no-cache`, `must-revalidate`) and `ETag`. External third-party stat cards frequently serve aggressive `Cache-Control: public, max-age=14400` (4 hours) or get cached indefinitely by Camo, causing data staleness.
- **Size Limits**: Camo enforces a maximum file size limit (5 MB). For performant vector rendering, all generated profile SVGs must remain under **50 KB**.
- **Timeout & Downtime Vulnerability**: If an external image host (e.g., free Heroku dynos, Vercel free-tier hobby functions) takes > 10 seconds to respond or errors with 5xx, Camo renders a broken image badge.
- **Architectural Solution**: **Store all SVG assets directly within the repository** (`assets/` and `assets/generated/`) and commit updates via GitHub Actions. Repository-hosted SVGs are served from GitHub's native CDN with zero third-party availability risks.

---

## 3. SVG Sanitization & Security Standards

GitHub applies an aggressive XML/SVG sanitizer to all SVGs loaded via raw URLs or rendered directly in the DOM.

### Strict Sanitization Enforcement:
1. **Banned Elements**:
   - `<script>`: Discarded immediately.
   - `<iframe>`, `<object>`, `<embed>`: Discarded.
   - `<foreignObject>`: Disallowed or rendered inert when loaded inside `<img>` tags on GitHub. Do not rely on `<foreignObject>` for HTML text formatting.
2. **Banned Attributes**:
   - All `on*` event handlers (`onload`, `onclick`, `onerror`, `onanimationend`).
   - `href="javascript:..."` or `xlink:href="javascript:..."`.
3. **External Asset Blocking (CORS & CSP)**:
   - External images via `<image href="https://...">` are blocked or fail Camo proxy routing.
   - External font stylesheets via `<style> @import url(...); </style>` or `<link rel="stylesheet">` are blocked by GitHub's Content Security Policy.
4. **Self-Contained Requirement**:
   - Every SVG component must be 100% self-contained: all shapes, paths, gradients, filters, styles, and typography stacks must be defined within the single `<svg>` document.

---

## 4. Typography & Font Stacks

Because web fonts (e.g. Google Fonts) cannot be loaded externally inside GitHub-rendered SVGs, typography must utilize high-performance, universally available system font stacks.

### Standard System Font Stacks:

#### Monospace / Technical Telemetry Stack (Primary):
```css
font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Monaco, Consolas, 'Courier New', monospace;
```

#### Editorial / Sans-Serif Header Stack:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
```

### Font Size & Scaling Constraints:
- When scaled down to mobile viewports (360px–420px), fonts smaller than `10px` become illegible.
- Primary text must be `12px` to `15px`.
- Micro-labels / coordinates must be at minimum `10px` with generous `letter-spacing` (0.5px–1.5px).
- Numerical metrics must use `font-variant-numeric: tabular-nums` or monospace font families to prevent optical jitter.

---

## 5. Animation Protocols: CSS vs. SMIL & Reduced-Motion

### Supported SVG Animation:
- **CSS `@keyframes` Animation**: Fully supported within SVG `<style>` blocks when rendered via `<img>` tags on modern Chromium, WebKit, and Gecko browsers.
- **Hardware-Accelerated Properties**: Use `transform` (rotate, translate, scale) and `opacity`. Avoid animating layout-triggering properties like `x`, `y`, `width`, `height`, or `stdDeviation` which cause high CPU load.
- **SMIL Animation (`<animate>`, `<animateTransform>`)**: Inconsistent across browser engines and deprecated in several rendering pipelines. Banned in this architecture in favor of CSS `@keyframes`.

### Non-Negotiable Accessibility Fallback:
Every animated SVG **must** implement a strict prefers-reduced-motion media query:
```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    animation: none !important;
    opacity: 1 !important;
  }
}
```
Static fallbacks ensure zero flickering, zero disorientation for vestibular-sensitive users, and 100% legibility in non-interactive viewing contexts.

---

## 6. Mobile Responsiveness & Viewport Mathematics

GitHub profiles are viewed on screens ranging from 360px (mobile) to 2560px+ (4K displays).

### Viewport Specifications:
- **GitHub Desktop README Container Width**: Between 896px and 1012px.
- **GitHub Mobile App / Web Viewport Width**: 360px to 420px.

### Vector Coordinate Rules:
1. **Never use fixed pixel widths**: Omit `width="960px"` on the SVG root tag.
2. **Always define standard `viewBox` and responsive fluid width**:
   ```xml
   <svg width="100%" viewBox="0 0 1000 400" fill="none" xmlns="http://www.w3.org/2000/svg">
   ```
3. **Aspect Ratio Preservation**: Use `preserveAspectRatio="xMidYMid meet"` (default) so vector assets scale proportionally without vertical or horizontal clipping.
4. **Transform Box for CSS Rotation**: Modern SVG engines require `transform-box: view-box;` or `transform-box: fill-box;` paired with `transform-origin: Xpx Ypx;` to guarantee rotation anchors do not drift when scaled across different viewports.

---

## 7. Color Contrast & Theme Adaptability

GitHub supports Light, Dark, and High Contrast Dark modes.

### Theme Strategy:
1. **Self-Contained Cosmic / Void Surface**:
   - Rather than relying on transparent backgrounds that can wash out or clash with both white and black backgrounds, use self-contained dark container capsules (`rx="12"`, background `#020205` to `#0A0E1A`) with subtle luminous rims (`stroke-width="1"`) and high-contrast foreground text (`#F8FAFC`, `#E2E8F0`, `#38BDF8`, `#00F0FF`, `#00E676`).
   - This guarantees consistent optical contrast (exceeding WCAG 2.2 AA ratio of 4.5:1 for normal text and 7:1 for headers) on both dark and light GitHub interfaces.
2. **Markdown-Level Dynamic Theme Switching**:
   - For assets that require distinct light and dark variants (e.g. contribution snake), use the HTML5 `<picture>` syntax:
   ```html
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="path/to/dark.svg"/>
     <source media="(prefers-color-scheme: light)" srcset="path/to/light.svg"/>
     <img src="path/to/dark.svg" width="100%" alt="Visual Component"/>
   </picture>
   ```

---

## 8. GitHub API Limits & Automation Architecture

### API Quota Constraints:
| Authentication Tier | REST API Limit | GraphQL API Limit | Search API Limit |
| :--- | :---: | :---: | :---: |
| **Unauthenticated (Public)** | 60 requests / hour | 0 (Forbidden) | 10 requests / min |
| **Actions `GITHUB_TOKEN`** | 1,000 requests / hour | Supported | 30 requests / min |
| **Personal Access Token (PAT)** | 5,000 requests / hour | 5,000 points / hour | 30 requests / min |

### Automation Architecture & Invariant Rules:
1. **No Live API Calls inside README**: A README is static Markdown; it cannot fetch live REST APIs at browser render time.
2. **Offline Resilience / Fallback Fixture**: Any Python generation script must accept a local fallback fixture (`data/profile.json` and `data/repositories.json`) so it executes deterministically even if GitHub APIs return 403 (Rate Limit Exceeded) or network is unavailable.
3. **Scheduled CI/CD Updates**: GitHub Actions pipeline `.github/workflows/profile-telemetry.yml` runs on a 12-hour cron schedule with `workflow_dispatch` manual trigger, commits updated generated SVGs to the repository, and relies exclusively on the automatic `${{ secrets.GITHUB_TOKEN }}`.
4. **Secret Safety**: No private access tokens, emails, or personal identifiers are hardcoded into scripts or committed to Git.
