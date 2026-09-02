# 📋 FED TTS - Executive Summary

## What is FED TTS?

FED TTS (Fluid Enhanced Dynamic Text Generator) is a 100% offline, privacy-first application that **generates new text from the words in your uploaded files**. You upload one or more text files (.txt, .csv, .md, .docx), and FED TTS extracts their words and produces fresh text built from your vocabulary — using a Markov chain that mimics your files' style or a random word-pool generator. You can then check spelling and grammar, and read the result aloud—all without using any AI/ML APIs.

## Key Features

| Feature | Description |
|---------|-------------|
| 📂 File Upload | Supports .txt, .csv, .md, .docx, .log, .json, .xml |
| 🔍 Word Extraction | Automatically reads the words out of every uploaded file |
| ✨ Markov Generation | Learns word transitions and mimics the style of your files |
| 🎲 Random Pool Generation | Mad-libs–style sentences from your vocabulary |
| 📊 Word Analysis | Frequency tables, total/unique counts, full vocabulary |
| 🔍 Grammar Check | Dictionary-based spelling + regex grammar rules |
| 🔊 Read Aloud | Native browser TTS (no cloud calls) |
| 💾 Export | Download generated text as .txt |
| 🔒 Privacy | 100% offline, no data leaves your machine |
| 💯 No AI | Deterministic algorithms only, no neural networks |

## Architecture

- **UI:** Streamlit (Python)
- **Word Extraction:** python-docx + stdlib csv/decode (.txt, .csv, .md, .docx, …)
- **Text Generation:** Markov chain (N-gram) + word-pool templates (deterministic)
- **Spell Check:** pyspellchecker (dictionary-based)
- **Grammar:** Regex rules (deterministic)
- **TTS:** Web SpeechSynthesis API (native browser)
- **Storage:** Session state (in-memory, local)

## Why "No AI"?

1. **Privacy** – No data sent to cloud services
2. **Cost** – No API fees or subscriptions
3. **Control** – 100% predictable behavior
4. **Simplicity** – No model downloads or complex dependencies
5. **Offline** – Works without internet (except browser for Streamlit)

## Target Users

- **Students** – Lecture transcription and textbook reading
- **Journalists** – Interview transcription with full privacy
- **Researchers** – Academic paper reading and transcription
- **Writers** – Audio-assisted proofreading
- **Privacy-conscious professionals** – Lawyers, doctors, therapists
- **Accessibility users** – Dyslexic users, visually impaired users

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python 3.8+ | Widely used, easy to maintain |
| UI Framework | Streamlit 1.29+ | Rapid development, Python-native |
| Text Generation | Markov chain + word pool | Deterministic, no AI |
| File Reading | python-docx + stdlib | Reads .txt/.csv/.md/.docx |
| Spell Check | pyspellchecker | Dictionary-based, no AI |
| Grammar | Regex | Deterministic, transparent |
| TTS | Browser SpeechSynthesis | OS-native, no cloud |
| Testing | pytest | Standard Python testing |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Container | Docker | Easy deployment |

## Roadmap Highlights

- **v0.1.0** (Current): Core features - upload, transcribe, check, read
- **v0.2.0**: Custom audio player, keyboard shortcuts, export
- **v0.3.0**: More grammar rules, batch processing, waveform
- **v0.4.0**: Plugin system, custom themes, multi-monitor
- **v1.0.0**: Desktop executable, full test coverage, i18n

## Links

- [GitHub Repository](https://github.com/your-github-username/fed-tts)
- [Documentation](docs/)
- [Installation Guide](INSTALL.md)
- [Buy Me a Coffee](https://ko-fi.com/YOUR_USERNAME)

## License

FED TTS is released under the MIT License, making it free for both personal and commercial use.
