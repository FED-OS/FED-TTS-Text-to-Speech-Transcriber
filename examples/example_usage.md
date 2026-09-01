# FED TTS — Example Usage

This document provides practical examples of using FED TTS in different scenarios.

## Example 1: Basic Grammar Check

Using the `GrammarChecker` class to check text for spelling and grammar issues.

```python
from fed_tts.grammar_checker import GrammarChecker

# Initialize the checker
checker = GrammarChecker()

# Text to check
text = """
The team would of finished the project sooner, but their was alot of 
unforseen issues. We should of planned better. Its a lesson learned for 
next time.
"""

# Run the full check
results = checker.check(text)

print(f"Total issues found: {results['total_issues']}")
print()

# Display spelling issues
print("=== Spelling Issues ===")
for issue in results['spelling']:
    print(f"  Word: {issue['word']}")
    print(f"  Suggestions: {', '.join(issue['suggestions'][:3])}")
    print()

# Display grammar issues
print("=== Grammar Issues ===")
for issue in results['grammar']:
    print(f"  Rule: {issue['rule']}")
    print(f"  Message: {issue['message']}")
    print(f"  Suggestion: {issue['suggestion']}")
    print()
```

**Expected Output:**
```
Total issues found: 6

=== Spelling Issues ===
  Word: unforseen
  Suggestions: unforeseen, forearm, foresee

=== Grammar Issues ===
  Rule: would_of
  Message: 'would of' is incorrect. Use 'would have' instead.
  Suggestion: would have

  Rule: their_is
  Message: 'their is' is incorrect. Use 'there is' instead.
  Suggestion: there is

  Rule: alot
  Message: 'alot' is not a word. Use 'a lot' instead.
  Suggestion: a lot

  Rule: should_of
  Message: 'should of' is incorrect. Use 'should have' instead.
  Suggestion: should have
```

---

## Example 2: Spell Check Only

```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()

text = "The recepcionist was very helpfull and accomodating."
spelling_issues = checker.check_spelling(text)

for issue in spelling_issues:
    word = issue['word']
    suggestions = issue['suggestions']
    print(f"Misspelled: '{word}' → Try: {', '.join(suggestions[:5])}")
```

**Expected Output:**
```
Misspelled: 'recepcionist' → Try: receptionist, receptionists, refectionist
Misspelled: 'helpfull' → Try: helpful, helpfully, helpfully
Misspelled: 'accomodating' → Try: accommodating, accommodatingly, communication
```

---

## Example 3: Grammar Check Only

```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()

text = "I could of done better. Their is no excuse. Your welcome to try again."
grammar_issues = checker.check_grammar(text)

for issue in grammar_issues:
    print(f"[{issue['rule']}] {issue['message']}")
    print(f"  → Suggestion: {issue['suggestion']}")
    print()
```

**Expected Output:**
```
[could_of] 'could of' is incorrect. Use 'could have' instead.
  → Suggestion: could have

[their_is] 'their is' is incorrect. Use 'there is' instead.
  → Suggestion: there is

[your_welcome] 'your welcome' is incorrect. Use "you're welcome" instead.
  → Suggestion: you're welcome
```

---

## Example 4: Text-to-Speech in Streamlit

```python
import streamlit as st
from fed_tts.tts import get_tts_js, get_stop_js

st.title("Read Aloud Demo")

text = st.text_area("Enter text to read aloud:", height=200)

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Read Aloud", type="primary"):
        if text.strip():
            js = get_tts_js(text, rate=1.0, pitch=1.0, volume=1.0)
            st.components.v1.html(js, height=0)
        else:
            st.warning("Please enter some text first.")

with col2:
    if st.button("⏹️ Stop"):
        st.components.v1.html(get_stop_js(), height=0)
```

---

## Example 5: Custom Audio Player

```python
import streamlit as st
from fed_tts.transcriber import audio_to_data_uri, get_custom_audio_player_js

st.title("Audio Player Demo")

uploaded = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

if uploaded is not None:
    # Determine MIME type
    mime_map = {
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "m4a": "audio/mp4",
        "flac": "audio/flac",
        "ogg": "audio/ogg",
    }
    ext = uploaded.name.split(".")[-1].lower()
    mime = mime_map.get(ext, "audio/wav")
    
    # Convert to data URI
    data_uri = audio_to_data_uri(uploaded.getvalue(), mime)
    
    # Render custom player
    player_js = get_custom_audio_player_js()
    html = f"""
    <audio id="audioPlayer" src="{data_uri}" controls></audio>
    <script>{player_js}</script>
    """
    st.components.v1.html(html, height=100)
```

