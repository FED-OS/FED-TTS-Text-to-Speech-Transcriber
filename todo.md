# Fix FED TTS: auto-transcribe uploaded MP4 files

## Diagnosis
- [x] Study project + all old versions (v1 text-generator fork, v2/v3/v4 manual "no AI" app)
- [x] Identify issue 1: file_uploader rejects mp4 (only wav/mp3/m4a/flac/ogg)
- [x] Identify issue 2: no automatic transcription exists (manual-only by design)

## Fix
- [x] Copy v4 project to /workspace/fed-tts as base
- [x] Install ffmpeg + Python deps (streamlit, vosk, pyspellchecker)
- [x] Create auto_transcriber.py (Vosk offline STT + ffmpeg audio extraction)
- [x] Update app.py: accept mp4/video files, "Transcribe automatically" button, progress, result fills transcript box; keep manual mode
- [x] Update requirements.txt
- [x] Add tests for auto transcriber (35 tests, all passing)

## Verify
- [x] Create a real speech mp4 test file (LibriVox human speech → ffmpeg → MP4/AAC)
- [x] Run unit tests
- [x] Live-run the app and auto-transcribe the test mp4 end-to-end (64 words from 30.5s audio; transcript visible in both tabs; sidebar stats; download button; grammar check + read aloud verified)
- [x] Fix transcript display session-state bug found during live testing
- [x] Update README.md, usage.md, FAQ.md, CHANGELOG.md for MP4/video + auto transcription
- [x] Package fixed project as zip and deliver
