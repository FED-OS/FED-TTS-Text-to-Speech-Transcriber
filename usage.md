# 📖 FED TTS - Usage Guide

## Getting Started

### Starting the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Features Overview

FED TTS has five main features:

1. **File Upload** – Upload audio *or video* files for transcription (MP4, MOV, MKV, MP3, WAV, ...)
2. **Automatic Transcription** – One-click offline speech-to-text (Vosk engine, 100% local)
3. **Manual Transcription** – Type what you hear while listening to audio
4. **Grammar & Spell Check** – Check your text for errors (No AI)
5. **Read Aloud** – Have text spoken aloud using your OS's native voices

## Using Each Feature

### 1. Uploading an Audio or Video File

1. Click the "Upload Audio or Video File" button or drag and drop a file
2. Supported audio formats: MP3, WAV, M4A, FLAC, OGG, AAC, OPUS, WMA, AIFF
3. Supported video formats: MP4, MOV, MKV, WEBM, AVI, MPG/MPEG, WMV, 3GP, M4V
4. The media player will appear above the transcript workspace

**Tips:**
- For large files, be patient while they load
- The file stays in your browser's memory—nothing is uploaded to a server
- Video files require **ffmpeg** to be installed on your machine (see the error banner in the app if it's missing)

### 2. Transcribing Automatically (MP4 and Other Media)

1. Upload an audio or video file (see above)
2. Go to the **🤖 Auto Transcribe** tab
3. Click **🤖 Transcribe Automatically**
4. On first use, the offline Vosk English model (~40 MB) is downloaded once to your home directory cache; after that, everything runs fully offline
5. Watch the live progress bar while the speech is converted to text
6. The transcript appears in the editable auto-transcript box and the ✍️ Manual workspace
7. Optional: tick **Include [mm:ss] timestamps** before transcribing to add time markers
8. Export your work from the 🎬 Subtitles and 🧰 Tools tabs (see below)

**Tips for Best Results:**
- Clear, single-speaker audio gives the best accuracy
- Very noisy recordings or overlapping speakers will produce more errors
- The auto transcript is a great first draft—switch to the ✍️ Manual tab to polish it
- For languages other than English, replace the model in `~/.cache/fed-tts/` with a matching Vosk model from alphacephei.com/vosk/models

### 2b. Exporting Subtitles (SRT / VTT)

1. Run an automatic transcription first (subtitles are built from its word timings)
2. Switch to the **🎬 Subtitles** tab
3. Review the cue table—each row shows its start time and text
4. Adjust **Cue length (seconds)** (2–30 s) to change how many words go into each subtitle block; the table updates live
5. Click **💾 SRT**, **💾 VTT**, or **💾 TXT** to download

**Where to use the files:**
- SRT/VTT load directly into VLC, YouTube uploads, Premiere Pro, DaVinci Resolve, and most video editors for burn-in subtitles
- SRT uses `HH:MM:SS,mmm` timing; VTT uses `HH:MM:SS.mmm` and starts with a `WEBVTT` header—both are generated with correct formatting automatically

### 2c. Transcript Tools (Find & Replace, Case, History)

The **🧰 Tools** tab keeps every cleanup job in one place:

- **Find & Replace**: type what to find and the replacement, optionally enable **Regex mode** or **Case-sensitive**, then click **Replace all**—the count of replacements is confirmed with a toast and a history snapshot
- **Case & Cleanup**: one-click UPPERCASE, lowercase, Sentence case, and Trim extra spaces
- **Transcript history**: every transcribe, replace, or case change is snapshotted (up to 25 entries this session); click **Restore** on any snapshot to roll back, or **🗑️ Clear history** to start fresh

### 3. Transcribing Manually

1. Upload your audio or video file (see above)
2. Switch to the **✍️ Manual** tab and press play on the media player
3. Type what you hear in the text area
4. **Right-click** the audio player for speed controls (slow down for difficult sections)
5. Your transcript is saved automatically in the session

**Tips for Efficient Transcription:**
- Use 0.75x speed for fast speech
- Use 1.5x speed for slow speech
- Take breaks—transcription is intensive work
- Type rough notes first, then polish later

### 4. Checking Grammar and Spelling

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

### 5. Reading Text Aloud

1. Enter text in the "Text to speak" area (defaults to your transcript)
2. Click "🗣️ Speak Now"
3. Your operating system's built-in voice will read the text
4. Click "⏹️ Stop" to stop the speech

**Tips:**
- The voice quality depends on your OS (Windows, macOS, Linux)
- You can install additional voices in your OS settings
- The speech is generated locally—no cloud TTS services are used

### 6. Using Without Audio Upload

You don't need to upload an audio file to use FED TTS! You can:
- Type or paste any text directly into the text area
- Use the grammar checker on any text
- Use the read-aloud feature on any text
- Check word and character counts in the sidebar

## Sidebar Features

### 🎨 Appearance (Dark Mode & Theming)

1. Open the **🎨 Appearance** panel at the top of the sidebar
2. **Theme**: pick **Dark**, **Light**, or **Auto (follow OS)**—Auto switches with your operating system's dark mode setting
3. **Accent colour**: blue, violet, emerald, rose, or amber—buttons, sliders, and highlights change instantly
4. **Font size**: scale the whole interface from 85% to 125%
5. **Rounded corners** and **Monospace editor**: toggle the corner style and a fixed-width font for the transcript editors
6. Click **💾 Save appearance** to persist your choices to `~/.config/.fed-tts/settings.json`—they'll be restored on every future launch. Settings are validated on load; a corrupt file simply falls back to defaults.

### Word and Character Count
- See real-time word and character counts of your text (plus auto-transcript words and estimated speaking time in the stat strip)

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

### "ffmpeg not found" when uploading a video (MP4, MOV, ...)

Video containers need ffmpeg to extract audio. Install it:

- **Debian/Ubuntu**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: `winget install ffmpeg` (then restart the app)

### Auto transcription produces empty text

- The file may contain music or noise instead of speech (the engine is speech-only)
- Very quiet audio: try boosting the volume in an editor first
- The model works best with clear English speech

### The model download fails on first use

- The ~40 MB model is fetched once from `https://alphacephei.com/vosk/models/`
- Behind a proxy? Set `HTTPS_PROXY` or pre-download the zip and unzip it to `~/.cache/fed-tts/vosk-model-small-en-us-0.15`
- You can point to any local Vosk model with the `FED_TTS_VOSK_MODEL=/path/to/model` environment variable

See [FAQ.md](FAQ.md) and [SUPPORT.md](SUPPORT.md) for common issues and solutions.
