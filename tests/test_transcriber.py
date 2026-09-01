"""Test the transcriber module."""

import pytest
from src.fed_tts.transcriber import get_timestamp, audio_to_data_uri


class TestTimestamp:
    def test_timestamp_format(self):
        """Timestamp should be in [HH:MM:SS] format."""
        ts = get_timestamp()
        assert ts.startswith("[") and ts.endswith("]")
        assert len(ts) == 10  # [HH:MM:SS] = 10 chars


class TestAudioDataUri:
    def test_data_uri_conversion(self):
        """Audio bytes should be converted to a base64 data URI."""
        test_bytes = b"fake audio data"
        uri = audio_to_data_uri(test_bytes, "audio/wav")
        assert uri.startswith("data:audio/wav;base64,")


class TestTTS:
    def test_tts_js_generation(self):
        """TTS JavaScript should be generated correctly."""
        from src.fed_tts.tts import get_tts_js

        js = get_tts_js("Hello world")
        assert "SpeechSynthesisUtterance" in js
        assert "Hello world" in js

    def test_tts_js_escapes_quotes(self):
        """TTS JavaScript should escape quotes in text."""
        from src.fed_tts.tts import get_tts_js

        js = get_tts_js("It's a test")
        assert "\\'" in js

    def test_stop_js(self):
        """Stop JS should cancel speech synthesis."""
        from src.fed_tts.tts import get_stop_js

        js = get_stop_js()
        assert "cancel" in js
