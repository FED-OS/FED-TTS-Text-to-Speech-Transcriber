# Architecture

This document describes the architecture and design decisions behind FED TTS.

## Overview

FED TTS (Fluid Enhanced Dynamic Text-to-Speech) is a Streamlit-based web
application that combines three tools into one:

1. **Transcriber** — Upload audio files and manually transcribe them
2. **Read Aloud** — Browser-native text-to-speech using the OS's built-in voices
3. **Grammar Checker** — Dictionary-based spell checking and regex-based grammar rules

All three tools follow a strict **"No AI" philosophy**: no neural networks, no
cloud APIs, no LLMs, no generative AI. Everything runs locally using
deterministic algorithms.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FED TTS Application                   │
│                      (Streamlit)                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Transcriber  │  │  Read Aloud  │  │   Grammar    │  │
│  │              │  │              │  │   Checker    │  │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │  │
│  │  │ Audio  │  │  │  │  TTS   │  │  │  │ Spell  │  │  │
│  │  │ Upload │  │  │  │  JS    │  │  │  │ Check  │  │  │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │  │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │  │
│  │  │ Audio  │  │  │  │ Stop   │  │  │  │ Grammar│  │  │
│  │  │ Player │  │  │  │ Button │  │  │  │ Rules  │  │  │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │  │
│  │  ┌────────┐  │  │              │  │              │  │
│  │  │Manual  │  │  │              │  │              │  │
│  │  │Text    │  │  │              │  │              │  │
│  │  │Area    │  │  │              │  │              │  │
│  │  └────────┘  │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Session State (st.session_state)      │    │
│  │         Persists transcript across reruns          │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │                   Sidebar                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │    │
│  │  │ Word     │  │ Char     │  │ Ko-fi Button │  │    │
│  │  │ Count    │  │ Count    │  │              │  │    │
│  │  └──────────┘  └──────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  Local File     │  │  Browser       │  │  pyspellchecker│
│  (Audio Upload) │  │  SpeechSynth   │  │  Dictionary    │
│  No cloud       │  │  API (OS TTS)  │  │  (Offline)     │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Component Design

### 1. Transcriber Module (`src/fed_tts/transcriber.py`)

The transcriber module handles audio file uploads and provides a custom audio
player for listening while transcribing.

**Key Design Decisions:**

- **Manual transcription only**: No automatic speech recognition (ASR) is used.
  The user listens to the audio and types the transcript manually. This keeps
  the tool completely AI-free.
- **Audio as data URI**: Uploaded audio files are converted to base64 data URIs
  for embedding in HTML, avoiding the need for a file server.
- **Custom audio player**: A custom HTML5 audio player with rewind (−5s),
  fast-forward (+5s), and speed control buttons improves the transcription
  workflow.

**Data Flow:**
```
User uploads file → bytes read → base64 encode → data URI → HTML audio player
                                                                  ↓
User types transcript → st.session_state → persisted across reruns
```

### 2. TTS Module (`src/fed_tts/tts.py`)

The TTS module generates JavaScript that uses the browser's native
`SpeechSynthesis` API for text-to-speech.

**Key Design Decisions:**

- **Browser-native TTS**: Uses the `window.speechSynthesis` API, which leverages
  the operating system's built-in speech synthesis voices. No cloud TTS
  services (Google, Amazon, Azure) are used.
- **JavaScript injection**: TTS is implemented by injecting JavaScript via
  `st.components.v1.html()`, which runs in an iframe within the Streamlit app.
- **Stop functionality**: A separate `get_stop_js()` function provides the
  ability to stop speech playback.
- **Parameter control**: Rate, pitch, and volume can be adjusted via parameters.

**Data Flow:**
```
Text input → get_tts_js(text, rate, pitch, volume) → JS string
                                                        ↓
                                            st.components.v1.html()
                                                        ↓
                                        window.speechSynthesis.speak()
                                                        ↓
                                              OS-native voice output
```

### 3. Grammar Checker Module (`src/fed_tts/grammar_checker.py`)

The grammar checker combines dictionary-based spell checking with regex-based
grammar rule matching.

**Key Design Decisions:**

- **pyspellchecker**: Uses `pyspellchecker` which uses Levenshtein distance and
  frequency-based dictionaries for spell checking. This is a deterministic
  algorithm, not a neural network.
- **Regex grammar rules**: Grammar rules are defined as regex patterns in a
  `grammar_rules` list. Each rule has a name, pattern, message, and suggestion.
  This makes rules easy to add, modify, and test.
- **No context-free grammar parser**: FED TTS does not attempt full NLP parsing.
  It uses targeted regex patterns for common mistakes, keeping the tool simple
  and deterministic.

