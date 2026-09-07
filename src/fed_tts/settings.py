"""
Settings Module - Persistent user preferences for FED TTS.

Settings are stored as plain JSON in a local file (default:
~/.config/fed-tts/settings.json) so they survive restarts. Everything
stays on the user's machine - no cloud, no accounts, no telemetry.
"""

import json
import os
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Dict, Optional

APP_DIR = ".fed-tts"


def default_settings_path() -> str:
    """Return the path of the settings JSON file."""
    base = os.environ.get("FED_TTS_SETTINGS_DIR")
    if not base:
        base = os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, APP_DIR, "settings.json")


@dataclass
class Settings:
    """User-adjustable settings with safe defaults."""

    # Appearance
    theme: str = "dark"            # "light" | "dark" | "auto" (follow OS)
    accent: str = "violet"         # blue | violet | emerald | rose | amber
    font_scale: float = 1.0        # 0.85 .. 1.25 global font size multiplier
    mono_editor: bool = True       # monospace font in transcript editors
    rounded: bool = True           # rounded corners / soft shadows

    # Transcription
    timestamps: bool = False       # include [mm:ss] markers by default
    timestamp_interval: float = 8.0  # seconds between markers / subtitle cues
    model_name: str = "vosk-model-small-en-us-0.15"

    # Read Aloud
    tts_rate: float = 1.0          # 0.5 .. 1.75
    tts_pitch: float = 1.0         # 0.5 .. 1.75

    # Behaviour
    history_enabled: bool = True   # keep transcript snapshots in session

    def __post_init__(self) -> None:
        self.validate()

    # ---- validation & clamping -------------------------------------
    def validate(self) -> None:
        """Clamp values into safe ranges so bad JSON can't break the app."""
        if self.theme not in {"light", "dark", "auto"}:
            self.theme = "dark"
        if self.accent not in ACCENTS:
            self.accent = "violet"
        self.font_scale = _clamp(self.font_scale, 0.85, 1.25, 1.0)
        self.timestamp_interval = _clamp(self.timestamp_interval, 2.0, 30.0, 8.0)
        self.tts_rate = _clamp(self.tts_rate, 0.5, 1.75, 1.0)
        self.tts_pitch = _clamp(self.tts_pitch, 0.5, 1.75, 1.0)

    # ---- persistence ------------------------------------------------
    def save(self, path: Optional[str] = None) -> str:
        """Write the settings to disk. Returns the path used."""
        path = path or default_settings_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)
        return path

    @classmethod
    def load(cls, path: Optional[str] = None) -> "Settings":
        """Load settings from disk, falling back to defaults."""
        path = path or default_settings_path()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return cls()
        if not isinstance(data, dict):
            return cls()
        # Only accept known keys, ignore anything else in the file
        known = {f.name for f in fields(cls)}
        clean = {k: v for k, v in data.items() if k in known}
        try:
            return cls(**clean)
        except TypeError:
            return cls()

    def reset(self, path: Optional[str] = None) -> None:
        """Restore defaults and save them."""
        fresh = Settings()
        for f in fields(self):
            setattr(self, f.name, getattr(fresh, f.name))
        self.save(path)


def _clamp(value: Any, lo: float, hi: float, default: float) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return default
    if value < lo or value > hi:
        return min(max(value, lo), hi)
    return value


ACCENTS: Dict[str, Dict[str, str]] = {
    # name: {base, dark-variant, soft-bg (light), soft-bg (dark), text-on-accent}
    "blue":    {"base": "#4a6fa5", "deep": "#2f4858", "soft": "#eaf1fb", "soft_dark": "#1b2a41", "on": "#ffffff"},
    "violet":  {"base": "#7c5cff", "deep": "#5a3fd8", "soft": "#f0ecff", "soft_dark": "#221a44", "on": "#ffffff"},
    "emerald": {"base": "#10b981", "deep": "#0b7d5c", "soft": "#e7f8f1", "soft_dark": "#12352a", "on": "#ffffff"},
    "rose":    {"base": "#e5487f", "deep": "#b83562", "soft": "#fdeaf2", "soft_dark": "#3d1a2a", "on": "#ffffff"},
    "amber":   {"base": "#d97706", "deep": "#a35a05", "soft": "#fdf2e3", "soft_dark": "#38270f", "on": "#ffffff"},
}
