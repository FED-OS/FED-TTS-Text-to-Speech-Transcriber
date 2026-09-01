# Claude AI Instructions for FED TTS

## Project Overview

FED TTS is a 100% offline, privacy-first text-to-speech and transcription tool built with Python and Streamlit. It features a "No AI" approach, using deterministic methods instead of neural networks.

## Key Principles (NON-NEGOTIABLE)

1. **No AI/ML** – Use ONLY deterministic algorithms (regex, dictionary lookups, formant synthesis, native browser TTS)
2. **Privacy First** – No data leaves the user's machine. No cloud calls. No telemetry.
3. **Simplicity** – Keep the codebase clean and well-documented
4. **Open Source** – MIT licensed

## Tech Stack

- Python 3.8+
- Streamlit 1.29+
- pyspellchecker (dictionary-based spelling)
- Browser's native SpeechSynthesis API (for TTS)

## Project Structure

```
fed-tts/
├── app.py              # Main Streamlit application
├── src/fed_tts/        # Core logic modules
│   ├── grammar_checker.py
│   ├── transcriber.py
│   └── tts.py
├── tests/              # Unit tests
├── docs/               # Documentation
├── styles.css          # Custom Streamlit theming
└── .github/            # CI/CD and templates
```

## Common Tasks

### Adding a New Grammar Rule
Update the `grammar_rules` list in `src/fed_tts/grammar_checker.py`:
```python
{
    "pattern": r"\byour_pattern\b",
    "message": "Description of the issue",
    "flags": re.IGNORECASE,
}
```

### Adding a New Audio Format
Update the `type` parameter in `app.py`:
```python
st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a", "flac", "ogg", "new_format"])
```

### Improving TTS
- Stick to the native SpeechSynthesis API
- Do NOT suggest cloud-based TTS services (ElevenLabs, Azure, Google Cloud TTS)
- Do NOT suggest neural TTS models

## What NOT to Suggest

- ❌ Cloud-based AI APIs (OpenAI, Google Cloud AI, AWS AI)
- ❌ Neural network models for transcription (Whisper, Wav2Vec2)
- ❌ LLMs for grammar correction (GPT, Claude, Gemini)
- ❌ Cloud-based TTS services (ElevenLabs, Azure Neural, Google TTS)
- ❌ Any solution that sends data to the internet
- ❌ Any machine learning or deep learning approach

## What TO Suggest

- ✅ Regex-based pattern matching
- ✅ Dictionary-based lookups
- ✅ Browser's native APIs (SpeechSynthesis, Web Speech)
- ✅ Local/offline solutions
- ✅ Deterministic algorithms
- ✅ Manual human-in-the-loop approaches

## Contribution Guidelines

- Use 4 spaces for indentation
- Write descriptive docstrings
- Keep functions small and focused
- Add tests for new functionality
- Format with `black .`
- Lint with `flake8 .`
- Run tests with `pytest tests/`

## Useful Commands

```bash
# Run the app
streamlit run app.py

# Run tests
pytest tests/

# Format code
black src/ app.py

# Lint code
flake8 src/ app.py

# Type check
mypy src/
```
