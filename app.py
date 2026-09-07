"""
FED TTS - Fluid Enhanced Dynamic Text-to-Speech
Transcriber + Read Aloud + Grammarly-clone. 100% Offline.

Automatic transcription runs fully on your machine (Vosk offline engine +
ffmpeg audio extraction) — audio AND video files (MP4, MOV, MKV, WEBM…)
are supported. No cloud APIs, no API keys, no data ever leaves the machine.

v0.3.0 — Dark mode, accent themes, persistent settings, subtitle
export (SRT/VTT), grammar health score, find & replace, tools panel.
"""

import os
import re
import tempfile

import streamlit as st

from src.fed_tts.grammar_checker import GrammarChecker
from src.fed_tts.tts import get_tts_js
from src.fed_tts.auto_transcriber import (
    SUPPORTED_EXTENSIONS,
    AutoTranscriber,
    ffmpeg_available,
    is_supported_file,
    is_video_file,
)
from src.fed_tts.settings import ACCENTS, Settings
from src.fed_tts.ui import build_css, chips, health_ring, hero, stat_cards, subtitle_table

APP_TAGLINE = "Offline transcription, subtitles, grammar & read-aloud — in one workspace"
MEDIA_EXTS = sorted(SUPPORTED_EXTENSIONS)

# ---------------------------------------------------------------------
# Page config (must run before any other st call)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="FED TTS — Offline Transcription Studio",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Settings (persistent JSON, offline)
# ---------------------------------------------------------------------
SETTINGS_KEY = "fed_settings"
PENDING_NEW_TRANSCRIPT = "fed_pending_new_transcript"


def load_settings() -> Settings:
    if SETTINGS_KEY not in st.session_state:
        st.session_state[SETTINGS_KEY] = Settings.load()
    return st.session_state[SETTINGS_KEY]


def commit_settings(s: Settings) -> None:
    s.save()
    st.session_state[SETTINGS_KEY] = s


settings = load_settings()

# Sidebar: appearance controls ----------------------------------------
with st.sidebar:
    with st.expander("🎨 Appearance", expanded=True):
        theme_label = st.radio(
            "Theme",
            ["Dark", "Light", "Auto (follow OS)"],
            index=["dark", "light", "auto"].index(settings.theme),
            horizontal=True,
            help="Auto follows your operating system's dark mode.",
        )
        settings.theme = {"Dark": "dark", "Light": "light",
                          "Auto (follow OS)": "auto"}[theme_label]

        accent_label = st.selectbox(
            "Accent colour",
            list(ACCENTS.keys()),
            index=list(ACCENTS.keys()).index(settings.accent),
        )
        settings.accent = accent_label

        settings.font_scale = st.slider(
            "Font size", 0.85, 1.25, settings.font_scale, 0.05,
            help="Scales the whole interface (85% – 125%).",
            key="font_scale_w",
        )
        settings.rounded = st.checkbox("Rounded corners", settings.rounded)
        settings.mono_editor = st.checkbox("Monospace editor", settings.mono_editor)

    if st.button("💾 Save appearance", use_container_width=True):
        commit_settings(settings)
        st.rerun()

