"""
Text Generator Module - No AI, deterministic text generation.

This is the CORE feature of FED TTS: it extracts words from uploaded text
files (.txt, .csv, .md, .docx) and generates NEW text based on those words.

Two generation strategies are provided, both 100% deterministic (no neural
networks, no LLMs, no cloud):

1. Markov Chain Generator
   Learns which words tend to follow which other words (an N-gram transition
   model) from the uploaded files, then walks that chain to produce new
   sentences that mimic the style/structure of the source material.

2. Word-Pool (Mad-Libs) Generator
   Extracts every unique word from the uploaded files, classifies them
   loosely by simple heuristics (capitalised = "noun-like", ends in -ly =
   "adverb-like", etc.), and assembles random sentences from sentence
   templates filled with words drawn from the pool.

A word-frequency analyser is also provided so users can inspect the
vocabulary that was learned from their files.
"""

from __future__ import annotations

import csv as csv_module
import io
import random
import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Word extraction from uploaded files
# ---------------------------------------------------------------------------

# Supported text file extensions (case-insensitive)
TEXT_EXTENSIONS = {".txt", ".csv", ".md", ".markdown", ".docx", ".log", ".json", ".xml", ".tsv"}


def _read_docx(file_bytes: bytes) -> str:
    """Extract plain text from a .docx file using python-docx (optional dep)."""
    try:
        from docx import Document  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on optional dep
        raise ImportError(
            "python-docx is required to read .docx files. "
            "Install it with: pip install python-docx"
        ) from exc

    document = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in document.paragraphs if p.text]
    return "\n".join(paragraphs)


def _read_csv(file_bytes: bytes) -> str:
    """Extract text from a CSV file by joining all cell values."""
    text = file_bytes.decode("utf-8", errors="ignore")
    reader = csv_module.reader(io.StringIO(text))
    cells: List[str] = []
    for row in reader:
        cells.extend(str(cell) for cell in row if cell)
    return " ".join(cells)


def read_file_content(file_bytes: bytes, filename: str) -> str:
    """
    Read the plain-text content of an uploaded file based on its extension.

    Args:
        file_bytes: Raw bytes of the file.
        filename: Name of the file (used to detect the format).

    Returns:
        The plain-text content of the file as a string.

    Raises:
        ValueError: If the file type is unsupported.
        ImportError: If a required optional dependency is missing.
    """
    ext = _get_extension(filename)

    if ext == ".docx":
        return _read_docx(file_bytes)
    if ext == ".csv" or ext == ".tsv":
        return _read_csv(file_bytes)
    # .txt, .md, .markdown, .log, .json, .xml and anything else text-like
    return file_bytes.decode("utf-8", errors="ignore")


def _get_extension(filename: str) -> str:
    """Return the lowercased file extension including the leading dot."""
    dot = filename.rfind(".")
    if dot == -1:
        return ""
    return filename[dot:].lower()


def is_supported_text_file(filename: str) -> bool:
    """Return True if the filename has a supported text extension."""
    return _get_extension(filename) in TEXT_EXTENSIONS


# Regex that splits text into tokens (words) while keeping the separators we
# care about (sentence terminators). Punctuation other than sentence enders
# is stripped from individual words.
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
_SENTENCE_END_RE = re.compile(r"[.!?]+")


def tokenize(text: str) -> List[str]:
    """
    Split text into a list of word tokens (lower-cased, punctuation stripped).

    Contractions such as "don't" are kept as a single token ("don't").
    """
    return [match.group(0) for match in _TOKEN_RE.finditer(text)]


def tokenize_with_sentences(text: str) -> List[List[str]]:
    """
    Split text into sentences, then each sentence into word tokens.

    Returns a list of sentences, where each sentence is a list of tokens.
    """
    sentences: List[List[str]] = []
    for raw_sentence in _SENTENCE_END_RE.split(text):
        tokens = tokenize(raw_sentence)
        if tokens:
            sentences.append(tokens)
    return sentences


def extract_words(text: str) -> List[str]:
    """Return the list of all word tokens (with duplicates) in the text."""
    return tokenize(text)


