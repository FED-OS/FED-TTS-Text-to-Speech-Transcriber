# Changelog

All notable changes to FED TTS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ✨ **Text generation from uploaded files** (new core feature): upload `.txt`, `.csv`, `.md`, `.docx`, `.log`, `.json`, `.xml` files and generate new text built from their words.
- Markov chain generator that mimics the style of the source files (N-gram transitions).
- Random word-pool / mad-libs generator that assembles sentences from the extracted vocabulary.
- Word frequency analysis, total/unique word counts, and full vocabulary display.
- Generation controls: mode, max words, Markov order, starting seed word, and reproducible random seed.
- Download generated text as `.txt`.
- `python-docx` dependency for `.docx` file support.

### Changed
- Refocused the app from manual audio transcription to text generation from uploaded text files.
- Updated README, SUMMARY, AGENTS docs, and architecture diagram to reflect the new pipeline.

### Planned
- Keyboard shortcuts for playback (Ctrl+Space, Ctrl+Left/Right)
- Export generated text as PDF
- Dark mode theme
- Batch file processing
- Audio waveform visualization
- Desktop executable (PyInstaller)
- Support for more grammar rules (20+)
- Internationalization (multiple languages)
- Plugin system for custom grammar rules

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
