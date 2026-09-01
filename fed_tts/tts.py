"""
TTS Module - No AI, uses browser's native SpeechSynthesis API.

Generates JavaScript to be injected via Streamlit components.
This uses the operating system's built-in voices (Windows SAPI, macOS say, etc.).
No cloud TTS services are used.
"""


def get_tts_js(text, rate=1.0, pitch=1.0, volume=1.0):
    """
    Generate JavaScript for browser's native SpeechSynthesis API.

    Args:
        text: The text to speak
        rate: Speech rate (0.1 to 10, default 1.0)
        pitch: Speech pitch (0 to 2, default 1.0)
        volume: Speech volume (0 to 1, default 1.0)

    Returns:
        JavaScript string to be injected via st.components.v1.html
    """
    # Escape special characters for JavaScript
    safe_text = text.replace("\\", "\\\\").replace("'", "\\'").replace("`", "\\`").replace("\n", " ")

    js = f"""
    <script>
    (function() {{
        var msg = new SpeechSynthesisUtterance(`{safe_text}`);
        msg.rate = {rate};
        msg.pitch = {pitch};
        msg.volume = {volume};
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }})();
    </script>
    """
    return js


def get_voices_js():
    """Generate JavaScript to list available system voices."""
    js = """
    <script>
    (function() {
        var voices = window.speechSynthesis.getVoices();
        var voiceList = voices.map(function(v, i) {
            return i + ': ' + v.name + ' (' + v.lang + ')';
        }).join('\\n');
        console.log(voiceList);
    })();
    </script>
    """
    return js


def get_stop_js():
    """Generate JavaScript to stop speech synthesis."""
    js = """
    <script>
    window.speechSynthesis.cancel();
    </script>
    """
    return js
