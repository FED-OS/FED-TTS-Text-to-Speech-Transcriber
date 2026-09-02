<img width="1536" height="1024" alt="generated_image_6a4557de-fc86-4e6c-9ca0-1ce0c8397c75_0" src="https://github.com/user-attachments/assets/3cd535fa-a5df-4711-aaf8-c6add1fc3651" />

# 🎙️ FED TTS - Fluid Enhanced Dynamic Text-to-Speech

**Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Zero AI.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![No AI](https://img.shields.io/badge/No%20AI-100%25%20Offline-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

FED TTS is a privacy-first, deterministic desktop application built with Python and Streamlit. It provides a professional workspace to manually transcribe audio, polish text with rule-based grammar checks, and read text aloud using your operating system's native voices—all without sending a single byte to the cloud.

## ✨ Features

- 📂 **File Upload**: Supports MP3, WAV, M4A, FLAC, and OGG
- 🎧 **Audio Playback**: Native player with speed control
- ✍️ **Manual Transcriber**: Professional text area with session persistence
- 🔍 **Grammarly Clone (No AI)**:
  - **Spell Check**: Dictionary-based (`pyspellchecker`)
  - **Grammar Rules**: Regex pattern matching for "would of", passive voice, long sentences, double spaces, and more
- 🔊 **Read Aloud (No AI)**: Uses the browser's built-in `SpeechSynthesis` API (Windows SAPI / macOS `say`)
- 🔒 **100% Private**: Everything runs locally. No data leaves your machine
- 💯 **Zero AI**: No neural networks, no LLMs, no cloud APIs—just deterministic algorithms

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

1. **Upload an Audio File**: Click the file uploader and select an MP3, WAV, M4A, FLAC, or OGG file
2. **Play the Audio**: Use the built-in audio player (right-click for speed controls)
3. **Transcribe Manually**: Type what you hear in the text area on the right
4. **Check Grammar**: Click "Check Spelling & Grammar" to run the deterministic checker
5. **Read Aloud**: Enter text and click "Speak Now" to hear it via your OS's native voices

## 📦 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| Streamlit | 1.29+ | UI framework |
| pyspellchecker | 0.7+ | Dictionary-based spell checking |

## 🏗️ Architecture

```
FED TTS uses ZERO AI. Here's how each feature works deterministically:

┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  File Upload    │────▶│  Audio Playback   │────▶│  Manual Type    │
│  (st.file_up    │     │  (st.audio)       │     │  (st.text_area) │
│   loader)       │     │                   │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Read Aloud     │◀────│  Grammar Check    │◀────│  Text Input     │
│  (Browser TTS)  │     │  (Regex + Dict)   │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 🤝 Contributing

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
