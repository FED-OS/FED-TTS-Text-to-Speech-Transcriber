"""
FED TTS - Fluid Enhanced Dynamic Text Generator
================================================

Generate text based on the words in your uploaded files.

Upload one or more text files (.txt, .csv, .md, .docx, .log, .json, .xml),
and FED TTS will extract the words from them and generate NEW text that is
built from — and inspired by — your own vocabulary.

Two generation modes are available, both 100% deterministic (No AI):
  1. Markov Chain  - learns which words follow which, then walks the chain
                     to produce text that mimics the style of your files.
  2. Random Pool   - assembles sentences from your words using templates
                     (mad-libs style).

The classic tools remain available too:
  - Grammar & Spell Check on any generated or pasted text
  - Read Aloud (native OS voice via the browser SpeechSynthesis API)

Everything runs locally. No data leaves your machine. No neural networks.
"""

import random

import streamlit as st

from src.fed_tts.text_generator import (
    TEXT_EXTENSIONS,
    TextGenerator,
    is_supported_text_file,
)
from src.fed_tts.grammar_checker import GrammarChecker
from src.fed_tts.tts import get_tts_js, get_stop_js

st.set_page_config(page_title="FED TTS - Text Generator", layout="wide")

# Load custom CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "generator" not in st.session_state:
    st.session_state.generator = TextGenerator(order=2)
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "last_file_count" not in st.session_state:
    st.session_state.last_file_count = 0

gen: TextGenerator = st.session_state.generator

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🎙️ FED TTS - Generate Text From Your Files")
st.caption(
    "⚡ Upload text files → extract their words → generate new text built "
    "from your vocabulary. 100% Offline. No AI. No Cloud."
)

st.markdown(
    "Upload one or more **text files** and FED TTS will read the words inside "
    "them, then generate **new text** based on those words. Choose between a "
    "**Markov chain** (mimics the style of your files) or a **random "
    "word-pool** generator (mad-libs style)."
)

# ---------------------------------------------------------------------------
# Step 1: Upload text files
# ---------------------------------------------------------------------------
st.divider()
st.header("📂 Step 1 — Upload Your Text Files")

ext_list = ", ".join(sorted(TEXT_EXTENSIONS))
uploaded_files = st.file_uploader(
    f"Upload text files ({ext_list})",
    type=[ext.lstrip(".") for ext in sorted(TEXT_EXTENSIONS)],
    accept_multiple_files=True,
    help="The words inside these files become the vocabulary used to generate new text.",
)

# Process any newly uploaded files
if uploaded_files:
    current_names = {f.name for f in uploaded_files}
    already_loaded = set(gen.filenames)
    new_files = [f for f in uploaded_files if f.name not in already_loaded]

    if new_files:
        with st.spinner("Reading words from your files…"):
            for f in new_files:
                try:
                    gen.add_file(f.getvalue(), f.name)
                except ImportError as e:
                    st.error(f"⚠️ Could not read `{f.name}`: {e}")
                except Exception as e:  # noqa: BLE001
                    st.error(f"⚠️ Error reading `{f.name}`: {e}")
        st.success(
            f"✅ Loaded {len(new_files)} file(s). "
            f"Total files in corpus: {len(gen.filenames)}."
        )
    elif len(uploaded_files) != st.session_state.last_file_count:
        st.info(f"📋 Corpus currently holds {len(gen.filenames)} file(s).")

    st.session_state.last_file_count = len(uploaded_files)

# Manage the corpus
if gen.filenames:
    st.caption(f"**Files in corpus ({len(gen.filenames)}):** " + ", ".join(gen.filenames))
    c_clear, _ = st.columns([1, 4])
    with c_clear:
        if st.button("🗑️ Clear Corpus", help="Remove all uploaded files and start over"):
            gen.clear()
            st.session_state.generated_text = ""
            st.session_state.last_file_count = 0
            st.rerun()

# ---------------------------------------------------------------------------
# Step 2: Inspect the extracted words
# ---------------------------------------------------------------------------
if gen.has_text():
    st.divider()
    st.header("🔍 Step 2 — Words Extracted From Your Files")

    m_total, m_unique, m_files = st.columns(3)
    m_total.metric("Total Words", gen.word_count())
    m_unique.metric("Unique Words", gen.unique_word_count())
    m_files.metric("Files", len(gen.filenames))

    with st.expander("Show word frequency analysis (top 30)"):
        freq = gen.frequency(top_n=30)
        if freq:
            freq_cols = st.columns(3)
            for i, (word, count) in enumerate(freq):
                freq_cols[i % 3].markdown(f"`{word}` — **{count}**")

    with st.expander("Show all unique words"):
        words = gen.all_unique_words()
        st.caption(f"{len(words)} unique words extracted.")
        st.write(", ".join(words))

