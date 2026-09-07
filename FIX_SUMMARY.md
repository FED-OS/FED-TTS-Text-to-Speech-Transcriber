# FED TTS — MP4 Transcription Fix Summary

## The Problem

Uploading MP4 files to FED TTS never produced a transcript. After studying all four archived versions of the project (v1 text-generator fork, v2/v3/v4 manual transcription app), two root causes were found:

1. **MP4 was rejected at the door.** The file uploader was `st.file_uploader(type=["wav", "mp3", "m4a", "flac", "ogg"])`. Streamlit blocks any file with an unlisted extension, so MP4 uploads failed before anything else could happen.
2. **There was no automatic transcription at all.** Every version of the app was a *manual* transcription workspace — you played the audio and typed what you heard. Even a supported MP3 would not have produced a transcript on its own.

## The Fix (100% offline, true to the project's no-cloud philosophy)

**New module `src/fed_tts/auto_transcriber.py`** (~330 lines):
- **Vosk offline speech recognition** — the compact `vosk-model-small-en-us-0.15` (~40 MB) Kaldi-based model runs entirely on your machine. No API keys, no cloud calls. Downloaded once to `~/.cache/fed-tts/` (or point `FED_TTS_VOSK_MODEL` at any local model, e.g. for other languages).
- **ffmpeg audio extraction** — video containers (MP4, MOV, MKV, WEBM, AVI, ...) are converted to 16 kHz mono WAV before recognition.
- **20 supported formats** — audio (MP3, WAV, M4A, FLAC, OGG, AAC, OPUS, WMA, AIFF) and video (MP4, MOV, MKV, WEBM, AVI, MPG/MPEG, M4V, WMV, 3GP).
- Word-level timing → optional `[mm:ss]` timestamps, sentence capitalization, punctuation, and cleanup of noise markers.

**Rewritten `app.py`:**
- Uploader accepts all 20 formats; video files get a `st.video` player.
- New **🤖 Auto Transcribe** tab: one-click "Transcribe Automatically" button with live progress bar, optional timestamps checkbox, editable transcript box with sync-back, and a 💾 Download .txt button.
- The ✍️ Manual tab, grammar checker, and Read Aloud all work as before — auto transcripts flow straight into them.
- Sidebar shows transcription engine status (model availability, ffmpeg detection) plus word/character stats.

## Verification (live browser test, real human speech)

Uploaded `alice_30s.mp4` (30.5 s LibriVox recording of *Alice's Adventures in Wonderland*, AAC audio in an MP4 container) into the running app:

> ✅ **Transcribed 64 words from 30.5s of audio**
> "Chapter one of alice's adventures in wonderland this is a librivox recording all librivox recordings are in the public domain... by lewis carroll chapter one down the rabbit hole alice was beginning to get very tired of sitting."

- Transcript appeared in both the Auto and Manual tabs, sidebar updated (Words: 64, Characters: 361), download button appeared, and "Check Spelling & Grammar" ran cleanly on the auto transcript.
- A transcript-display bug found during live testing (Streamlit widget session-state desync) was fixed and re-verified.
- **35 unit tests pass** (`pytest tests/`), covering format acceptance, model discovery, timestamping, punctuation cleanup, ffmpeg extraction (16 kHz mono verification), and the end-to-end MP4 pipeline.

## How to Run

```bash
pip install -r requirements.txt        # now includes vosk
# ensure ffmpeg is installed (sudo apt-get install ffmpeg / brew install ffmpeg)
streamlit run app.py
```

First transcription downloads the ~40 MB English model once; after that the app is fully offline.

## Files Changed / Added

| File | Change |
|---|---|
| `src/fed_tts/auto_transcriber.py` | **NEW** — offline STT engine (Vosk) + ffmpeg extraction + formatting |
| `app.py` | Rewritten — video upload, Auto Transcribe tab, progress, download, session-state fixes |
| `requirements.txt` | Added `vosk>=0.3.45` |
| `tests/test_auto_transcriber.py` | **NEW** — 35-test suite (with existing tests) |
| `README.md`, `usage.md`, `FAQ.md`, `CHANGELOG.md` | Updated for MP4/video + automatic transcription |
