# Frequently Asked Questions (FAQ)

## General

### What does "FED TTS" stand for?
FED stands for **Fluid Enhanced Dynamic** Text-to-Speech. It represents our commitment to a smooth, enhanced, and dynamic user experience for transcription and text-to-speech.

### What makes FED TTS different from other transcription tools?
FED TTS is **100% AI-free and offline**. Unlike tools like Otter.ai, Whisper, or AssemblyAI that use cloud-based AI models, FED TTS uses:
- **Manual transcription** (you type what you hear)
- **Dictionary-based spell checking** (pyspellchecker)
- **Regex-based grammar rules** (deterministic patterns)
- **Browser's native TTS** (operating system voices)

This means complete privacy, zero ongoing costs, and no dependency on cloud services.

### Is FED TTS really 100% offline?
Yes! The only "internet" requirement is that you need a browser to run Streamlit. The TTS feature uses your operating system's built-in voices (Windows SAPI, macOS `say`, Linux speech-dispatcher). No data is ever sent to any server.

## Installation

### Do I need to install ffmpeg?
For basic file upload and playback, ffmpeg is not strictly required as Streamlit can handle most common formats. However, for broader audio format support, installing ffmpeg is recommended:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### Which Python version do I need?
FED TTS requires Python 3.8 or later. We test against Python 3.8, 3.9, 3.10, and 3.11.

### How do I create a virtual environment?

```bash
# Create
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

## Usage

### How do I transcribe audio?
1. Upload your audio file (MP3, WAV, M4A, FLAC, or OGG)
2. Press play on the audio player
3. Type what you hear in the text area
4. Use right-click on the player for speed control to slow down difficult sections
5. Click "Check Spelling & Grammar" when done

### How does the grammar checker work?
The grammar checker uses two deterministic methods:
1. **Spell Check**: Uses `pyspellchecker`, which compares words against a built-in dictionary. No AI involved.
2. **Grammar Rules**: Uses regular expressions (regex) to find common mistakes like "would of" (should be "would have"), double spaces, passive voice patterns, and overly long sentences.

### The Read Aloud feature doesn't work. Why?
The Read Aloud feature uses your browser's `SpeechSynthesis` API, which relies on your operating system's installed voices. Make sure:
1. You're using a modern browser (Chrome, Firefox, Edge, Safari)
2. Your system volume is turned up
3. Your OS has TTS voices installed (most do by default)

### Can I use FED TTS without uploading an audio file?
Yes! You can type or paste any text directly into the text area and use the grammar checker and read-aloud features without uploading a file.

## Privacy

### Does FED TTS collect any data?
**No.** FED TTS does not collect, store, or transmit any user data. Everything runs on your local machine. There is no telemetry, no analytics, and no cloud calls.

### Are my audio files uploaded anywhere?
No. When you upload an audio file, it is read into your browser's memory locally. It is never sent to any server.

### Can I use FED TTS for sensitive/confidential audio?
Yes! FED TTS is ideal for sensitive audio (medical, legal, confidential interviews) because no data ever leaves your machine.

## Technical

### Can I add my own grammar rules?
Yes! The grammar rules are defined in `src/fed_tts/grammar_checker.py` in the `grammar_rules` list. Each rule is a dictionary with a regex pattern, a message, and flags. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Can I use a different TTS engine?
FED TTS uses the browser's native SpeechSynthesis API by design (no AI, no cloud). If you want to use a different TTS engine, you would need to modify `src/fed_tts/tts.py`. Note that using cloud-based TTS would violate the "No AI" principle.

### How do I run tests?

```bash
pytest tests/
```

### How do I build a standalone executable?

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "FED TTS" app.py
```

## Support

### How do I get help?
1. Check this FAQ
2. Read the [Documentation](docs/)
3. Search [GitHub Issues](https://github.com/your-github-username/fed-tts/issues)
4. Start a [GitHub Discussion](https://github.com/your-github-username/fed-tts/discussions)

### How do I report a bug?
Open a [bug report issue](https://github.com/your-github-username/fed-tts/issues/new/choose) and fill out the template completely.

### How can I support the project?
- ⭐ Star the repository on GitHub
- ☕ [Buy me a coffee](https://ko-fi.com/YOUR_USERNAME)
- 🐛 Report bugs and suggest features
- 📝 Contribute code or documentation
- 📢 Share FED TTS with others