def unique_words(text: str) -> List[str]:
    """Return the unique word tokens in the text, preserving first-seen order."""
    seen: set = set()
    ordered: List[str] = []
    for word in tokenize(text):
        if word not in seen:
            seen.add(word)
            ordered.append(word)
    return ordered


def word_frequencies(text: str, top_n: Optional[int] = None) -> List[Tuple[str, int]]:
    """
    Count how often each word appears in the text.

    Args:
        text: The text to analyse.
        top_n: If given, return only the N most common words.

    Returns:
        A list of (word, count) pairs sorted by count descending.
    """
    counter = Counter(tokenize(text))
    if top_n is None:
        return counter.most_common()
    return counter.most_common(top_n)


# ---------------------------------------------------------------------------
# Markov chain generator
# ---------------------------------------------------------------------------


class MarkovChain:
    """
    A simple N-gram Markov chain over words.

    Builds a transition table mapping a tuple of `order` previous words to a
    Counter of words that followed that context in the training text. New text
    is generated by walking the chain, picking the next word weighted by how
    often it appeared after the current context.

    This is a purely statistical, deterministic-when-seeded process: no AI,
    no neural networks, no cloud calls.
    """

    def __init__(self, order: int = 2):
        if order < 1:
            raise ValueError("Markov chain order must be >= 1")
        self.order = order
        # transitions[context_tuple] -> Counter(next_word -> count)
        self.transitions: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
        # All distinct sentence-start contexts, for seeding generation.
        self.starts: List[Tuple[str, ...]] = []
        self._trained = False

    def train(self, text: str) -> None:
        """Build the transition table from the given text."""
        sentences = tokenize_with_sentences(text)
        for sentence in sentences:
            if len(sentence) < self.order + 1:
                # Sentence too short for this order; still record it as a
                # possible start context if it has at least `order` tokens.
                if len(sentence) >= self.order:
                    self.starts.append(tuple(sentence[: self.order]))
                continue
            # Record the sentence start context.
            self.starts.append(tuple(sentence[: self.order]))
            # Slide a window over the sentence to build transitions.
            for i in range(len(sentence) - self.order):
                context = tuple(sentence[i : i + self.order])
                next_word = sentence[i + self.order]
                self.transitions[context][next_word] += 1
        self._trained = True

    def is_trained(self) -> bool:
        return self._trained and bool(self.transitions)

    def _pick_next(self, context: Tuple[str, ...], rng: random.Random) -> Optional[str]:
        """Pick a weighted-random next word for the given context."""
        options = self.transitions.get(context)
        if not options:
            return None
        words = list(options.keys())
        weights = list(options.values())
        return rng.choices(words, weights=weights, k=1)[0]

    def generate(
        self,
        max_words: int = 50,
        seed: Optional[str] = None,
        rng: Optional[random.Random] = None,
    ) -> str:
        """
        Generate new text by walking the Markov chain.

        Args:
            max_words: Maximum number of words to generate.
            seed: Optional starting word. If given (and present in the model),
                  generation begins from a context that starts with this word.
                  If None, a random sentence-start context is used.
            rng: Optional random.Random instance for reproducibility.

        Returns:
            A generated string of text.
        """
        if not self.is_trained():
            raise ValueError(
                "Markov chain has not been trained yet. Call train() first."
            )
        rng = rng or random.Random()

        context = self._choose_start_context(seed, rng)
        if context is None:
            # Could not find a context matching the seed; fall back to any.
            context = self._choose_start_context(None, rng)

        generated: List[str] = list(context)
        while len(generated) < max_words:
            next_word = self._pick_next(tuple(generated[-self.order :]), rng)
            if next_word is None:
                # Dead end: jump to a new random start context.
                new_start = self._choose_start_context(None, rng)
                if new_start is None:
                    break
                # End the current sentence, begin a new one.
                generated.append(".")
                generated.extend(new_start)
                continue
            generated.append(next_word)
        return self._format_output(generated[:max_words])

    def _choose_start_context(
        self, seed: Optional[str], rng: random.Random
    ) -> Optional[Tuple[str, ...]]:
        """Choose a starting context, optionally biased toward a seed word."""
        if not self.starts:
            # Fall back to any transition key.
            keys = list(self.transitions.keys())
            return rng.choice(keys) if keys else None
        if seed:
            seed_lower = seed.lower()
            matching = [s for s in self.starts if s[0].lower() == seed_lower]
            if matching:
                return rng.choice(matching)
            # Also try transitions whose first word matches the seed.
            matching_keys = [
                k for k in self.transitions.keys() if k[0].lower() == seed_lower
            ]
            if matching_keys:
                return rng.choice(matching_keys)
        return rng.choice(self.starts)

    @staticmethod
    def _format_output(words: List[str]) -> str:
        """Join generated words into a readable, capitalised string."""
        if not words:
            return ""
        text = " ".join(words)
        # Collapse a space before a sentence-ending period we inserted.
        text = re.sub(r"\s+\.", ".", text)
        # Capitalise the first letter.
        text = text[0].upper() + text[1:] if text else text
        # Ensure it ends with punctuation.
        if text and text[-1] not in ".!?":
            text += "."
        return text


