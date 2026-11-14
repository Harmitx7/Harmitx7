import os
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
README_PATH = os.path.join(REPO_ROOT, "README.md")
PREVIEW_HTML = os.path.join(REPO_ROOT, "docs", "preview.html")
SCREENSHOT_PATH = os.path.join(REPO_ROOT, "docs", "preview_github.png")

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Create GitHub-accurate profile container
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>GitHub Profile Preview - Harmit Kalal</title>
  <style>
    body {{
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 40px 20px;
      display: flex;
      justify-content: center;
    }}
    .container {{
      width: 100%;
      max-width: 896px;
      background-color: #0d1117;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 32px;
      box-sizing: border-box;
    }}
    a {{
      color: #58a6ff;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    img {{
      max-width: 100%;
      box-sizing: border-box;
    }}
    p {{
      margin-top: 0;
      margin-bottom: 16px;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <div class="container">
    {content}
  </div>
</body>
</html>"""

# Fix relative card paths in HTML preview
html = html.replace('src="./cards/', f'src="file:///{REPO_ROOT.replace(os.sep, "/")}/cards/')
html = html.replace('src="cards/', f'src="file:///{REPO_ROOT.replace(os.sep, "/")}/cards/')

with open(PREVIEW_HTML, "w", encoding="utf-8") as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1800})
    page.goto(f"file:///{PREVIEW_HTML.replace(os.sep, '/')}")
    page.wait_for_timeout(1000)
    page.screenshot(path=SCREENSHOT_PATH, full_page=True)
    browser.close()

print(f"✔ Screenshot saved to: {SCREENSHOT_PATH}")
