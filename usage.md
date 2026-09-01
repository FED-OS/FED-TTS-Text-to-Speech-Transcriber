# 📖 FED TTS - Usage Guide

## Getting Started

### Starting the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Features Overview

FED TTS has four main features:

1. **File Upload** – Upload audio files for transcription
2. **Manual Transcription** – Type what you hear while listening to audio
3. **Grammar & Spell Check** – Check your text for errors (No AI)
4. **Read Aloud** – Have text spoken aloud using your OS's native voices

## Using Each Feature

### 1. Uploading an Audio File

1. Click the "Upload Audio File" button or drag and drop a file
2. Supported formats: MP3, WAV, M4A, FLAC, OGG
3. The audio player will appear on the left side

**Tips:**
- For large files, be patient while they load
- The file stays in your browser's memory—nothing is uploaded to a server

### 2. Transcribing Audio

1. Upload your audio file (see above)
2. Press the play button on the audio player
3. Type what you hear in the text area on the right
4. **Right-click** the audio player for speed controls (slow down for difficult sections)
5. Your transcript is saved automatically in the session

**Tips for Efficient Transcription:**
- Use 0.75x speed for fast speech
- Use 1.5x speed for slow speech
- Take breaks—transcription is intensive work
- Type rough notes first, then polish later

### 3. Checking Grammar and Spelling

1. Type or paste text into the text area (or transcribe audio first)
2. Click the "Check Spelling & Grammar" button
3. Review the results:
   - 🟡 **Yellow warnings** = Potential spelling errors
   - 🔴 **Red messages** = Double spaces
   - ❓ **Question marks** = Grammar issues (e.g., "would of")
   - 📝 **Notes** = Style suggestions (passive voice, long sentences)
   - 🔁 **Repeated** = Duplicate words
   - ✂️ **Scissors** = Long sentences that may need splitting

**What the Checker Detects:**
- Misspelled words (dictionary-based)
- "would of" → "would have"
- "could of" → "could have"
- "should of" → "should have"
- "must of" → "must have"
- "alot" → "a lot"
- Double spaces
- Passive voice patterns ("was ... by")
- Sentences over 25 words
- Repeated words
- Missing capitalization at sentence starts

**Important:** The grammar checker is **100% deterministic** (no AI). It uses pattern matching, so it may miss context-dependent issues or produce occasional false positives. Always use your own judgment.

### 4. Reading Text Aloud

1. Enter text in the "Text to speak" area (defaults to your transcript)
2. Click "🗣️ Speak Now"
3. Your operating system's built-in voice will read the text
4. Click "⏹️ Stop" to stop the speech

**Tips:**
- The voice quality depends on your OS (Windows, macOS, Linux)
- You can install additional voices in your OS settings
- The speech is generated locally—no cloud TTS services are used

### 5. Using Without Audio Upload

You don't need to upload an audio file to use FED TTS! You can:
- Type or paste any text directly into the text area
- Use the grammar checker on any text
- Use the read-aloud feature on any text
- Check word and character counts in the sidebar

## Sidebar Features

### Word and Character Count
- See real-time word and character counts of your text

### Ko-fi Support
- Support the project by buying the developer a coffee

## Keyboard Shortcuts (Planned for v0.2.0)

| Shortcut | Action |
|----------|--------|
| Ctrl+Space | Play/Pause audio |
| Ctrl+Left | Rewind 5 seconds |
| Ctrl+Right | Forward 5 seconds |
| Ctrl+T | Insert timestamp |

## Tips for Best Results

### For Transcription
- Use headphones for clearer audio
- Slow down the playback for difficult sections
- Type in short segments
- Take breaks to avoid fatigue
- Proofread your transcript after completing it

### For Grammar Checking
- Check your text after completing your transcript
- Review each suggestion carefully
- Not all suggestions may apply to your context
- Use the checker as a guide, not a final authority

### For Read Aloud
- Test with a short passage first
- Adjust your system volume
- Try different OS voices if available
- The voice is robotic but functional (no AI TTS by design)

## Exporting Your Transcript (Planned)

Currently, you can copy your transcript manually:
1. Select all text in the text area (Ctrl+A)
2. Copy it (Ctrl+C)
3. Paste it into your preferred text editor (Ctrl+V)

Future versions will include:
- Export as TXT
- Export as PDF
- Auto-save to local storage

## Troubleshooting

See [FAQ.md](FAQ.md) and [SUPPORT.md](SUPPORT.md) for common issues and solutions.