# ---------------------------------------------------------------------------
# Word-pool (mad-libs style) generator
# ---------------------------------------------------------------------------


class WordPoolGenerator:
    """
    Generates random sentences from a pool of words extracted from uploaded
    files, using simple sentence templates filled with loosely-classified
    words.

    Classification is intentionally heuristic (no POS tagger / no AI):
      - nouns-ish: capitalised words or words not matching other categories
      - verbs-ish: words ending in -ed, -ing, or -s (excluding -ly/-ous)
      - adjectives-ish: words ending in -ful, -ous, -y, -ic, -al, -ive
      - adverbs-ish: words ending in -ly

    These rough buckets are enough to produce grammatical-ish random
    sentences that only use vocabulary drawn from the user's files.
    """

    TEMPLATES = [
        "The {adj} {noun} {verb} the {noun2}.",
        "A {noun} and a {noun2} {verb} {adv}.",
        "{noun} is very {adj}.",
        "The {adj} {noun} {verb} {adv} near the {noun2}.",
        "Every {noun} {verb} a {adj} {noun2}.",
        "The {noun} {verb} {adv}, while the {noun2} rests.",
        "A {adj} {adj2} {noun} appears.",
        "{noun} and {noun2} {verb} together {adv}.",
        "The {adj} {noun} sees a {adj2} {noun2}.",
        "{noun} {verb} {adv} into the {adj} {noun2}.",
    ]

    def __init__(self, text: str):
        self.words = tokenize(text)
        self.unique = list(dict.fromkeys(self.words))  # preserve order, unique
        self._classify()

    def _classify(self) -> None:
        self.nouns: List[str] = []
        self.verbs: List[str] = []
        self.adjectives: List[str] = []
        self.adverbs: List[str] = []
        seen: set = set()
        for word in self.unique:
            lw = word.lower()
            if word in seen:
                continue
            seen.add(word)
            if lw.endswith("ly") and len(lw) > 3:
                self.adverbs.append(word)
            elif lw.endswith(("ful", "ous", "ic", "ive", "al")) and len(lw) > 4:
                self.adjectives.append(word)
            elif lw.endswith(("ed", "ing")) and len(lw) > 4:
                self.verbs.append(word)
            elif lw.endswith("y") and len(lw) > 3 and not lw.endswith("ly"):
                self.adjectives.append(word)
            elif lw.endswith("s") and len(lw) > 4 and not lw.endswith("ss"):
                # plural/3rd-person -> treat as noun-ish / verb-ish
                self.nouns.append(word)
            else:
                self.nouns.append(word)
        # Fallbacks: if a category is empty, reuse the general noun pool so
        # generation never fails.
        self.nouns = self.nouns or self.unique
        self.verbs = self.verbs or self.unique
        self.adjectives = self.adjectives or self.nouns
        self.adverbs = self.adverbs or self.nouns

    def _pick(self, category: List[str], rng: random.Random) -> str:
        return rng.choice(category) if category else "something"

    def generate_sentence(self, rng: Optional[random.Random] = None) -> str:
        """Generate a single random sentence from the word pool."""
        rng = rng or random.Random()
        template = rng.choice(self.TEMPLATES)
        values = {
            "noun": self._pick(self.nouns, rng),
            "noun2": self._pick(self.nouns, rng),
            "verb": self._pick(self.verbs, rng),
            "adj": self._pick(self.adjectives, rng),
            "adj2": self._pick(self.adjectives, rng),
            "adv": self._pick(self.adverbs, rng),
        }
        # Avoid filling the same slot with the identical word twice in a row.
        for _ in range(5):
            if values["noun2"] != values["noun"]:
                break
            values["noun2"] = self._pick(self.nouns, rng)
        sentence = template.format(**values)
        return sentence[0].upper() + sentence[1:]

    def generate_paragraph(
        self, sentences: int = 4, rng: Optional[random.Random] = None
    ) -> str:
        """Generate a paragraph of `sentences` random sentences."""
        rng = rng or random.Random()
        return " ".join(
            self.generate_sentence(rng) for _ in range(max(1, sentences))
        )


