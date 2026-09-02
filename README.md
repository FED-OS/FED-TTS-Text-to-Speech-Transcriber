<img width="1164" height="966" alt="Screenshot 2026-09-01 171028" src="https://github.com/user-attachments/assets/3cab76f9-e6ce-4330-a622-57d8807a65df" />

# 🎙️ FED TTS - Fluid Enhanced Dynamic Text Generator

**Generate text from the words in your uploaded files. 100% Offline. Zero AI.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![No AI](https://img.shields.io/badge/No%20AI-100%25%20Offline-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

FED TTS is a privacy-first, deterministic desktop application built with Python and Streamlit. You upload one or more **text files** (`.txt`, `.csv`, `.md`, `.docx`, `.log`, `.json`, `.xml`), and FED TTS extracts the words from them and **generates new text** built from — and inspired by — your own vocabulary. It then lets you polish that text with rule-based grammar checks and read it aloud using your operating system's native voices—all without sending a single byte to the cloud.

## ✨ Features

- 📂 **File Upload**: Supports `.txt`, `.csv`, `.md`, `.docx`, `.log`, `.json`, `.xml`
- 🔍 **Word Extraction**: Automatically reads the words out of every uploaded file
- ✨ **Text Generation (No AI)** — two deterministic modes:
  - **Markov Chain**: Learns which words follow which in your files, then walks the chain to produce text that mimics their style
  - **Random Word Pool**: Assembles sentences from your words using mad-libs–style templates
- 📊 **Word Analysis**: Total/unique word counts, frequency tables, and the full extracted vocabulary
- 🔍 **Grammarly Clone (No AI)**:
  - **Spell Check**: Dictionary-based (`pyspellchecker`)
  - **Grammar Rules**: Regex pattern matching for "would of", passive voice, long sentences, double spaces, and more
- 🔊 **Read Aloud (No AI)**: Uses the browser's built-in `SpeechSynthesis` API (Windows SAPI / macOS `say`)
- 💾 **Export**: Download generated text as a `.txt` file
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

1. **Upload Text Files**: Click the file uploader and select one or more `.txt`, `.csv`, `.md`, or `.docx` files. The words inside them become your vocabulary.
2. **Inspect the Words**: View the total/unique word counts, frequency table, and full extracted vocabulary.
3. **Generate Text**: Choose a mode (Markov Chain or Random Word Pool), set the length/order/seed, and click **Generate Text**.
4. **Polish**: Edit the generated text and click "Check Spelling & Grammar" to run the deterministic checker.
5. **Read Aloud**: Click "Speak" to hear the text via your OS's native voices.
6. **Export**: Download the generated text as a `.txt` file.

## 📦 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| Streamlit | 1.29+ | UI framework |
| pyspellchecker | 0.7+ | Dictionary-based spell checking |
| python-docx | 1.1+ | Reading `.docx` files (optional but recommended) |

## 🏗️ Architecture

```
FED TTS uses ZERO AI. Here's how the text-generation pipeline works deterministically:

Upload Text      Extract Words       Word Analysis
 Files    ──────▶  (.txt/.csv/.md  ──────▶  (freq + vocab)
(.txt/.docx…)      /.docx/…)

                                                       │
                                                       ▼
Read Aloud    ◀────  Grammar Check   ◀────  Generate Text
(Browser TTS)        (Regex + Dict)         (Markov / Pool)
```

### How generation works (no AI)

- **Markov Chain** (`MarkovChain`): Builds an N-gram transition table mapping each
  sequence of `order` words to the words that followed it in your files. New text
  is produced by walking this chain, picking each next word weighted by how often
  it appeared after the current context. This is pure statistics — no model
  training, no neural networks.
- **Random Word Pool** (`WordPoolGenerator`): Extracts every unique word,
  loosely buckets them by simple suffix heuristics (nouns/verbs/adjectives/
  adverbs), and fills sentence templates with random picks from those buckets.

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
