"""
UI Module - Theme engine & reusable components for FED TTS.

Renders light/dark/auto themes entirely with injected CSS variables so it
works on any Streamlit version (no theme config reload required - the
palette swaps instantly at runtime). Dark mode follows the OS preference
automatically when theme == "auto".
"""

import json
from typing import Dict, List, Optional, Sequence, Tuple

from .settings import ACCENTS, Settings

# ---------------------------------------------------------------------
# Palettes
# ---------------------------------------------------------------------
# Each palette maps CSS variable -> (light value, dark value)

TOKENS: Dict[str, Tuple[str, str]] = {
    "bg":               ("#f6f7fb", "#0e1117"),
    "bg-panel":         ("#ffffff", "#161b26"),
    "bg-inset":         ("#eef1f7", "#1d2433"),
    "bg-code":          ("#f3f4f8", "#11151d"),
    "text":             ("#1f2430", "#e8eaf2"),
    "text-muted":       ("#5c6578", "#9aa3b8"),
    "border":           ("#dfe3ec", "#2a3242"),
    "accent":           ("#7c5cff", "#8f76ff"),   # default violet; overridden per-accent
    "accent-deep":      ("#5a3fd8", "#6a53e0"),
    "accent-soft":      ("#f0ecff", "#221a44"),
    "on-accent":        ("#ffffff", "#ffffff"),
    "success":          ("#0f9d58", "#2fbf71"),
    "warning":          ("#d97706", "#e3a008"),
    "danger":           ("#d13438", "#ff6b6b"),
}


def build_css(settings: Settings) -> str:
    """Generate the full <style> block for the current settings."""
    accent = ACCENTS.get(settings.accent, ACCENTS["violet"])
    theme = settings.theme
    radius = "14px" if settings.rounded else "4px"
    shadow = (
        "0 10px 30px rgba(15, 18, 30, 0.10)" if settings.rounded
        else "none"
    )
    radius_s = "9px" if settings.rounded else "3px"

    variables = []
    dark_variables = []
    for name, (light, dark) in TOKENS.items():
        variables.append(f"--fed-{name}:{light};")
        dark_variables.append(f"--fed-{name}:{dark};")

    # accent overrides
    variables.append(f"--fed-accent:{accent['base']};")
    variables.append(f"--fed-accent-deep:{accent['deep']};")
    variables.append(f"--fed-accent-soft:{accent['soft']};")
    dark_variables.append(f"--fed-accent:{accent['base']};")
    dark_variables.append(f"--fed-accent-deep:{accent['deep']};")
    dark_variables.append(f"--fed-accent-soft:{accent['soft_dark']};")

    font_family = "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif"
    mono_family = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"

    css = f"""
:root {{
    {"".join(variables)}
    --fed-radius: {radius};
    --fed-radius-s: {radius_s};
    --fed-shadow: {shadow};
    --fed-font: {font_family};
    --fed-font-mono: {mono_family};
    --fed-font-scale: {settings.font_scale};
}}

/* ---- global app background & font ---- */
.stApp {{
    background: var(--fed-bg);
    color: var(--fed-text);
    font-size: calc(15px * var(--fed-font-scale));
}}

/* Dark mode: variables get re-declared on .stApp by the theme blocks below */
.fed-theme, .fed-theme * {{
    color: var(--fed-text) !important;
    border-color: var(--fed-border) !important;
}}
"""

    # Apply dark palette to the whole app by re-declaring variables on
    # .stApp when the theme is dark (or auto+OS-dark). Simplest robust
    # approach: emit a <style> that targets html/body-level data attribute.
    if theme == "dark":
        css += f"""
.stApp {{
    {"".join(dark_variables)}
    color: var(--fed-text);
}}
"""
    elif theme == "auto":
        css += f"""
@media (prefers-color-scheme: dark) {{
    .stApp {{
        {"".join(dark_variables)}
        color: var(--fed-text);
    }}
}}
"""

    css += COMPONENT_CSS

    if settings.mono_editor:
        css += """
div[data-testid="stTextArea"] textarea, .stTextArea textarea {
    font-family: var(--fed-font-mono) !important;
}
"""
    return css


