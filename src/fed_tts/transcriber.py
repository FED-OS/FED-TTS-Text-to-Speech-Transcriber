"""
Transcriber Module - Manual transcription workspace logic.

Since FED TTS uses NO AI, transcription is done manually by the user.
This module provides helpers for managing transcription state and
generating the custom audio player.
"""

import base64


def audio_to_data_uri(audio_bytes, mime_type="audio/wav"):
    """Convert audio bytes to a base64 data URI for HTML embedding."""
    b64 = base64.b64encode(audio_bytes).decode()
    return f"data:{mime_type};base64,{b64}"


def get_custom_audio_player_js(data_uri, mime_type="audio/wav"):
    """
    Generate a custom HTML5 audio player with rewind/forward/speed controls.

    This provides a better transcription experience than the basic st.audio.
    """
    html = f"""
    <div style="padding: 10px; background: #f8f9fa; border-radius: 8px;">
        <audio id="fed-audio-player" controls style="width: 100%;">
            <source src="{data_uri}" type="{mime_type}">
            Your browser does not support the audio element.
        </audio>
        <div style="margin-top: 10px; display: flex; gap: 5px; flex-wrap: wrap;">
            <button onclick="rewindAudio(5)" style="padding: 5px 10px; cursor: pointer;">⏪ -5s</button>
            <button onclick="forwardAudio(5)" style="padding: 5px 10px; cursor: pointer;">⏩ +5s</button>
            <button onclick="rewindAudio(10)" style="padding: 5px 10px; cursor: pointer;">⏪ -10s</button>
            <button onclick="forwardAudio(10)" style="padding: 5px 10px; cursor: pointer;">⏩ +10s</button>
            <button onclick="setSpeed(0.5)" style="padding: 5px 10px; cursor: pointer;">0.5x</button>
            <button onclick="setSpeed(0.75)" style="padding: 5px 10px; cursor: pointer;">0.75x</button>
            <button onclick="setSpeed(1.0)" style="padding: 5px 10px; cursor: pointer;">1.0x</button>
            <button onclick="setSpeed(1.5)" style="padding: 5px 10px; cursor: pointer;">1.5x</button>
            <button onclick="setSpeed(2.0)" style="padding: 5px 10px; cursor: pointer;">2.0x</button>
        </div>
        <p style="font-size: 12px; color: #6c757d; margin-top: 5px;">
            Keyboard: Ctrl+Space = Play/Pause, Ctrl+Left = Rewind, Ctrl+Right = Forward
        </p>
    </div>
    <script>
    function rewindAudio(seconds) {{
        var player = document.getElementById('fed-audio-player');
        player.currentTime -= seconds;
    }}
    function forwardAudio(seconds) {{
        var player = document.getElementById('fed-audio-player');
        player.currentTime += seconds;
    }}
    function setSpeed(rate) {{
        var player = document.getElementById('fed-audio-player');
        player.playbackRate = rate;
    }}
    </script>
    """
    return html


def get_timestamp():
    """Get a formatted timestamp string for inserting into transcripts."""
    from datetime import datetime

    return datetime.now().strftime("[%H:%M:%S]")
