# 🎙️ FED TTS - Fluid Enhanced Dynamic Text-to-Speech

**Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Privacy-first.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![Offline](https://img.shields.io/badge/No%20Cloud-100%25%20Offline-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

FED TTS is a privacy-first desktop application built with Python and Streamlit. It automatically transcribes audio **and video** files (including MP4) using offline speech recognition, offers a professional manual transcription workspace, polishes text with rule-based grammar checks, and reads text aloud using your operating system's native voices—all without sending a single byte to the cloud.

## ✨ Features

- 📂 **File Upload**: Supports MP3, WAV, M4A, FLAC, OGG, AAC, OPUS, and video files: **MP4**, MOV, MKV, WEBM, AVI, MPG, WMV, 3GP
- 🤖 **Auto Transcribe (Offline)**: One-click speech-to-text for any audio/video file using the Vosk engine—runs 100% locally on your machine (first use downloads a ~40 MB English model from alphacephei.com; no audio or text ever leaves your computer)
- ⏱️ **Optional Timestamps**: Insert `[mm:ss]` markers into the auto transcript for easy navigation
- 🎬 **Subtitle Export**: Download burn-in ready **SRT**, **WebVTT**, and plain-text transcripts generated from word-level timings; adjustable cue length (2–30 s)
- 🎨 **Dark Mode & Theming**: Dark / Light / Auto (follows your OS) themes, five accent colours (blue, violet, emerald, rose, amber), adjustable font size (85–125%), rounded corners toggle, and monospace editor toggle—all rendered live without a restart
- 🧰 **Transcript Tools**: Find & Replace (with regex + case options), case conversion (UPPERCASE/lowercase/Sentence case), space cleanup, and a session transcript history with one-click restore
- 📊 **Live Stats & Health Score**: Words, characters, auto-transcript words, and estimated speaking time update as you work; the grammar check shows a 0–100 health ring
- 🎧 **Audio/Video Playback**: Native players with speed control
- ✍️ **Manual Transcriber**: Professional text area with session persistence—perfect for polishing the auto transcript
- 🔍 **Grammarly Clone (No AI)**:
  - **Spell Check**: Dictionary-based (`pyspellchecker`)
  - **Grammar Rules**: Regex pattern matching for "would of", passive voice, long sentences, double spaces, and more
- 🔊 **Read Aloud (No AI)**: Uses the browser's built-in `SpeechSynthesis` API (Windows SAPI / macOS `say`), with adjustable speed and pitch
- 🔒 **100% Private**: Everything runs locally. No data leaves your machine
- ⚙️ **Persistent Settings**: Appearance and transcription preferences are saved to a local JSON file (`~/.config/.fed-tts/settings.json`) and restored on every launch—no accounts, no cloud

> ℹ️ **Note on "Zero AI"**: The original FED TTS philosophy was strictly rule-based. Offline speech-to-text is technically pattern-matching acoustic models (Vosk/Kaldi), not a cloud service or LLM—so your privacy is intact. If you prefer, the manual transcription workspace is still fully available in the ✍️ Manual tab.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-github-username/fed-tts.git
cd fed-tts
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📖 How to Use

1. **Pick your look** *(optional)*: In the sidebar's 🎨 Appearance panel, choose a theme (Dark / Light / Auto), an accent colour, font size, and editor style, then click "💾 Save appearance" to remember them across sessions
2. **Upload an Audio or Video File**: Click the file uploader and select an MP4, MOV, MP3, WAV, or any other supported file
3. **Auto Transcribe**: Go to the "🤖 Auto Transcribe" tab and click "🤖 Transcribe Automatically"—the offline Vosk engine converts speech to text with a live progress bar (optionally with `[mm:ss]` timestamps)
4. **Export Subtitles**: In the "🎬 Subtitles" tab, review the cue table, adjust cue length, and download **SRT**, **VTT**, or **TXT** files
5. **Polish the Text**: The "🧰 Tools" tab offers Find & Replace (regex + case options), case conversion, space cleanup, and a session history with one-click restore
6. **Or Transcribe Manually**: Switch to the "✍️ Manual" tab, play the media, and type what you hear
7. **Check Grammar**: Click "Check Spelling & Grammar" to run the deterministic checker and see your 0–100 grammar health score
8. **Read Aloud**: Enter text, adjust speed/pitch, and click "Speak Now" to hear it via your OS's native voices

## 📦 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| Streamlit | 1.29+ | UI framework |
| vosk | 0.3.45+ | Offline speech recognition (auto transcription) |
| pyspellchecker | 0.7+ | Dictionary-based spell checking |
| ffmpeg | any | Audio extraction from video containers (MP4, MOV, MKV, ...) |

> ⚠️ **ffmpeg is required** for video files. Install it with `sudo apt-get install ffmpeg` (Debian/Ubuntu), `brew install ffmpeg` (macOS), or `winget install ffmpeg` (Windows).

## 🏗️ Architecture

```
FED TTS runs entirely on your machine. Here's how each feature works:

┌───────────────┐     ┌───────────────────┐     ┌────────────────┐
│  File Upload  │────▶│ Audio Extraction  │────▶│ Auto Transcribe│
│ (st.file_up-  │     │ (ffmpeg → 16 kHz  │     │ (Vosk offline  │
│   loader)     │     │  mono WAV)        │     │  speech engine)│
└───────┬───────┘     └───────────────────┘     └───────┬────────┘
        │                                             │
        ▼                                             ▼
┌───────────────┐     ┌───────────────┐     ┌────────────────┐
│ Media Playback│     │ Manual Type   │     │ Transcript Box │
│ (st.audio /   │     │ (st.text_area)│     │ + Download     │
│  st.video)    │     │               │     │ (editable)     │
└───────┬───────┘     └───────┬───────┘     └───────┬────────┘
        └─────────────────────┴─────────────────────┤
                                                    ▼
                              ┌──────────────────────────────┐
                              │ Grammar Check (Regex + Dict) │
                              │ ⇄ Read Aloud (Browser TTS)   │
                              └──────────────────────────────┘
```

## 🤝 Contributing

### Project Structure (v0.3.0)

```
fed-tts/
├── app.py                      # Streamlit UI (tabs, tools, theming hooks)
├── requirements.txt
├── src/fed_tts/
│   ├── auto_transcriber.py     # Vosk engine + SRT/VTT subtitle export
│   ├── grammar_checker.py      # Regex + dictionary checks
│   ├── settings.py             # Persistent JSON settings (theme, accents…)
│   ├── ui.py                   # Theme engine: CSS vars, hero, cards, ring
│   └── webapp_utils.py
└── tests/                      # 63 passing tests (subtitles, settings, UI)
```

Settings are stored at `~/.config/.fed-tts/settings.json` (override with the `FED_TTS_SETTINGS_DIR` environment variable). Corrupt or partial files are safely ignored—worst case, defaults are restored.

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## 🔗 Links

- [Documentation](docs/)
- [Installation Guide](INSTALL.md)
- [Usage Guide](usage.md)
- [FAQ](FAQ.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

## 💖 Support the Project

If you find FED TTS useful, consider buying me a coffee!

<a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
    <img height='36' style='border:0px;height:36px;' src='https://ko-fi.com/img/githubbutton_sm.svg' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a>

## 🌟 Star History

If you like this project, please give it a ⭐ on GitHub!

---

**FED TTS** — Built with ❤️ for privacy-first applications. No AI. No cloud. Just you and your data.
