# 📝 Architecture Decision Records (ADR)

## What is an ADR?

Architecture Decision Records capture important architectural decisions made during the project's development. They document the context, decision, and consequences of each significant choice.

---

## ADR-001: Use Streamlit for the UI

**Status:** Accepted  
**Date:** 2026-01-01

### Context
We needed a fast way to build a desktop-like interface for audio transcription and TTS. Options included Tkinter, Electron, Streamlit, and Flask.

### Decision
Use Streamlit because:
- Rapid development with Python
- Built-in components (audio player, file uploader, text areas)
- Cross-platform support
- Good for MVPs and prototypes
- Large community and ecosystem

### Consequences
- **Positive**: Fast development, Python-native, easy to deploy, good component library
- **Negative**: Limited audio player controls (requires custom HTML for advanced features), server-client architecture means some state management complexity

---

## ADR-002: No AI/ML Approach

**Status:** Accepted  
**Date:** 2026-01-01

### Context
The project needed transcription and grammar checking capabilities. The default modern approach uses AI/ML models (Whisper, Grammarly API, LLMs, etc.). We needed to decide whether to use AI or not.

### Decision
Use deterministic, non-AI approaches:
- Manual transcription (user types what they hear)
- Dictionary-based spell checking (pyspellchecker)
- Regex-based grammar rules
- Native browser TTS (SpeechSynthesis API)

### Consequences
- **Positive**: 100% private (no cloud), no API costs, works offline, predictable behavior, no model downloads, lightweight
- **Negative**: Lower accuracy (no automatic transcription), more manual work for users, robotic TTS voices, limited grammar checking compared to AI

### Rationale
Privacy and cost were the primary drivers. Many users (journalists, lawyers, doctors) need to transcribe sensitive audio without sending it to cloud services. The "No AI" approach also eliminates ongoing API costs and dependency on external services.

---

## ADR-003: Native SpeechSynthesis API for TTS

**Status:** Accepted  
**Date:** 2026-01-01

### Context
We needed TTS without sending data to the cloud. Options included eSpeak (formant synthesis), Festival (diphone concatenation), or the browser's native SpeechSynthesis API.

### Decision
Use the browser's built-in SpeechSynthesis API because:
- Available in every modern browser
- Uses OS-level voices (Windows SAPI, macOS `say`, Linux speech-dispatcher)
- Zero installation required
- No additional dependencies
- Works within Streamlit's component system

### Consequences
- **Positive**: Works out of the box, no dependencies, uses system voices, no cloud calls
- **Negative**: Voices are robotic (less natural than ElevenLabs or Azure Neural), voice quality varies by OS, limited prosody control

---

## ADR-004: pyspellchecker for Spell Checking

**Status:** Accepted  
**Date:** 2026-01-01

### Context
We needed spell checking without AI. Options included Hunspell (via cyhunspell), pyspellchecker, or aspell.

### Decision
Use pyspellchecker because:
- Pure Python (no C dependencies)
- Easy to install (pip install pyspellchecker)
- Uses frequency list-based dictionary (no AI/ML)
- Supports multiple languages
- Active maintenance

### Consequences
- **Positive**: Easy installation, pure Python, good accuracy for common words, multi-language support
- **Negative**: Larger package size (includes word frequency lists), may not catch all domain-specific terms

---

## ADR-005: Regex-Based Grammar Rules

**Status:** Accepted  
**Date:** 2026-01-01

### Context
We needed grammar checking without AI/LLMs. Options included LanguageTool (has AI components), pure regex rules, or a hybrid approach.

### Decision
Use regex-based grammar rules because:
- 100% deterministic and predictable
- No AI/ML dependencies
- Easy to understand and modify
- Fast execution
- Transparent (users can see exactly what rules are being applied)

### Consequences
- **Positive**: No AI, transparent, fast, easy to extend, no external dependencies
- **Negative**: Limited to pattern matching (can't understand context), may produce false positives, can't catch complex grammar issues that require understanding

---

## ADR-006: Session State for Transcript Persistence

**Status:** Accepted  
**Date:** 2026-01-01

### Context
Streamlit reruns the entire script on every interaction. We needed to persist the user's transcript across these reruns.

### Decision
Use Streamlit's `st.session_state` to store the transcript text.

### Consequences
- **Positive**: Transcript persists across reruns, no external storage needed, simple implementation
- **Negative**: Data is lost when the browser tab is closed or refreshed, no long-term persistence (planned for v0.2.0 with local storage)

---

## ADR-007: Project Structure with src/ Layout

**Status:** Accepted  
**Date:** 2026-01-01

### Context
We needed to decide on the project structure. Options included flat layout (all files in root) or src/ layout (code in src/ directory).

### Decision
Use src/ layout with `src/fed_tts/` package directory because:
- Standard Python project structure
- Clear separation of source code from tests and docs
- Prevents accidental imports from the current directory
- Better for packaging and distribution
- Follows modern Python packaging best practices

### Consequences
- **Positive**: Professional structure, easy packaging, clear organization
- **Negative**: Slightly more complex import paths, requires proper package configuration in pyproject.toml
