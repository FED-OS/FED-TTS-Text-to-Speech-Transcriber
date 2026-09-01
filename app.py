"""
FED TTS - Fluid Enhanced Dynamic Text-to-Speech
Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Zero AI.
"""

import streamlit as st
import re
from spellchecker import SpellChecker

from src.fed_tts.grammar_checker import GrammarChecker
from src.fed_tts.tts import get_tts_js


st.set_page_config(page_title="FED TTS (No AI)", layout="wide")

# Load custom CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("🎙️ FED TTS - Transcriber + Read Aloud + Grammar")
st.caption("⚡ 100% Offline. No AI. No Cloud APIs. Just pure deterministic Python + Browser features.")

# --- Session State Init ---
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# --- Row 1: Upload ---
uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a", "flac", "ogg"])

# --- Row 2: Player & Transcription ---
if uploaded_file:
    col_player, col_text = st.columns([1, 2])

    with col_player:
        st.subheader("🎧 Audio Player")
        st.audio(uploaded_file)
        st.caption("Tip: Right-click the player to change playback speed.")

    with col_text:
        st.subheader("📝 Transcription (Type manually)")
        st.session_state.transcript = st.text_area(
            "Write what you hear:",
            value=st.session_state.transcript,
            height=400,
            key="main_text",
        )
else:
    st.info("👆 Upload an audio file to begin transcribing, or just type text below to use the grammar checker and read-aloud features.")
    st.session_state.transcript = st.text_area(
        "Or type/paste text here:",
        value=st.session_state.transcript,
        height=300,
        key="main_text_no_upload",
    )

# --- Row 3: Grammarly Clone ---
st.divider()
col_check, col_read = st.columns(2)

with col_check:
    st.subheader("🔍 Grammar & Spell Check (No AI)")
    if st.button("Check Spelling & Grammar", use_container_width=True):
        text = st.session_state.transcript
        if not text.strip():
            st.warning("Please type some text first.")
        else:
            checker = GrammarChecker()
            results = checker.check(text)

            # Spell Check
            if results["misspelled"]:
                st.warning(f"🟡 Potential typos: {', '.join(list(results['misspelled'])[:20])}")
            else:
                st.success("✅ Spelling looks perfect!")

            # Grammar Rules
            if results["issues"]:
                for issue in results["issues"]:
                    st.info(issue)
            else:
                if results["misspelled"]:
                    st.info("📝 Grammar looks good (only spelling issues above).")
                else:
                    st.balloons()
                    st.success("✨ Your text looks clear and professional!")

with col_read:
    st.subheader("🔊 Read Aloud (Native OS Voice)")
    read_text = st.text_area("Text to speak:", value=st.session_state.transcript[:1000], height=100)
    if st.button("🗣️ Speak Now", use_container_width=True):
        if read_text.strip():
            js = get_tts_js(read_text)
            st.components.v1.html(js, height=0)
            st.success("🔊 Speaking via your OS!")
        else:
            st.warning("Please enter text to read.")

    # Stop button
    if st.button("⏹️ Stop", use_container_width=True):
        stop_js = """
        <script>
        window.speechSynthesis.cancel();
        </script>
        """
        st.components.v1.html(stop_js, height=0)

st.divider()
st.caption("⚡ 100% Offline. No AI. No Cloud APIs. Built with ❤️ using Streamlit.")

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 💖 Support the Project")
    st.markdown(
        """
        <a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
            <img height='36' style='border:0px;height:36px;' src='https://ko-fi.com/img/githubbutton_sm.svg' border='0' alt='Buy Me a Coffee at ko-fi.com' />
        </a>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### 📊 Stats")
    word_count = len(st.session_state.transcript.split()) if st.session_state.transcript else 0
    char_count = len(st.session_state.transcript) if st.session_state.transcript else 0
    st.metric("Words", word_count)
    st.metric("Characters", char_count)
