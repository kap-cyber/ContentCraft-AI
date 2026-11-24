"""Shared, presentation-only UI helpers for ContentCraft AI.

Nothing in this module touches generation logic, prompts or session state
used by the generators: it only renders HTML/CSS and Streamlit layout.
"""

import base64
from html import escape
from pathlib import Path

import streamlit as st

APP_NAME = "ContentCraft AI"
TAGLINE = "Create smarter. Write faster."

_CSS_PATH = Path(__file__).with_name("styles.css")
_DARK_CSS_PATH = Path(__file__).with_name("theme_dark.css")

# Minimal stroke icons (24x24 viewBox) used inside custom HTML blocks.
_ICON_PATHS = {
    "logo": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>'
            '<path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "blog": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'
            '<path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h4"/>',
    "social": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>'
              '<path d="M9 12h.01"/><path d="M12 12h.01"/><path d="M15 12h.01"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/>'
             '<path d="m3 7 9 6 9-6"/>',
    "spark": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'
           '<path d="M14 3v5h5"/>',
}


def icon_svg(name: str, size: int = 20, color: str = "#4F46E5") -> str:
    """Return an <img> tag holding an inline SVG icon.

    st.html sanitizes raw <svg> markup, so icons are embedded as data URIs.
    """
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round">{_ICON_PATHS[name]}</svg>'
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (
        f'<img src="data:image/svg+xml;base64,{encoded}" width="{size}" '
        f'height="{size}" alt="" style="display:block">'
    )


def text_to_html(text) -> str:
    """Escape model output for safe HTML display, keeping line breaks."""
    return escape(str(text or "")).replace("\n", "<br>")


def init_theme() -> str:
    """Return the active theme ("light" or "dark"), defaulting to light."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    return st.session_state.theme


def load_css(theme: str = "light") -> None:
    css = _CSS_PATH.read_text(encoding="utf-8")
    if theme == "dark":
        css += _DARK_CSS_PATH.read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


def _sync_theme() -> None:
    st.session_state.theme = "dark" if st.session_state.theme_toggle else "light"


def theme_toggle() -> None:
    """Sidebar switch bound to st.session_state.theme."""
    # Keep the widget in sync with the stored theme (survives page switches).
    st.session_state.theme_toggle = st.session_state.theme == "dark"
    st.toggle(
        ":material/dark_mode: Dark mode",
        key="theme_toggle",
        on_change=_sync_theme,
    )


def sidebar_brand() -> None:
    st.html(
        f"""
        <div class="cc-brand">
          <div class="cc-brand-mark">{icon_svg("logo", 20, "#FFFFFF")}</div>
          <div>
            <div class="cc-brand-name">{APP_NAME}</div>
            <div class="cc-brand-tagline">{TAGLINE}</div>
          </div>
        </div>
        """
    )


def sidebar_label(text: str) -> None:
    st.html(f'<div class="cc-nav-label">{escape(text)}</div>')


def page_header(title: str, subtitle: str, icon: str, eyebrow: str = "") -> None:
    eyebrow_html = f'<div class="cc-eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    st.html(
        f"""
        <div class="cc-page-header">
          <div class="cc-page-icon">{icon_svg(icon, 22)}</div>
          <div>
            {eyebrow_html}
            <h1 class="cc-page-title">{escape(title)}</h1>
            <p class="cc-page-subtitle">{escape(subtitle)}</p>
          </div>
        </div>
        """
    )


def section_title(title: str, caption: str = "") -> None:
    caption_html = f'<div class="cc-section-caption">{escape(caption)}</div>' if caption else ""
    st.html(
        f'<div class="cc-section-title">{escape(title)}</div>{caption_html}'
    )


def empty_state(target, title: str, message: str, icon: str = "spark") -> None:
    """Render an empty-state panel into `target` (a container or placeholder)."""
    target.html(
        f"""
        <div class="cc-empty">
          <div class="cc-empty-icon">{icon_svg(icon, 26)}</div>
          <div class="cc-empty-title">{escape(title)}</div>
          <div class="cc-empty-text">{escape(message)}</div>
        </div>
        """
    )