**Grammar Rule Structure:**
```python
{
    "name": "would_of",
    "pattern": r"\bwould of\b",
    "message": "'would of' is incorrect. Use 'would have' instead.",
    "suggestion": "would have",
}
```

**Data Flow:**
```
Text input → check_spelling() → pyspellchecker → misspelled words + suggestions
           → check_grammar() → regex matching → rule violations + suggestions
                              → combine results → return dict
```

### 4. Session State Management

Streamlit reruns the entire script on every interaction. To persist the
transcript across reruns, FED TTS uses `st.session_state`.

**Key Pattern:**
```python
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

transcript = st.text_area("Transcript", value=st.session_state.transcript)
st.session_state.transcript = transcript
```

### 5. UI Layer (`app.py`)

The main application file (`app.py`) ties everything together:

- Renders the Streamlit UI with a header, file uploader, audio player,
  transcript text area, and grammar check results
- Manages session state for the transcript
- Handles button clicks for "Check Grammar" and "Read Aloud"
- Displays the Ko-fi support button in the sidebar
- Shows word and character counts in the sidebar
- Loads custom CSS from `styles.css`

## Data Flow

### Complete User Journey

```
1. User opens app
   └→ Streamlit renders app.py
      └→ Loads styles.css
      └→ Initializes session_state

2. User uploads audio file (MP3/WAV/M4A/FLAC/OGG)
   └→ File stored in session as bytes
   └→ audio_to_data_uri() converts to base64
   └→ Custom audio player rendered in HTML

3. User plays audio and types transcript
   └→ Text stored in st.session_state.transcript
   └→ Word/char counts update in sidebar

4. User clicks "Check Grammar"
   └→ GrammarChecker.check() called
      └→ check_spelling() → pyspellchecker
      └→ check_grammar() → regex rules
   └→ Results displayed below text area

5. User clicks "Read Aloud"
   └→ get_tts_js(text) generates JavaScript
   └→ st.components.v1.html() injects JS
   └→ Browser SpeechSynthesis reads text
   └→ OS-native voice plays audio

6. User clicks "Stop"
   └→ get_stop_js() generates JavaScript
   └→ speechSynthesis.cancel() stops playback
```

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| UI Framework | Streamlit | Python-native, easy deployment, no JS needed |
| Spell Checking | pyspellchecker | Dictionary-based, offline, deterministic |
| Grammar Checking | Python `re` module | Regex pattern matching, deterministic |
| Text-to-Speech | Browser SpeechSynthesis API | OS-native, no cloud, no AI |
| State Management | st.session_state | Built into Streamlit, persists across reruns |
| Styling | CSS | Custom styles loaded via st.markdown |
| Audio Playback | HTML5 Audio API | Native browser support, no plugins |
| Packaging | pyproject.toml + setuptools | Modern Python packaging standard |

## No AI Architecture

The "No AI" philosophy is enforced at every level:

1. **No neural networks**: No PyTorch, TensorFlow, or similar frameworks
2. **No cloud APIs**: All processing happens in the browser or locally
3. **No LLMs**: No OpenAI, Anthropic, or other LLM API calls
4. **No ML models**: No pre-trained models are loaded or used
5. **Deterministic algorithms**: Same input always produces same output
6. **Privacy by design**: No data leaves the user's machine

This is verified by the CI pipeline, which includes a check that scans for
AI/ML library imports in all changed files (see
`.github/workflows/dependency-review.yml` and `.github/workflows/pr.yml`).

## Security Considerations

- **No data transmission**: Audio files and transcripts never leave the user's
  browser. They are processed entirely client-side.
- **Base64 encoding**: Audio is encoded as data URIs for local playback only.
- **No external scripts**: The only JavaScript injected is the TTS code, which
  uses the browser's native API.
- **Input sanitization**: Text is escaped before being embedded in JavaScript
  to prevent injection attacks.

## Extension Points

FED TTS is designed to be extensible:

1. **Adding grammar rules**: Add entries to the `grammar_rules` list in
   `grammar_checker.py`
2. **Custom spell dictionaries**: `pyspellchecker` supports custom word lists
3. **TTS voice selection**: The `get_voices_js()` function can be extended to
   allow voice selection
4. **Custom audio player controls**: The player JavaScript can be modified to
   add new controls
5. **Export functionality**: Future versions may add TXT/PDF export (planned in
   roadmap)

## Related Documents

- [ADR.md](../ADR.md) — Architecture Decision Records
- [API Reference](api.md) — Detailed API documentation
- [Quick Start](quickstart.md) — Getting started guide
- [ROADMAP.md](../ROADMAP.md) — Future development plans
- [FAQ.md](../FAQ.md) — Frequently asked questions
