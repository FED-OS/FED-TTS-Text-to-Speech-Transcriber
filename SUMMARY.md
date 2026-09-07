# 📋 FED TTS - Executive Summary

## What is FED TTS?

FED TTS (Fluid Enhanced Dynamic Text-to-Speech) is a 100% offline, privacy-first transcription and text-to-speech application. It allows users to upload audio files, manually transcribe them, check spelling and grammar, and read text aloud—all without using any AI/ML APIs.

## Key Features

| Feature | Description |
|---------|-------------|
| 📂 File Upload | Supports MP3, WAV, M4A, FLAC, OGG |
| 🎧 Audio Playback | Native player with speed controls |
| ✍️ Manual Transcription | Professional text area with session persistence |
| 🔍 Grammar Check | Dictionary-based spelling + regex grammar rules |
| 🔊 Read Aloud | Native browser TTS (no cloud calls) |
| 🔒 Privacy | 100% offline, no data leaves your machine |
| 💯 No AI | Deterministic algorithms only, no neural networks |

## Architecture

- **UI:** Streamlit (Python)
- **Spell Check:** pyspellchecker (dictionary-based)
- **Grammar:** Regex rules (deterministic)
- **TTS:** Web SpeechSynthesis API (native browser)
- **Audio:** HTML5 audio with native controls
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
