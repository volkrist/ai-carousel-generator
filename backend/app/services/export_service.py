import io
import zipfile
from typing import Any

from playwright.sync_api import sync_playwright

from app.services.storage_service import upload_file

SLIDE_W = 1080
SLIDE_H = 1350


def build_slide_html(slide: dict[str, Any], design: dict[str, Any]) -> str:
    bg_type = design.get("bg_type", "color")
    bg_color = design.get("bg_color", "#ffffff")
    bg_dim = float(design.get("bg_dim", 0.0) or 0.0)

    template = design.get("template", "classic")
    padding = int(design.get("layout_padding", 24) or 24)

    show_header = bool(design.get("show_header", False))
    header_text = design.get("header_text") or ""
    show_footer = bool(design.get("show_footer", True))
    footer_text = design.get("footer_text") or ""

    title = slide.get("title") or ""
    body = slide.get("body") or ""
    footer = slide.get("footer") or ""

    if template == "bold":
        title_size = 64
        body_size = 42
        title_weight = 800
    elif template == "minimal":
        title_size = 52
        body_size = 38
        title_weight = 600
    else:
        title_size = 56
        body_size = 40
        title_weight = 700

    background_css = f"background:{bg_color};"
    overlay_css = (
        f"background: rgba(0,0,0,{bg_dim});"
        if bg_dim > 0
        else "background: transparent;"
    )

    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body {{
      width: {SLIDE_W}px; height: {SLIDE_H}px;
      margin: 0; padding: 0;
      font-family: Arial, sans-serif;
    }}
    .slide {{
      position: relative;
      width: {SLIDE_W}px; height: {SLIDE_H}px;
      {background_css}
      overflow: hidden;
      box-sizing: border-box;
    }}
    .overlay {{
      position:absolute; inset:0;
      {overlay_css}
    }}
    .content {{
      position: relative;
      height: 100%;
      padding: {padding}px;
      display: flex;
      flex-direction: column;
      gap: 24px;
      box-sizing: border-box;
      color: #111827;
    }}
    .header {{
      font-size: 28px;
      opacity: 0.85;
    }}
    .title {{
      font-size: {title_size}px;
      font-weight: {title_weight};
      line-height: 1.05;
      margin-top: 12px;
    }}
    .body {{
      font-size: {body_size}px;
      line-height: 1.25;
      white-space: pre-wrap;
      flex: 1;
    }}
    .footer {{
      font-size: 26px;
      opacity: 0.8;
      display:flex;
      justify-content: space-between;
      gap: 12px;
    }}
    .small {{
      opacity: 0.75;
    }}
  </style>
</head>
<body>
  <div class="slide">
    <div class="overlay"></div>
    <div class="content">
      {"<div class='header'>" + header_text + "</div>" if show_header else ""}
      <div class="title">{title}</div>
      <div class="body">{body}</div>
      {"<div class='footer'><span>" + (footer_text or "") + "</span><span class='small'>" + (footer or "") + "</span></div>" if show_footer else ""}
    </div>
  </div>
</body>
</html>
"""
    return html


def render_png(html: str) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": SLIDE_W, "height": SLIDE_H, "deviceScaleFactor": 1}
        )
        page.set_content(html, wait_until="load")
        png = page.screenshot(type="png", full_page=True)
        browser.close()
        return png


def export_carousel_to_zip(
    slides: list[dict[str, Any]], design: dict[str, Any]
) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for i, slide in enumerate(slides, start=1):
            html = build_slide_html(slide, design)
            png = render_png(html)
            zf.writestr(f"slide_{i:02d}.png", png)
    return buf.getvalue()


def upload_export_zip(zip_bytes: bytes) -> dict:
    return upload_file(zip_bytes, "export.zip", "application/zip")