# ---------------------------------------------------------------------
# Component CSS (hero, cards, chips, ring, toggles) - theme aware via vars
# ---------------------------------------------------------------------
COMPONENT_CSS = """
/* ---------- Hero banner ---------- */
.fed-hero {
    position: relative;
    overflow: hidden;
    border-radius: var(--fed-radius);
    padding: 26px 30px;
    margin-bottom: 8px;
    background:
        radial-gradient(1200px 400px at -10% -50%, var(--fed-accent-soft), transparent 60%),
        linear-gradient(135deg, var(--fed-bg-panel), var(--fed-bg-inset));
    border: 1px solid var(--fed-border);
    box-shadow: var(--fed-shadow);
}
.fed-hero h1 {
    margin: 0 0 6px 0;
    font-size: calc(28px * var(--fed-font-scale));
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--fed-text);
    font-family: var(--fed-font);
}
.fed-hero p {
    margin: 0;
    color: var(--fed-text-muted);
    font-size: calc(14px * var(--fed-font-scale));
}
.fed-hero .fed-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 12px;
    border-radius: 999px;
    background: var(--fed-accent);
    color: var(--fed-on-accent);
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
}
.fed-hero .fed-pill.ghost {
    background: transparent;
    border: 1px solid var(--fed-border);
    color: var(--fed-text-muted);
}
.fed-hero .fed-badges { margin-top: 10px; }

/* ---------- Stat cards ---------- */
.fed-stats {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 10px 0 4px 0;
}
.fed-stat {
    flex: 1 1 120px;
    min-width: 110px;
    background: var(--fed-bg-panel);
    border: 1px solid var(--fed-border);
    border-radius: var(--fed-radius-s);
    padding: 12px 16px;
    box-shadow: var(--fed-shadow);
}
.fed-stat .v {
    font-size: calc(22px * var(--fed-font-scale));
    font-weight: 800;
    color: var(--fed-accent);
    font-family: var(--fed-font);
}
.fed-stat .k {
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--fed-text-muted);
    margin-top: 2px;
}

/* ---------- Chips ---------- */
.fed-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.fed-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    border: 1px solid var(--fed-border);
    background: var(--fed-bg-panel);
    color: var(--fed-text);
}
.fed-chip .dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--fed-success);
}
.fed-chip.warn .dot { background: var(--fed-warning); }
.fed-chip.off .dot  { background: var(--fed-danger); }

/* ---------- Grammar health ring ---------- */
.fed-ring-wrap {
    display: flex; align-items: center; gap: 18px;
    background: var(--fed-bg-panel);
    border: 1px solid var(--fed-border);
    border-radius: var(--fed-radius-s);
    padding: 16px;
    box-shadow: var(--fed-shadow);
}
.fed-ring {
    --p: 82;
    width: 96px; height: 96px; flex: 0 0 auto;
    border-radius: 50%;
    background:
        conic-gradient(var(--fed-accent) calc(var(--p)*1%), var(--fed-bg-inset) 0);
    display: flex; align-items: center; justify-content: center;
    mask: radial-gradient(farthest-side, transparent calc(100% - 14px), #000 calc(100% - 13.5px));
    -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 12px), #000 calc(100% - 11.5px));
}
.fed-ring .num {
    font-size: 24px; font-weight: 800; color: var(--fed-text);
    font-family: var(--fed-font);
}
.fed-ring-label { font-size: 12px; color: var(--fed-text-muted); margin-bottom: 8px; }

/* ---------- Segmented control (fake, CSS only) ---------- */
.fed-segment {
    display: inline-flex;
    border: 1px solid var(--fed-border);
    border-radius: 999px;
    overflow: hidden;
    background: var(--fed-bg-inset);
    padding: 2px;
}
.fed-segment span {
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    color: var(--fed-text-muted);
}
.fed-segment span.on {
    background: var(--fed-accent);
    color: var(--fed-on-accent);
    border-radius: 999px;
}

/* ---------- Panel / card container ---------- */
.fed-panel {
    background: var(--fed-bg-panel);
    border: 1px solid var(--fed-border);
    border-radius: var(--fed-radius);
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: var(--fed-shadow);
}

/* ---------- Find & replace preview ---------- */
.fed-diff { font-family: var(--fed-font-mono); font-size: 13px; }
.fed-diff del { color: var(--fed-danger); text-decoration-color: var(--fed-danger); }
.fed-diff ins { color: var(--fed-success); text-decoration: none; background: color-mix(in srgb, var(--fed-success) 18%, transparent); }

/* ---------- Subtitle table ---------- */
.fed-sub-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.fed-sub-table td { padding: 6px 10px; border-bottom: 1px solid var(--fed-border); }
.fed-sub-table td.t { color: var(--fed-accent); font-family: var(--fed-font-mono); white-space: nowrap; }
.fed-sub-table tr:last-child td { border-bottom: none; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--fed-bg-panel);
    border-right: 1px solid var(--fed-border);
}
[data-testid="stSidebar"] * { color: var(--fed-text); }

/* ---------- Streamlit widget theming ---------- */
.stButton > button, .stDownloadButton > button {
    border-radius: var(--fed-radius-s) !important;
    border: 1px solid var(--fed-accent-deep) !important;
    background: var(--fed-accent) !important;
    color: var(--fed-on-accent) !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.1rem !important;
    transition: all 0.18s ease;
    box-shadow: var(--fed-shadow);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: var(--fed-accent-deep) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="secondary"], .stDownloadButton > button[kind="secondary"] {
    background: var(--fed-bg-inset) !important;
    border: 1px solid var(--fed-border) !important;
    color: var(--fed-text) !important;
}
.stTextArea textarea {
    background: var(--fed-bg-panel) !important;
    color: var(--fed-text) !important;
    border: 1px solid var(--fed-border) !important;
    border-radius: var(--fed-radius-s) !important;
    font-size: calc(15px * var(--fed-font-scale)) !important;
    line-height: 1.65 !important;
    padding: 13px 15px !important;
    caret-color: var(--fed-accent);
}
.stTextArea textarea:focus {
    border-color: var(--fed-accent) !important;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--fed-accent) 25%, transparent) !important;
}
.fed-mono, .fed-mono textarea {
    font-family: var(--fed-font-mono) !important;
}
/* tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--fed-border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px 9px 0 0;
    padding: 8px 16px;
    color: var(--fed-text-muted);
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: var(--fed-accent-soft);
    color: var(--fed-accent) !important;
}
/* file uploader */
[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed var(--fed-border) !important;
    border-radius: var(--fed-radius) !important;
    background: var(--fed-bg-panel) !important;
    transition: border-color .2s ease, background .2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--fed-accent) !important;
    background: var(--fed-accent-soft) !important;
}
/* metrics & alerts */
[data-testid="stMetric"] {
    background: var(--fed-bg-panel);
    border: 1px solid var(--fed-border);
    border-radius: var(--fed-radius-s);
    padding: 8px 12px;
}
.stAlert, [data-testid="stAlert"] {
    border-radius: var(--fed-radius-s) !important;
}
/* checkbox / radio / slider */
.stCheckbox label, .stRadio label, [data-testid="stWidgetLabel"] p {
    color: var(--fed-text) !important;
}
[data-testid="stSliderThumbValue"], [data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input, [data-baseweb="input"] {
    color: var(--fed-text) !important;
}
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input {
    background: var(--fed-bg-panel) !important;
    border-color: var(--fed-border) !important;
}
[data-baseweb="select"] > div, [data-baseweb="select"] {
    background: var(--fed-bg-panel) !important;
    color: var(--fed-text) !important;
}
/* divider */
hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, transparent, var(--fed-accent), transparent);
    opacity: .35;
    margin: 18px 0;
}
/* scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb {
    background: var(--fed-border);
    border-radius: 8px;
}
::-webkit-scrollbar-thumb:hover { background: var(--fed-text-muted); }
"""