---

## Example 6: Complete Transcription Workflow

```python
import streamlit as st
from fed_tts.grammar_checker import GrammarChecker
from fed_tts.tts import get_tts_js, get_stop_js
from fed_tts.transcriber import audio_to_data_uri

st.title("FED TTS — Transcription Workflow")

# Initialize session state
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# Step 1: Upload audio
uploaded = st.file_uploader("1. Upload audio file", type=["mp3", "wav", "m4a"])

if uploaded is not None:
    mime = f"audio/{uploaded.name.split('.')[-1]}"
    data_uri = audio_to_data_uri(uploaded.getvalue(), mime)
    st.components.v1.html(
        f'<audio controls src="{data_uri}"></audio>',
        height=50
    )

# Step 2: Transcribe
st.subheader("2. Transcribe")
transcript = st.text_area(
    "Transcription",
    value=st.session_state.transcript,
    height=200,
    key="transcript_input"
)
st.session_state.transcript = transcript

# Word count
words = len(transcript.split())
chars = len(transcript)
st.caption(f"Words: {words} | Characters: {chars}")

# Step 3: Check grammar
st.subheader("3. Check Grammar")
if st.button("Check Grammar & Spelling"):
    checker = GrammarChecker()
    results = checker.check(transcript)
    
    st.write(f"**Total issues: {results['total_issues']}**")
    
    if results['spelling']:
        st.write("**Spelling Issues:**")
        for issue in results['spelling']:
            st.write(f"- `{issue['word']}` → {', '.join(issue['suggestions'][:3])}")
    
    if results['grammar']:
        st.write("**Grammar Issues:**")
        for issue in results['grammar']:
            st.write(f"- {issue['message']} → *{issue['suggestion']}*")
    
    if not results['spelling'] and not results['grammar']:
        st.success("No issues found!")

# Step 4: Read aloud
st.subheader("4. Read Aloud")
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Read Aloud"):
        if transcript.strip():
            st.components.v1.html(get_tts_js(transcript), height=0)
with col2:
    if st.button("⏹️ Stop"):
        st.components.v1.html(get_stop_js(), height=0)
```

---

## Example 7: Adding Custom Grammar Rules

```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()

# Add a custom rule
checker.grammar_rules.append({
    "name": "irregardless",
    "pattern": r"\birregardless\b",
    "message": "'irregardless' is not standard English. Use 'regardless' instead.",
    "suggestion": "regardless",
})

# Add another custom rule
checker.grammar_rules.append({
    "name": "supposed_to",
    "pattern": r"\bsuppose to\b",
    "message": "'suppose to' is incorrect. Use 'supposed to' instead.",
    "suggestion": "supposed to",
})

# Test with the new rules
text = "I am suppose to go, but irregardless of that, I will try."
results = checker.check_grammar(text)

for issue in results:
    print(f"[{issue['rule']}] {issue['message']}")
```

**Expected Output:**
```
[supposed_to] 'suppose to' is incorrect. Use 'supposed to' instead.
[irregardless] 'irregardless' is not standard English. Use 'regardless' instead.
```

---

## Example 8: Using as a Python Library

FED TTS can be used as a standalone library without Streamlit:

```python
from fed_tts.grammar_checker import GrammarChecker
from fed_tts.transcriber import get_timestamp

# Grammar checking as a library
checker = GrammarChecker()

# Check a batch of texts
texts = [
    "I would of gone to the store.",
    "Their is a problem with this sentence.",
    "This sentence is perfectly fine.",
    "We could of done better.",
]

for text in texts:
    results = checker.check(text)
    print(f"[{get_timestamp()}] Text: {text}")
    print(f"  Issues: {results['total_issues']}")
    for issue in results['grammar']:
        print(f"  - {issue['rule']}: {issue['suggestion']}")
    print()
```

---

## No AI Reminder

All examples above use **deterministic algorithms only**:

- Spell checking uses dictionary-based lookup (pyspellchecker)
- Grammar checking uses regex pattern matching
- Text-to-speech uses the browser's native SpeechSynthesis API
- No neural networks, cloud APIs, or LLMs are used

This is the core philosophy of FED TTS — powerful tools that respect your
privacy and work completely offline.
