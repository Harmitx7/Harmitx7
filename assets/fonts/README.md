# System Fonts Architecture

GitHub's strict Content Security Policy (CSP) forbids loading web fonts (`@font-face` pointing to Google Fonts, Typekit, or external CDNs) inside SVGs rendered through the Camo image proxy.

### Supported Universal System Font Stacks:
1. **Technical Monospace (Default)**:
   ```css
   font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', 'Fira Code', Menlo, Monaco, Consolas, monospace;
   ```
2. **Editorial Sans-Serif**:
   ```css
   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
   ```

No external `.woff2` or `.ttf` files are bundled to keep repository size lean and eliminate network latency.