# Inject theme CSS before first content paint ---------------------------
st.markdown(f"<style>{build_css(settings)}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "auto_result" not in st.session_state:
    st.session_state.auto_result = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_check" not in st.session_state:
    st.session_state.last_check = None

# Apply a transcript update scheduled by set_transcript() on the previous
# run. This MUST run before any widgets are instantiated, otherwise
# Streamlit raises StreamlitWidgetAlreadyInstantiatedError.
if PENDING_NEW_TRANSCRIPT in st.session_state:
    _pending = st.session_state.pop(PENDING_NEW_TRANSCRIPT)
    st.session_state.transcript = _pending
    for _key in ("/manual_text", "main_text_no_upload", "auto_text_display"):
        st.session_state[_key] = _pending


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_transcriber() -> AutoTranscriber:
    return AutoTranscriber()


def push_history(source: str, transcription: str) -> None:
    """Remember a transcript snapshot (deduplicated, max 25)."""
    if not settings.history_enabled or not transcription.strip():
        return
    item = (source, transcription)
    history = st.session_state.history
    if not history or history[-1] != item:
        history.append(item)
        if len(history) > 25:
            history.pop(0)


def set_transcript(text: str, msg: str) -> None:
    """Schedule a transcript update for the *next* run (deferred write).

    Streamlit forbids writing a widget's session-state key after that
    widget has been instantiated during the same run, so we park the new
    text in a marker, log a history snapshot now, and apply the update at
    the top of the next run before any widgets exist.
    """
    push_history(msg, text)
    st.session_state[PENDING_NEW_TRANSCRIPT] = text
    st.toast(f"✅ {msg}")
    st.rerun()


def count_matches(text: str, find: str, regex: bool, case: bool) -> int:
    if regex:
        flags = 0 if case else re.IGNORECASE
        return len(re.findall(find, text, flags))
    if case:
        return text.count(find)
    return len(re.findall(re.escape(find), text, re.IGNORECASE))


def do_replace(text: str, find: str, replace: str, regex: bool, case: bool) -> str:
    if regex:
        flags = 0 if case else re.IGNORECASE
        return re.sub(find, replace, text, flags=flags)
    if case:
        return text.replace(find, replace)
    return re.sub(re.escape(find), replace, text, flags=re.IGNORECASE)


def sentence_case(text: str) -> str:
    def cap(m):
        return m.group(0).upper()

    text = re.sub(r"^\s*[a-z]", cap, text)
    text = re.sub(r"[.!?]\s+[a-z]", cap, text)
    return text


def grammar_health_score(n_words: int, misspelled, issues) -> int:
    """0-100 quality score (100 = no issues found)."""
    if n_words <= 1:
        return 100
    penalty = len(misspelled) * 4 + len(issues) * 6
    return max(0, 100 - int(penalty / n_words * 100))


# ---------------------------------------------------------------------
# Hero banner
# ---------------------------------------------------------------------
st.markdown(
    hero(
        "🎙️ FED TTS",
        APP_TAGLINE,
        pills=["100% Offline", "MP4 + Video", "No API keys"],
        ghost_pills=["Vosk engine", "SRT / VTT export", "Dark mode"],
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Upload & media
# ---------------------------------------------------------------------
ext_list = ", ".join(MEDIA_EXTS)
uploaded_file = st.file_uploader(
    "Upload Audio or Video File",
    type=MEDIA_EXTS,
    help=f"Supported: {ext_list}. MP4 and other video files are handled automatically.",
)

if uploaded_file:
    col_player, col_text = st.columns([1, 2])

    with col_player:
        st.markdown('<div class="fed-panel">', unsafe_allow_html=True)
        st.markdown("**🎧 Media Player**")
        if is_video_file(name := uploaded_file.name):
            st.video(uploaded_file)
        else:
            st.audio(uploaded_file)
        st.caption("Tip: Right-click the player to change playback speed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_text:
        tab_auto, tab_manual, tab_subs, tab_tools = st.tabs(
            ["🤖 Auto Transcribe", "✍️ Manual", "🎬 Subtitles", "🧰 Tools"]
        )

        # ================= AUTO TAB =================
        with tab_auto:
            st.markdown(
                "Transcribe this file **automatically** with the offline "
                "speech engine (Vosk). Runs 100% on your machine — the file "
                "is never uploaded anywhere."
            )

            if not ffmpeg_available():
                st.error(
                    "**ffmpeg is not installed.** Automatic transcription "
                    "needs ffmpeg to read the audio track. Install it with "
                    "`sudo apt install ffmpeg` (Linux), `brew install ffmpeg` "
                    "(macOS) or `winget install ffmpeg` (Windows), then "
                    "restart the app. You can still transcribe manually in "
                    "the next tab."
                )
            else:
                c1, c2 = st.columns([1, 1])
                with c1:
                    do_transcribe = st.button(
                        "🤖 Transcribe Automatically",
                        type="primary",
                        use_container_width=True,
                    )
                with c2:
                    ts_enabled = st.checkbox(
                        "Include [mm:ss] timestamps",
                        settings.timestamps,
                        help="Also adjustable in Settings.",
                    )
                    ts_interval = st.slider(
                        "Timestamp interval (s)",
                        2.0, 30.0, settings.timestamp_interval, 0.5,
                        help="How often to insert a marker / split a subtitle cue.",
                        key="ts_interval_w",
                    )

                if not is_supported_file(uploaded_file.name):
                    st.warning(
                        f"Unknown file type `{uploaded_file.name}` — ffmpeg "
                        "will try its best, but the format may not work."
                    )

                if do_transcribe:
                    try:
                        transcriber = get_transcriber()

                        if not transcriber.model_ready():
                            progress = st.progress(0.0, "Preparing speech model…")
                        else:
                            progress = st.progress(0.0, "Starting…")

                        def cb(frac, msg):
                            progress.progress(min(1.0, frac), msg)

                        transcriber.ensure_model(progress=cb)

                        ext = os.path.splitext(uploaded_file.name)[1] or ".bin"
                        suffix = f".{ext.lstrip('.')}" if not ext.startswith(".") else ext
                        with tempfile.NamedTemporaryFile(
                            suffix=suffix, delete=False
                        ) as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name

                        try:
                            result = transcriber.transcribe_file(tmp_path, progress=cb)
                        finally:
                            try:
                                os.remove(tmp_path)
                            except OSError:
                                pass

                        if result.text.strip():
                            new_text = (
                                result.with_timestamps(ts_interval)
                                if ts_enabled
                                else result.text
                            )
                            st.session_state.transcript = new_text
                            st.session_state["/manual_text"] = new_text
                            st.session_state["auto_transcript_display"] = new_text
                            st.session_state.auto_result = result
                            push_history(f"Auto — {uploaded_file.name}", new_text)
                            st.success(
                                f"✅ Transcribed **{result.word_count} words** "
                                f"from {result.duration_seconds:.1f}s of audio. "
                                "The transcript is below — edit it freely in "
                                "the Manual tab, then check grammar or read "
                                "it aloud."
                            )
                        else:
                            st.warning(
                                "No speech was detected in this file. If it "
                                "contains music or silence there is nothing "
                                "to transcribe — try the manual tab."
                            )
                    except Exception as e:  # noqa: BLE001
                        st.error(f"⚠️ Transcription failed: {e}")

            auto_text = st.session_state.get("auto_transcript_display", "")
            if auto_text:
                st.text_area(
                    "📝 Auto transcript (editable)",
                    value=auto_text,
                    height=220,
                    key="auto_text_display",
                )
                if st.session_state.get("auto_text_display", "") != auto_text:
                    edited = st.session_state["auto_text_display"]
                    st.session_state.transcript = edited
                    st.session_state["/manual_text"] = edited

            st.caption(
                "First run downloads a small offline speech model (~40 MB) "
                "once. After that everything works with no internet at all. "
                "Bigger models = better accuracy: see "
                "[alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)."
            )

        # ================= MANUAL TAB =================
        with tab_manual:
            st.caption("Type what you hear — your words stay 100% accurate.")
            st.session_state.transcript = st.text_area(
                "Write what you hear:",
                value=st.session_state.transcript,
                height=250,
                key="/manual_text",
                label_visibility="collapsed",
            )
            if st.button("⬇️ Copy auto-transcript here", use_container_width=True,
                         help="Re-show the last automatic transcript in this editor."):
                auto_text = st.session_state.get("auto_transcript_display", "")
                if auto_text:
                    set_transcript(auto_text, "Auto-transcript copied to Manual tab")
                else:
                    st.rerun()

        # ================= SUBTITLES TAB =================
        with tab_subs:
            st.markdown(
                "**🎬 Subtitle export** — burn-in ready SRT/VTT files "
                "generated from word timings."
            )
            result = st.session_state.get("auto_result")
            if result and result.words:
                cue_interval = st.slider(
                    "Cue length (seconds)", 2.0, 30.0,
                    float(settings.timestamp_interval), 0.5,
                    key="cue_len",
                )
                cues = result.cues(cue_interval)
                st.markdown(
                    subtitle_table(
                        [(result._fmt(c.start), c.text) for c in cues]
                    ),
                    unsafe_allow_html=True,
                )
                base = os.path.splitext(name)[0]
                d1, d2, d3 = st.columns(3)
                with d1:
                    st.download_button(
                        "💾 SRT", data=result.to_srt(cue_interval),
                        file_name=f"{base}.srt", mime="text/plain",
                        use_container_width=True,
                    )
                with d2:
                    st.download_button(
                        "💾 VTT", data=result.to_vtt(cue_interval),
                        file_name=f"{base}.vtt", mime="text/vtt",
                        use_container_width=True,
                    )
                with d3:
                    st.download_button(
                        "💾 TXT", data=st.session_state.transcript,
                        file_name=f"{base}_transcript.txt", mime="text/plain",
                        use_container_width=True,
                    )
            else:
                st.info(
                    "Run 🤖 Auto Transcribe first — subtitles are built from "
                    "the word timings of the last automatic transcription."
                )

        # ================= TOOLS TAB =================
        with tab_tools:
            st.markdown("**🧰 Transcript tools**")
            tcol1, tcol2 = st.columns(2)

            # ---- Find & Replace ----
            with tcol1:
                st.markdown("#### 🔎 Find & Replace")
                find_what = st.text_input("Find", key="fr_find")
                replace_with = st.text_input("Replace with", key="fr_replace")
                use_regex = st.checkbox("Regex mode", key="fr_regex")
                case_sensitive = st.checkbox("Case-sensitive", key="fr_case")
                if st.button("Replace all", use_container_width=True,
                             type="primary"):
                    if find_what:
                        try:
                            count = count_matches(
                                st.session_state.transcript, find_what,
                                use_regex, case_sensitive,
                            )
                            new_text = do_replace(
                                st.session_state.transcript, find_what,
                                replace_with, use_regex, case_sensitive,
                            )
                            set_transcript(
                                new_text,
                                f"Replaced {count} occurrence(s)",
                            )
                        except re.error as e:
                            st.error(f"Invalid regex: {e}")
                    else:
                        st.warning("Enter something to find.")

            # ---- Case conversion & cleanup ----
            with tcol2:
                st.markdown("#### 🔠 Case & Cleanup")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("UPPERCASE", use_container_width=True):
                        set_transcript(
                            st.session_state.transcript.upper(), "Upper-cased"
                        )
                with cc2:
                    if st.button("lowercase", use_container_width=True):
                        set_transcript(
                            st.session_state.transcript.lower(), "Lower-cased"
                        )
                if st.button("Trim extra spaces", use_container_width=True):
                    set_transcript(
                        re.sub(r"[ \t]+", " ",
                               st.session_state.transcript).strip(),
                        "Extra spaces trimmed",
                    )
                if st.button("Sentence case", use_container_width=True):
                    set_transcript(
                        sentence_case(st.session_state.transcript),
                        "Sentence-cased",
                    )

            # ---- History ----
            if settings.history_enabled:
                st.divider()
                st.markdown("#### 🕘 Transcript history (this session)")
                history = st.session_state.history
                if history:
                    for i, (src, text) in enumerate(reversed(history)):
                        cA, cB = st.columns([4, 1])
                        n = len(history) - i
                        with cA:
                            st.caption(f"{n}. {src} — {len(text.split())} words")
                            st.text(text[:140] + ("…" if len(text) > 140 else ""))
                        with cB:
                            if st.button("Restore", key=f"hist_restore_{i}",
                                         use_container_width=True):
                                set_transcript(text, f"Restored snapshot {n}")
                    if st.button("🗑️ Clear history"):
                        st.session_state.history = []
                        st.rerun()
                else:
                    st.caption(
                        "No snapshots yet — transcribe or edit text to "
                        "start collecting history."
                    )

else:
    # ---------------- No file uploaded: landing state ----------------
    st.markdown('<div class="fed-panel">', unsafe_allow_html=True)
    st.markdown(
        "**Get started** — upload an audio or VIDEO file (MP4 supported!) to "
        "transcribe it automatically, or just type text below to use the "
        "grammar checker and read-aloud features."
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.transcript = st.text_area(
        "Or type/paste text here:",
        value=st.session_state.transcript,
        height=200,
        key="main_text_no_upload",
    )


# ---------------------------------------------------------------------
# Grammar & Read Aloud panel
# ---------------------------------------------------------------------
st.markdown('<div class="fed-panel">', unsafe_allow_html=True)
col_check, col_read = st.columns(2)

with col_check:
    st.markdown("#### 🔍 Grammar & Spell Check (No AI)")
    if st.button("Check Spelling & Grammar", use_container_width=True):
        text = st.session_state.transcript
        if not text.strip():
            st.warning("Please type some text first.")
            st.session_state.last_check = None
        else:
            checker = GrammarChecker()
            st.session_state.last_check = checker.check(text)

with col_read:
    st.markdown("#### 🔊 Read Aloud (Native OS Voice)")
    read_text = st.text_area(
        "Text to speak:", value=st.session_state.transcript[:1000],
        height=100, key="read_text",
    )
    rc1, rc2 = st.columns(2)
    with rc1:
        speak_rate = st.select_slider(
            "Speed", options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
            value=float(settings.tts_rate), key="tts_rate_w",
        )
    with rc2:
        speak_pitch = st.select_slider(
            "Pitch", options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
            value=float(settings.tts_pitch), key="tts_pitch_w",
        )
    rc3, rc4 = st.columns(2)
    with rc3:
        if st.button("🗣️ Speak Now", use_container_width=True):
            if read_text.strip():
                js = get_tts_js(read_text, rate=speak_rate, pitch=speak_pitch)
                st.components.v1.html(js, height=0)
                st.success("🔊 Speaking via your OS!")
            else:
                st.warning("Please enter text to read.")
    with rc4:
        if st.button("⏹️ Stop", use_container_width=True):
            st.components.v1.html(
                "<script>window.speechSynthesis.cancel();</script>", height=0
            )

# Grammar check results display
if st.session_state.last_check:
    results = st.session_state.last_check
    misspelled, issues = results["misspelled"], results["issues"]
    n_words = max(1, len(st.session_state.transcript.split()))
    score = grammar_health_score(n_words, misspelled, issues)
    st.markdown(health_ring(score), unsafe_allow_html=True)
    if misspelled:
        st.warning(f"🟡 Potential typos ({len(misspelled)}): "
                   f"{', '.join(list(misspelled)[:15])}")
    else:
        st.success("✅ Spelling looks perfect!")
    if issues:
        for issue in issues:
            st.info(issue)
    else:
        if not misspelled:
            st.balloons()
            st.success("✨ Your text looks clear and professional!")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Stats strip
# ---------------------------------------------------------------------
word_count = len(st.session_state.transcript.split()) if st.session_state.transcript else 0
char_count = len(st.session_state.transcript) if st.session_state.transcript else 0
speak_time = round(word_count / 150 * 60)  # ~150 wpm
auto_wc = (st.session_state.auto_result.word_count
           if st.session_state.auto_result else None)
st.markdown(
    stat_cards([
        (f"{word_count}", "Words"),
        (f"{char_count}", "Characters"),
        (f"{auto_wc}" if auto_wc else "—", "Auto words"),
        (f"{speak_time // 60}m {speak_time % 60:02d}s", "Est. speak time"),
    ]),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Sidebar: engine info, stats, behaviour settings
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("### ⚙️ Transcription engine")
    model_ready = get_transcriber().model_ready()
    st.markdown(
        chips([
            (f"Vosk model {'ready' if model_ready else 'not loaded'}",
             True if model_ready else None),
            (f"ffmpeg {'detected' if ffmpeg_available() else 'missing'}",
             ffmpeg_available()),
        ]),
        unsafe_allow_html=True,
    )
    st.caption(
        "Offline [Vosk](https://alphacephei.com/vosk/) speech recognition + "
        "ffmpeg audio extraction. First transcription downloads the small "
        "English model once (~40 MB); then it works fully offline."
    )

    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Words", word_count)
    st.metric("Characters", char_count)

    with st.expander("🛠️ Transcription settings", expanded=False):
        settings.timestamps = st.checkbox(
            "Timestamps by default", settings.timestamps, key="st_ts_w")
        settings.timestamp_interval = st.slider(
            "Timestamp interval (s)", 2.0, 30.0,
            settings.timestamp_interval, 0.5, key="st_tsint_w")
        settings.tts_rate = st.select_slider(
            "Read-aloud speed", options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
            value=float(settings.tts_rate), key="st_rate_w")
        settings.tts_pitch = st.select_slider(
            "Read-aloud pitch", options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
            value=float(settings.tts_pitch), key="st_pitch_w")
        settings.history_enabled = st.checkbox(
            "Keep transcript history", settings.history_enabled,
            key="st_hist_w")
        if st.button("💾 Save settings", use_container_width=True):
            commit_settings(settings)
            st.rerun()

    st.markdown("---")
    st.markdown("### 💖 Support the Project")
    st.markdown(
        """
        <a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
            <img height='36' style='border:0px;height:36px;' src='https://ko-fi.com/img/githubbutton_sm.svg' border='0' alt='Buy Me a Coffee at ko-fi.com' />
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr style="margin:22px 0 8px 0;">', unsafe_allow_html=True)
st.caption("⚡ 100% Offline transcription (Vosk) + grammar checker + read aloud. "
           "No cloud APIs. Built with ❤️ using Streamlit.")
