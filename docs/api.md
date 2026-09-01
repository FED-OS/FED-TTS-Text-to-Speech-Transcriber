# API Reference

This document provides a complete reference for the FED TTS Python API.

## Module: `fed_tts`

### Package Information

```python
import fed_tts
print(fed_tts.__version__)  # "0.1.0"
```

---

## Module: `fed_tts.grammar_checker`

### `GrammarChecker`

The `GrammarChecker` class provides deterministic spell checking and grammar
rule validation using dictionary-based and regex-based methods.

#### Constructor

```python
GrammarChecker()
```

Creates a new `GrammarChecker` instance. Initializes the `pyspellchecker`
dictionary for spell checking and loads the built-in grammar rules.

#### Methods

##### `check_spelling(text: str) -> list[dict]`

Checks the input text for misspelled words using a dictionary-based approach.

**Parameters:**
- `text` (`str`): The text to check for spelling errors.

**Returns:**
- `list[dict]`: A list of dictionaries, each containing:
  - `word` (`str`): The misspelled word
  - `suggestions` (`list[str]`): Suggested corrections
  - `context` (`str`): The surrounding text context

**Example:**
```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()
results = checker.check_spelling("This is a spelinge error in the sentense.")
for result in results:
    print(f"Misspelled: {result['word']}")
    print(f"Suggestions: {result['suggestions']}")
```

##### `check_grammar(text: str) -> list[dict]`

Checks the input text against built-in grammar rules using regex pattern matching.

**Parameters:**
- `text` (`str`): The text to check for grammar issues.

**Returns:**
- `list[dict]`: A list of dictionaries, each containing:
  - `rule` (`str`): The name of the grammar rule that was violated
  - `message` (`str`): A human-readable description of the issue
  - `match` (`str`): The text that matched the rule
  - `suggestion` (`str`): Suggested correction
  - `position` (`tuple[int, int]`): Start and end position of the match

**Built-in Grammar Rules:**
| Rule | Pattern | Example | Suggestion |
|------|---------|---------|------------|
| would_of | `would of` | "I would of gone" | "would have" |
| could_of | `could of` | "I could of done it" | "could have" |
| should_of | `should of` | "I should of known" | "should have" |
| must_of | `must of` | "It must of been" | "must have" |
| alot | `a lot` (written as "alot") | "I like it alot" | "a lot" |
| their_is | `their is` | "Their is a problem" | "There is" |
| your_welcome | `your welcome` | "Your welcome" | "You're welcome" |
| its_a | `its a` (ambiguous) | "Its a good idea" | "It's a" |
| double_space | `  ` (two+ spaces) | "Hello  world" | "Hello world" |
| passive_voice | `\b(is|was|were|are|been) \w+ed\b` | "was completed" | Active voice |
| long_sentence | sentences > 25 words | (long sentence) | Split into shorter sentences |
| repeated_words | `\b(\w+) \1\b` | "the the" | Remove duplicate |
| capitalization | sentence start lowercase | "this is wrong." | Capitalize first letter |

**Example:**
```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()
results = checker.check_grammar("I would of gone to the store.")
for result in results:
    print(f"Rule: {result['rule']}")
    print(f"Issue: {result['message']}")
    print(f"Suggestion: {result['suggestion']}")
```

##### `check(text: str) -> dict`

Runs both spell checking and grammar checking on the input text and returns a
combined result.

**Parameters:**
- `text` (`str`): The text to check.

**Returns:**
- `dict`: A dictionary containing:
  - `spelling` (`list[dict]`): Results from `check_spelling()`
  - `grammar` (`list[dict]`): Results from `check_grammar()`
  - `total_issues` (`int`): Total number of issues found

**Example:**
```python
from fed_tts.grammar_checker import GrammarChecker

checker = GrammarChecker()
results = checker.check("I would of gone, but I had a spelinge error.")
print(f"Total issues: {results['total_issues']}")
print(f"Spelling issues: {len(results['spelling'])}")
print(f"Grammar issues: {len(results['grammar'])}")
```

#### Attributes

##### `grammar_rules: list[dict]`