# ---------------------------------------------------------------------
# HTML components
# ---------------------------------------------------------------------
def hero(title: str, subtitle: str, pills: Optional[Sequence[str]] = None,
         ghost_pills: Optional[Sequence[str]] = None) -> str:
    """Return the hero banner HTML."""
    pills = pills or []
    ghost_pills = ghost_pills or []
    pill_html = "".join(
        f'<span class="fed-pill">{p}</span>' for p in pills
    )
    ghost_html = "".join(
        f'<span class="fed-pill ghost">{p}</span>' for p in ghost_pills
    )
    return f"""
<div class="fed-hero">
    <h1>{title}</h1>
    <p>{subtitle}</p>
    <div class="fed-badges">{pill_html}{ghost_html}</div>
</div>
"""


def stat_cards(stats: Sequence[Tuple[str, str]]) -> str:
    """stats: list of (value, label) tuples."""
    cells = "".join(
        f'<div class="fed-stat"><div class="v">{v}</div><div class="k">{k}</div></div>'
        for v, k in stats
    )
    return f'<div class="fed-stats">{cells}</div>'


def chips(items: Sequence[Tuple[str, bool]]) -> str:
    """items: list of (label, ok?) - True=green, None=amber, False=red."""
    parts = []
    for label, ok in items:
        cls = "" if ok else ("warn" if ok is None else "off")
        parts.append(f'<span class="fed-chip {cls}"><span class="dot"></span>{label}</span>')
    return f'<div class="fed-chips">{"".join(parts)}</div>'


def health_ring(score: int, label: str = "Grammar health") -> str:
    """score: 0-100."""
    score = max(0, min(100, int(score)))
    return f"""
<div class="fed-ring-wrap">
    <div class="fed-ring" style="--p:{score}">
        <span class="num">{score}</span>
    </div>
    <div>
        <div class="fed-ring-label">{label}</div>
        <div style="font-size:13px;color:var(--fed-text-muted)">
            90+ excellent &middot; 75-90 good &middot; below 75 needs polish
        </div>
    </div>
</div>
"""


def segment(active: str, options: Sequence[str]) -> str:
    """Static segmented control (visual only - real input via widgets)."""
    parts = []
    for o in options:
        cls = "on" if o == active else ""
        parts.append(f'<span class="{cls}">{o}</span>')
    return f'<div class="fed-segment">{"".join(parts)}</div>'


def subtitle_table(cues: Sequence[Tuple[str, str]]) -> str:
    """cues: list of (timestamp, text)."""
    rows = "".join(
        f'<tr><td class="t">{t}</td><td>{text}</td></tr>' for t, text in cues
    )
    return f'<table class="fed-sub-table">{rows}</table>'


def render(html: str) -> None:
    """Emit HTML via Streamlit (imported lazily to keep module testable)."""
    import streamlit as st
    st.markdown(html, unsafe_allow_html=True)
