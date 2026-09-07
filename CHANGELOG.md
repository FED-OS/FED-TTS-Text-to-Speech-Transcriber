# Changelog

All notable changes to FED TTS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Custom HTML5 audio player with rewind/forward buttons
- Keyboard shortcuts for transcription (Ctrl+Space, Ctrl+Left/Right)
- Auto-save transcripts to local storage
- Batch file processing
- Audio waveform visualization
- Desktop executable (PyInstaller)
- Support for more grammar rules (20+)
- Internationalization (multiple languages)
- Plugin system for custom grammar rules

## [0.3.0] - 2026-01-16

### Added
- 🎨 **Dark mode & full theming system**: Dark / Light / Auto (follows your OS via `prefers-color-scheme`) themes, applied live with no restart. Five accent colours (blue, violet, emerald, rose, amber), adjustable interface font size (85–125%), rounded-corners toggle, and a monospace editor toggle
- 💾 **Persistent settings**: appearance and transcription preferences (timestamps, interval, read-aloud speed/pitch, history) are saved to a local JSON file (`~/.config/.fed-tts/settings.json`) with strict validation—corrupt files can never break the app
- 🎬 **Subtitle export**: burn-in ready **SRT** and **WebVTT** files generated from word-level timings, plus a plain-text transcript download; adjustable cue length (2–30 s) with a live cue preview table
- 🧰 **Transcript tools tab**: Find & Replace (plain or regex, optional case-sensitivity), one-click case conversion (UPPERCASE / lowercase / Sentence case), extra-space cleanup, and a session transcript history (up to 25 snapshots) with restore
- 📊 **Live stat cards & grammar health score**: words, characters, auto-transcript words, and estimated speaking time update as you work; the grammar check now shows a 0–100 health ring (90+ excellent, 75–90 good, below 75 needs polish)
- 🖥️ **Visual overhaul**: hero banner with feature pills, status chips (Vosk model ready / ffmpeg detected), tabbed workspace (🤖 Auto Transcribe / ✍️ Manual / 🎬 Subtitles / 🧰 Tools), and a restyled sidebar

### Fixed
- 🐛 Find & Replace and the Manual-tab copy button no longer raise `StreamlitWidgetAlreadyInstantiatedError` when updating the transcript after those widgets were instantiated—transcript updates are now applied via a deferred-write pattern at the top of the next run

### Changed
- 🎨 The default theme is now **dark** (previously the plain Streamlit light theme)

## [0.2.0] - 2026-01-15

### Fixed
- 🐛 **Uploading MP4 files no longer fails**: the file uploader previously rejected every video container, so MP4 uploads (and their transcription) could never work
- 🐛 Transcript display now updates reliably after automatic transcription (widget session-state sync)

### Added
- 🤖 **Automatic transcription (offline)**: new "🤖 Auto Transcribe" tab with one-click speech-to-text powered by the Vosk engine—runs 100% locally, no cloud APIs, no API keys
- 📂 Video file support: MP4, MOV, MKV, WEBM, AVI, MPG/MPEG, WMV, 3GP, M4V (audio extracted via ffmpeg to 16 kHz mono WAV)
- 📂 Extended audio support: AAC, OPUS, WMA, AIFF (in addition to MP3, WAV, M4A, FLAC, OGG)
- ⏱️ Optional `[mm:ss]` timestamps in auto transcripts
- 📝 Editable auto-transcript panel with sync-back into the manual workspace
- 💾 Download transcript as `.txt`
- 🎥 Video playback for uploaded video files
- ⚙️ Sidebar "Transcription engine" status panel (model availability, ffmpeg detection)
- 🧪 New test suite for the auto transcriber (35 tests total, all passing)

### Changed
- `requirements.txt` now includes `vosk>=0.3.45`
- README, usage guide, and architecture diagram updated to document the offline transcription pipeline
- File uploader label changed to "Upload Audio or Video File"

## [0.1.0] - 2026-01-01

### Added
- 🎉 Initial release of FED TTS
- File upload support for MP3, WAV, M4A, FLAC, OGG
- Native audio player with playback controls
- Manual transcription text area with session state persistence
- Dictionary-based spell checking using pyspellchecker
- Regex-based grammar rules:
  - "would of" → "would have"
  - "could of" → "could have"
  - "should of" → "should have"
  - "must of" → "must have"
  - Double space detection
  - Passive voice detection
  - Long sentence detection (>25 words)
  - Repeated word detection
  - Capitalization at sentence start
- Read aloud using browser's native SpeechSynthesis API
- Stop speech button
- Custom CSS styling
- Word and character count in sidebar
- Ko-fi support button
- Comprehensive documentation:
  - README.md
  - CONTRIBUTING.md
  - CODE_OF_CONDUCT.md
  - SECURITY.md
  - INSTALL.md
  - BUILD.md
  - DEPLOYMENT.md
  - FAQ.md
  - ROADMAP.md
  - ADR.md
  - GOVERNANCE.md
  - CITATIONS.md
  - COPYING.md
  - PRICING.md
  - SUPPORT.md
  - NOTICE.md
- GitHub Actions workflows (16 total)
- Issue templates (bug report, feature request, custom)
- Pull request template
- Dependabot configuration
- Pre-commit hooks (black, flake8, isort)
- Docker support
- Test suite with pytest
- pyproject.toml for modern Python packaging

### Security
- 100% offline operation
- No data collection or telemetry
- No cloud API calls
