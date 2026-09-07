"""
Auto Transcriber Module - Offline automatic speech-to-text.

FED TTS was originally manual-only ("no AI" by design). This module adds a
fully local, deterministic speech-to-text option so uploaded audio AND video
files (mp4, mov, mkv, webm, ...) can be automatically transcribed without
any cloud service.

Pipeline:
  1. Uploaded media (any audio/video container) is written to a temp file.
  2. ffmpeg extracts/converts the audio track to 16 kHz mono PCM WAV
     (the format the Vosk models expect).
  3. The Vosk Kaldi recognizer streams the audio and emits words with
     timestamps.
  4. Words are assembled into readable sentences (with optional timestamps).

Everything runs on the user's machine. No network calls, no API keys.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import wave
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

SAMPLE_RATE = 16000
DEFAULT_MODEL = "vosk-model-small-en-us-0.15"

SUPPORTED_EXTENSIONS = {
    # audio
    "wav", "mp3", "m4a", "flac", "ogg", "aac", "opus", "wma", "aiff", "mpga",
    "mpeg",
    # video (the part that was missing!)
    "mp4", "mov", "mkv", "webm", "avi", "m4v", "mpg", "mpeg", "3gp", "wmv",
}


@dataclass
class TranscriptionWord:
    """A single recognized word with its start/end times in seconds."""
    word: str
    start: float
    end: float


@dataclass
class TranscriptionResult:
    """The full result of an automatic transcription run."""
    text: str = ""
    words: List[TranscriptionWord] = field(default_factory=list)
    duration_seconds: float = 0.0

    @property
    def word_count(self) -> int:
        return len(self.words)

    # ------------------------------------------------------------------
    # Chunking shared by timestamps / SRT / VTT
    # ------------------------------------------------------------------
    def cues(self, interval: float = 8.0) -> List["TranscriptionCue"]:
        """Group words into cues of at most `interval` seconds of speech."""
        cues: List[TranscriptionCue] = []
        current: List[TranscriptionWord] = []
        start = self.words[0].start if self.words else 0.0

        def flush() -> None:
            if current:
                cues.append(
                    TranscriptionCue(
                        start=current[0].start,
                        end=current[-1].end,
                        text=" ".join(w.word for w in current),
                    )
                )

        for w in self.words:
            if current and (w.start - current[0].start) > interval:
                flush()
                current = []
            current.append(w)
        flush()
        return cues

    def with_timestamps(self, interval: float = 8.0) -> str:
        """Return the text prefixed with a running [mm:ss] timestamp."""
        if not self.words:
            return ""
        return "\n".join(
            f"[{self._fmt(c.start)}] {c.text}" for c in self.cues(interval)
        )

    # ------------------------------------------------------------------
    # Subtitle export (SRT / WebVTT)
    # ------------------------------------------------------------------
    def to_srt(self, interval: float = 8.0) -> str:
        """Return the transcript as an .srt subtitle file."""
        blocks = []
        for i, c in enumerate(self.cues(interval), start=1):
            blocks.append(
                f"{i}\n{self._srt_time(c.start)} --> {self._srt_time(c.end)}\n{c.text}\n"
            )
        return "\n".join(blocks)

    def to_vtt(self, interval: float = 8.0) -> str:
        """Return the transcript as a .vtt (WebVTT) subtitle file."""
        lines = ["WEBVTT", ""]
        for i, c in enumerate(self.cues(interval), start=1):
            lines.append(f"{i}")
            lines.append(f"{self._vtt_time(c.start)} --> {self._vtt_time(c.end)}")
            lines.append(c.text)
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _srt_time(seconds: float) -> str:
        h, rem = divmod(max(0.0, seconds), 3600)
        m, s = divmod(rem, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"

    @staticmethod
    def _vtt_time(seconds: float) -> str:
        h, rem = divmod(max(0.0, seconds), 3600)
        m, s = divmod(rem, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{int(round((s - int(s)) * 1000)):03d}"

    @staticmethod
    def _fmt(seconds: float) -> str:
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"


@dataclass
class TranscriptionCue:
    """A timed chunk of transcript used for timestamps and subtitles."""
    start: float
    end: float
    text: str


def is_supported_file(filename: str) -> bool:
    """True if the uploaded file extension is audio or video we can handle."""
    ext = os.path.splitext(filename or "")[1].lstrip(".").lower()
    return ext in SUPPORTED_EXTENSIONS


def is_video_file(filename: str) -> bool:
    ext = os.path.splitext(filename or "")[1].lstrip(".").lower()
    return ext in {"mp4", "mov", "mkv", "webm", "avi", "m4v", "mpg", "mpeg",
                   "3gp", "wmv"}


def ffmpeg_available() -> bool:
    """True if the ffmpeg binary is on the PATH."""
    return shutil.which("ffmpeg") is not None


def find_model_dir(search_paths: Optional[Iterable[str]] = None) -> Optional[str]:
    """Locate a downloaded Vosk model directory.

    Checks the environment variable FED_TTS_VOSK_MODEL first, then a set of
    common locations (./models, ., ~/.cache/fed-tts, /tmp).
    """
    env = os.environ.get("FED_TTS_VOSK_MODEL")
    if env and os.path.isdir(env) and _looks_like_vosk_model(env):
        return env

    home = os.path.expanduser("~")
    candidates = list(search_paths or [])
    candidates += [
        os.path.join("models", DEFAULT_MODEL),
        DEFAULT_MODEL,
        os.path.join(home, ".cache", "fed-tts", DEFAULT_MODEL),
        os.path.join(home, ".cache", "fed-tts"),
        os.path.join(tempfile.gettempdir(), DEFAULT_MODEL),
    ]
    for path in candidates:
        if os.path.isdir(path) and _looks_like_vosk_model(path):
            return path
    return None


def _looks_like_vosk_model(path: str) -> bool:
    """A Vosk model dir contains conf, ivector, am or graph folders."""
    try:
        entries = set(os.listdir(path))
    except OSError:
        return False
    return bool(entries & {"conf", "ivector", "am", "graph", "MODEL_ID"})


def download_model(progress: Optional[callable] = None,
                   model_name: str = DEFAULT_MODEL,
                   dest_dir: Optional[str] = None) -> str:
    """Download and unzip a Vosk model from alphacephei.com (~40 MB small).

    Runs only once; afterwards find_model_dir() picks the model up locally.
    """
    import urllib.request
    import zipfile

    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    dest_root = dest_dir or os.path.join(
        os.path.expanduser("~"), ".cache", "fed-tts"
    )
    os.makedirs(dest_root, exist_ok=True)
    zip_path = os.path.join(dest_root, f"{model_name}.zip")

    if not os.path.exists(zip_path):
        if progress:
            progress(0.0, f"Downloading speech model ({model_name})…")
        urllib.request.urlretrieve(url, zip_path)

    if progress:
        progress(0.7, "Unpacking speech model…")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_root)

    os.remove(zip_path)
    model_path = os.path.join(dest_root, model_name)
    if progress:
        progress(1.0, "Model ready.")
    return model_path


class AutoTranscriber:
    """Offline automatic transcriber backed by Vosk + ffmpeg.

    Usage:
        t = AutoTranscriber()
        result = t.transcribe_file("interview.mp4")
        print(result.text)
    """

    def __init__(self, model_path: Optional[str] = None,
                 sample_rate: int = SAMPLE_RATE):
        self.model_path = model_path or find_model_dir()
        self.sample_rate = sample_rate
        self._model = None

    # -- model handling ----------------------------------------------------

    def model_ready(self) -> bool:
        if self.model_path and os.path.isdir(self.model_path):
            return True
        self.model_path = find_model_dir()
        return self.model_path is not None

    def ensure_model(self, progress: Optional[callable] = None) -> None:
        """Make sure a model is available, downloading it if needed."""
        if self.model_ready():
            if progress:
                progress(1.0, "Speech model found.")
            return
        self.model_path = download_model(progress=progress)
        if progress:
            progress(1.0, "Speech model ready.")

    def _load_model(self):
        if self._model is None:
            if not self.model_ready():
                raise RuntimeError(
                    "No Vosk model found. Call ensure_model() first."
                )
            from vosk import Model  # imported lazily so UI stays snappy

            self._model = Model(self.model_path)
        return self._model

    # -- audio extraction ---------------------------------------------------

    def extract_audio(self, media_path: str, out_path: Optional[str] = None,
                      progress: Optional[callable] = None) -> str:
        """Convert any media file to 16 kHz mono WAV using ffmpeg."""
        if not ffmpeg_available():
            raise RuntimeError(
                "ffmpeg is not installed. Install it (e.g. "
                "'sudo apt install ffmpeg' or 'brew install ffmpeg') to "
                "transcribe video/audio files automatically."
            )
        if out_path is None:
            out_path = media_path.rsplit(".", 1)[0] + ".fed16k.wav"
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", media_path,
            "-vn",                      # drop any video track
            "-ac", "1", "-ar", str(self.sample_rate),
            "-f", "wav", out_path,
        ]
        if progress:
            progress(0.1, "Extracting audio track…")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError(
                f"ffmpeg could not extract audio: {proc.stderr.strip()[:500]}"
            )
        if progress:
            progress(0.3, "Audio extracted.")
        return out_path

    # -- transcription -------------------------------------------------------

    def transcribe_file(self, media_path: str,
                        progress: Optional[callable] = None,
                        keep_wav: bool = False) -> TranscriptionResult:
        """Transcribe an audio or video file completely offline."""
        wav_path = self.extract_audio(media_path, progress=progress)
        try:
            return self.transcribe_wav(wav_path, progress=progress)
        finally:
            if not keep_wav and wav_path != media_path:
                try:
                    os.remove(wav_path)
                except OSError:
                    pass

    def transcribe_wav(self, wav_path: str,
                       progress: Optional[callable] = None) -> TranscriptionResult:
        """Transcribe a PCM WAV file with Vosk. Returns words + text."""
        from vosk import KaldiRecognizer

        model = self._load_model()
        wf = wave.open(wav_path, "rb")
        try:
            if wf.getnchannels() != 1 or wf.getframerate() != self.sample_rate:
                raise RuntimeError(
                    "WAV must be mono PCM at "
                    f"{self.sample_rate} Hz (use extract_audio())."
                )
            rec = KaldiRecognizer(model, self.sample_rate)
            rec.SetWords(True)

            words: List[TranscriptionWord] = []
            frames = 0
            total = wf.getnframes()
            chunk = 8000
            while True:
                data = wf.readframes(chunk)
                if not data:
                    break
                frames += chunk
                if rec.AcceptWaveform(data):
                    words.extend(self._parse_chunk(rec.Result()))
                if progress and total:
                    frac = min(1.0, frames / total)
                    progress(0.3 + 0.6 * frac,
                             f"Transcribing… {int(frac * 100)}%")
            words.extend(self._parse_chunk(rec.FinalResult()))
        finally:
            wf.close()

        if progress:
            progress(1.0, "Done.")
        return TranscriptionResult(
            text=self._words_to_text(words),
            words=words,
            duration_seconds=frames / self.sample_rate if frames else
                (words[-1].end if words else 0.0),
        )

    # -- helpers --------------------------------------------------------------

    @staticmethod
    def _parse_chunk(result_json: str) -> List[TranscriptionWord]:
        try:
            data = json.loads(result_json) if result_json else {}
        except json.JSONDecodeError:
            return []
        return [
            TranscriptionWord(w["word"], float(w["start"]), float(w["end"]))
            for w in data.get("result", [])
        ]

    @staticmethod
    def _words_to_text(words: List[TranscriptionWord]) -> str:
        if not words:
            return ""
        text = " ".join(w.word for w in words)
        # Vosk emits tokens like '[music]', noise markers and confidence junk
        text = re.sub(r"\[(noise|music|laughter|silence|breath)\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        # capitalize standalone "i", sentence starts, add punctuation
        text = re.sub(r"\bi\b", "I", text)
        sentences = re.split(r"(?<=[.!?])\s+", text)
        out = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            if not s[0].isupper():
                s = s[0].upper() + s[1:]
            if s[-1] not in ".!?":
                s += "."
            out.append(s)
        return " ".join(out)


def transcribe_media(media_path: str,
                     progress: Optional[callable] = None) -> TranscriptionResult:
    """Convenience one-shot function used by the Streamlit app."""
    t = AutoTranscriber()
    t.ensure_model(progress=progress)
    return t.transcribe_file(media_path, progress=progress)
