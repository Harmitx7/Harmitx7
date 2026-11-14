import os
from playwright.sync_api import sync_playwright

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
hero_svg = os.path.join(repo_root, "cards", "hero.svg")
output_png = os.path.join(repo_root, "docs", "hero_preview.png")

svg_url = "file:///" + hero_svg.replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1000, "height": 520})
    page.goto(svg_url)
    page.wait_for_timeout(1000)
    page.screenshot(path=output_png)
    browser.close()

print("Hero screenshot saved to:", output_png)