# ---------------------------------------------------------------------------
# Step 3: Generate text
# ---------------------------------------------------------------------------
if gen.has_text():
    st.divider()
    st.header("✨ Step 3 — Generate Text")

    gen_col, opts_col = st.columns([3, 2])

    with opts_col:
        st.subheader("Generation Options")
        mode = st.radio(
            "Generation mode",
            ["Markov Chain (style mimic)", "Random Word Pool (mad-libs)"],
            help=(
                "Markov Chain learns which words follow which in your files and "
                "produces text that imitates their style. Random Word Pool builds "
                "sentences from your words using templates."
            ),
        )
        is_markov = mode.startswith("Markov")

        if is_markov:
            max_words = st.slider(
                "Max words to generate", min_value=10, max_value=300, value=60, step=10
            )
            order = st.slider(
                "Markov order (context length)",
                min_value=1,
                max_value=4,
                value=2,
                step=1,
                help="Higher order = closer to original text but less variety.",
            )
            seed_word = st.text_input(
                "Starting word (optional)",
                value="",
                help="Begin the generated text with this word if it exists in your files.",
            )
        else:
            num_sentences = st.slider(
                "Sentences to generate", min_value=1, max_value=20, value=5, step=1
            )

        seed_value = st.number_input(
            "Random seed (for reproducibility)",
            min_value=0,
            value=42,
            step=1,
            help="Same seed + same options = same output. Change it for variety.",
        )

    with gen_col:
        st.subheader("Generated Text")
        if st.button("🎲 Generate Text", type="primary", use_container_width=True):
            rng = random.Random(int(seed_value))
            # (Re)build the Markov chain at the requested order if it changed.
            if is_markov and gen.order != order:
                gen.order = order
                gen._dirty = True
            try:
                if is_markov:
                    if not gen.markov_ready():
                        st.warning(
                            "Not enough words for this Markov order. "
                            "Upload more text or lower the order."
                        )
                    else:
                        seed = seed_word.strip() or None
                        result = gen.generate_markov(
                            max_words=max_words, seed=seed, rng=rng
                        )
                        st.session_state.generated_text = result
                else:
                    result = gen.generate_random(
                        sentences=num_sentences, rng=rng
                    )
                    st.session_state.generated_text = result
            except Exception as e:  # noqa: BLE001
                st.error(f"⚠️ Generation error: {e}")

        if st.session_state.generated_text:
            st.text_area(
                "Generated output",
                value=st.session_state.generated_text,
                height=220,
                key="generated_output",
            )
            # Download button
            st.download_button(
                "💾 Download as .txt",
                data=st.session_state.generated_text,
                file_name="fed_tts_generated.txt",
                mime="text/plain",
            )
        else:
            st.info("👆 Click **Generate Text** to create new text from your files.")

# ---------------------------------------------------------------------------
# Step 4: Grammar check + Read aloud (work on generated OR pasted text)
# ---------------------------------------------------------------------------
st.divider()
st.header("🛠️ Step 4 — Polish & Read Aloud")

# The working text defaults to the generated text but can be edited.
default_text = st.session_state.generated_text
working_text = st.text_area(
    "Text to check & read (auto-filled with generated text — edit freely):",
    value=default_text,
    height=160,
    key="working_text",
)

check_col, read_col = st.columns(2)

with check_col:
    st.subheader("🔍 Grammar & Spell Check")
    if st.button("Check Spelling & Grammar", use_container_width=True):
        if not working_text.strip():
            st.warning("Please enter some text first.")
        else:
            checker = GrammarChecker()
            results = checker.check(working_text)
            if results["misspelled"]:
                miss = list(results["misspelled"])[:20]
                st.warning(f"🟡 Potential typos: {', '.join(miss)}")
            else:
                st.success("✅ Spelling looks perfect!")
            if results["issues"]:
                for issue in results["issues"]:
                    st.info(issue)
            elif not results["misspelled"]:
                st.balloons()
                st.success("✨ Your text looks clear and professional!")

with read_col:
    st.subheader("🔊 Read Aloud (Native OS Voice)")
    rate = st.slider("Speech rate", 0.5, 2.0, 1.0, 0.1)
    rc1, rc2 = st.columns(2)
    with rc1:
        if st.button("🗣️ Speak", use_container_width=True):
            if working_text.strip():
                js = get_tts_js(working_text, rate=rate)
                st.components.v1.html(js, height=0)
                st.success("🔊 Speaking via your OS!")
            else:
                st.warning("Please enter text to read.")
    with rc2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.components.v1.html(get_stop_js(), height=0)

st.divider()
st.caption("⚡ 100% Offline. No AI. No Cloud APIs. Built with ❤️ using Streamlit.")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📊 Corpus Stats")
    st.metric("Files Loaded", len(gen.filenames))
    st.metric("Total Words", gen.word_count() if gen.has_text() else 0)
    st.metric("Unique Words", gen.unique_word_count() if gen.has_text() else 0)
    if gen.has_text():
        st.markdown("---")
        st.markdown("### Top 10 Words")
        for word, count in gen.frequency(top_n=10):
            st.markdown(f"- `{word}` — **{count}**")

    st.markdown("---")
    st.markdown("## 💖 Support the Project")
    st.markdown(
        """
        <a href='https://ko-fi.com/fedpromptly' target='_blank'>
            <img height='36' style='border:0px;height:36px;'
            src='https://ko-fi.com/img/githubbutton_sm.svg' border='0'
            alt='Buy Me a Coffee at ko-fi.com' />
        </a>
        """,
        unsafe_allow_html=True,
    )