A list of grammar rule definitions, each containing:
- `name` (`str`): Rule identifier
- `pattern` (`str`): Regex pattern string
- `message` (`str`): Description of the issue
- `suggestion` (`str`): Suggested fix

##### `spell: SpellChecker`

The internal `pyspellchecker.SpellChecker` instance used for spell checking.

---

## Module: `fed_tts.tts`

### Functions

##### `get_tts_js(text: str, rate: float = 1.0, pitch: float = 1.0, volume: float = 1.0) -> str`

Generates JavaScript code that uses the browser's native `SpeechSynthesis` API
to read text aloud. This is completely offline and uses the operating system's
built-in voices.

**Parameters:**
- `text` (`str`): The text to be read aloud.
- `rate` (`float`, optional): Speech rate. Default `1.0`. Range: `0.1` to `10.0`.
- `pitch` (`float`, optional): Speech pitch. Default `1.0`. Range: `0` to `2.0`.
- `volume` (`float`, optional): Speech volume. Default `1.0`. Range: `0` to `1.0`.

**Returns:**
- `str`: JavaScript code string to be rendered via `st.components.v1.html()`.

**Example:**
```python
import streamlit as st
from fed_tts.tts import get_tts_js

js = get_tts_js("Hello, world!", rate=1.0, pitch=1.0, volume=1.0)
st.components.v1.html(js, height=0)
```

##### `get_voices_js() -> str`

Generates JavaScript code that lists all available system voices for the
browser's `SpeechSynthesis` API.

**Returns:**
- `str`: JavaScript code that populates the voices list.

##### `get_stop_js() -> str`

Generates JavaScript code that stops any currently playing speech synthesis.

**Returns:**
- `str`: JavaScript code to stop speech.

**Example:**
```python
import streamlit as st
from fed_tts.tts import get_stop_js

if st.button("Stop Reading"):
    st.components.v1.html(get_stop_js(), height=0)
```

---

## Module: `fed_tts.transcriber`

### Functions

##### `audio_to_data_uri(audio_bytes: bytes, mime_type: str = "audio/wav") -> str`

Converts raw audio bytes to a base64-encoded data URI for embedding in HTML.

**Parameters:**
- `audio_bytes` (`bytes`): The raw audio file bytes.
- `mime_type` (`str`, optional): The MIME type of the audio. Default `"audio/wav"`.

**Returns:**
- `str`: A base64-encoded data URI string.

**Example:**
```python
from fed_tts.transcriber import audio_to_data_uri

with open("audio.wav", "rb") as f:
    audio_bytes = f.read()

data_uri = audio_to_data_uri(audio_bytes, "audio/wav")
# Use in HTML: <audio src="data_uri"></audio>
```

##### `get_custom_audio_player_js() -> str`

Generates JavaScript code for a custom HTML5 audio player with rewind,
fast-forward, and speed control buttons.

**Returns:**
- `str`: JavaScript code for the custom audio player.

##### `get_timestamp() -> str`

Returns the current timestamp as a formatted string.

**Returns:**
- `str`: Timestamp in `YYYY-MM-DD HH:MM:SS` format.

**Example:**
```python
from fed_tts.transcriber import get_timestamp

print(get_timestamp())  # "2025-01-15 14:30:22"
```

---

## Error Handling

All FED TTS functions are designed to be robust and handle edge cases gracefully:

- **Empty text**: Spell checking and grammar checking return empty lists for
  empty or whitespace-only text.
- **None input**: Functions raise `TypeError` for `None` input.
- **Invalid audio**: `audio_to_data_uri` handles empty bytes gracefully.
- **Browser TTS**: If the browser doesn't support `SpeechSynthesis`, the
  JavaScript includes a fallback message.

---

## No AI Guarantee

All functions in the FED TTS API use **deterministic algorithms only**:

- **Spell checking**: Dictionary-based lookup via `pyspellchecker`
- **Grammar checking**: Regex pattern matching against rule definitions
- **Text-to-Speech**: Browser's native `SpeechSynthesis` API (OS voices)
- **Transcription**: Manual human input (no automatic transcription)

No neural networks, no machine learning models, no cloud APIs, and no LLMs are
used anywhere in the FED TTS codebase.