# ---------------------------------------------------------------------------
# High-level convenience facade
# ---------------------------------------------------------------------------


class TextGenerator:
    """
    High-level facade that combines file reading, word extraction and the two
    generation strategies into one easy-to-use object for the Streamlit app.

    Usage:
        gen = TextGenerator()
        gen.add_file(file_bytes, "notes.txt")
        gen.add_file(file_bytes2, "journal.docx")
        markov_text = gen.generate_markov(max_words=60, seed="the")
        random_text = gen.generate_random(sentences=5)
        freq = gen.frequency(top_n=20)
    """

    def __init__(self, order: int = 2):
        self.order = order
        self._text_buffer: List[str] = []
        self._filenames: List[str] = []
        self._markov: Optional[MarkovChain] = None
        self._pool: Optional[WordPoolGenerator] = None
        self._dirty = True

    # -- file ingestion ----------------------------------------------------

    def add_file(self, file_bytes: bytes, filename: str) -> str:
        """
        Read an uploaded file and append its text to the corpus.

        Returns the extracted text so the caller can inspect/preview it.
        """
        content = read_file_content(file_bytes, filename)
        self._text_buffer.append(content)
        self._filenames.append(filename)
        self._dirty = True
        return content

    def add_text(self, text: str, source: str = "manual") -> None:
        """Append raw text directly to the corpus."""
        self._text_buffer.append(text)
        self._filenames.append(source)
        self._dirty = True

    def clear(self) -> None:
        """Remove all ingested text."""
        self._text_buffer = []
        self._filenames = []
        self._markov = None
        self._pool = None
        self._dirty = True

    # -- accessors ---------------------------------------------------------

    @property
    def filenames(self) -> List[str]:
        return list(self._filenames)

    def combined_text(self) -> str:
        return "\n\n".join(self._text_buffer)

    def has_text(self) -> bool:
        return any(t.strip() for t in self._text_buffer)

    def word_count(self) -> int:
        return len(tokenize(self.combined_text()))

    def unique_word_count(self) -> int:
        return len(set(tokenize(self.combined_text())))

    def frequency(self, top_n: Optional[int] = 20) -> List[Tuple[str, int]]:
        return word_frequencies(self.combined_text(), top_n=top_n)

    def all_unique_words(self) -> List[str]:
        return unique_words(self.combined_text())

    # -- lazy model builders ----------------------------------------------

    def _ensure_models(self) -> None:
        if not self._dirty and self._markov is not None and self._pool is not None:
            return
        text = self.combined_text()
        self._markov = MarkovChain(order=self.order)
        self._markov.train(text)
        self._pool = WordPoolGenerator(text)
        self._dirty = False

    # -- generation --------------------------------------------------------

    def generate_markov(
        self,
        max_words: int = 50,
        seed: Optional[str] = None,
        rng: Optional[random.Random] = None,
    ) -> str:
        """Generate text using the Markov chain (mimics source style)."""
        self._ensure_models()
        assert self._markov is not None
        if not self._markov.is_trained():
            return ""
        return self._markov.generate(max_words=max_words, seed=seed, rng=rng)

    def generate_random(
        self,
        sentences: int = 4,
        rng: Optional[random.Random] = None,
    ) -> str:
        """Generate text using the word-pool / mad-libs generator."""
        self._ensure_models()
        assert self._pool is not None
        return self._pool.generate_paragraph(sentences=sentences, rng=rng)

    def markov_ready(self) -> bool:
        """Return True if there is enough text to build a Markov model."""
        return self.word_count() >= self.order + 1
