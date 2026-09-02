"""Test the text generator module (No AI, deterministic)."""

import random

import pytest

from src.fed_tts.text_generator import (
    MarkovChain,
    TextGenerator,
    WordPoolGenerator,
    extract_words,
    is_supported_text_file,
    read_file_content,
    tokenize,
    tokenize_with_sentences,
    unique_words,
    word_frequencies,
)


SAMPLE = (
    "The quick brown fox jumps over the lazy dog. "
    "The lazy dog sleeps quietly while the fox runs. "
    "A quick fox is a happy fox. The dog is calm and slow."
)


# ---------------------------------------------------------------------------
# Tokenisation
# ---------------------------------------------------------------------------


class TestTokenize:
    def test_basic_tokenize(self):
        assert tokenize("Hello world") == ["Hello", "world"]

    def test_strips_punctuation(self):
        assert tokenize("Hello, world!") == ["Hello", "world"]

    def test_keeps_contractions(self):
        assert tokenize("don't stop") == ["don't", "stop"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_numbers_kept(self):
        assert tokenize("I have 42 cats") == ["I", "have", "42", "cats"]


class TestSentences:
    def test_split_sentences(self):
        sents = tokenize_with_sentences("Hello world. Bye now!")
        assert len(sents) == 2
        assert sents[0] == ["Hello", "world"]
        assert sents[1] == ["Bye", "now"]

    def test_no_terminator(self):
        sents = tokenize_with_sentences("Just one sentence")
        assert len(sents) == 1


class TestWordExtraction:
    def test_extract_words(self):
        words = extract_words("one two two three")
        assert words == ["one", "two", "two", "three"]

    def test_unique_words(self):
        words = unique_words("b a a b c")
        assert words == ["b", "a", "c"]

    def test_word_frequencies(self):
        freq = dict(word_frequencies("apple banana apple cherry apple"))
        assert freq["apple"] == 3
        assert freq["banana"] == 1

    def test_word_frequencies_top_n(self):
        freq = word_frequencies("a a a b b c", top_n=2)
        assert len(freq) == 2
        assert freq[0][0] == "a"


# ---------------------------------------------------------------------------
# File reading
# ---------------------------------------------------------------------------


class TestFileReading:
    def test_read_txt(self):
        content = read_file_content(b"hello world", "note.txt")
        assert "hello world" in content

    def test_read_csv(self):
        csv_bytes = b"name,age\nAlice,30\nBob,25"
        content = read_file_content(csv_bytes, "data.csv")
        assert "Alice" in content
        assert "Bob" in content

    def test_read_md(self):
        content = read_file_content(b"# Heading\n\nSome text", "readme.md")
        assert "Heading" in content

    def test_unsupported_extension_detected(self):
        assert is_supported_text_file("notes.txt") is True
        assert is_supported_text_file("song.mp3") is False
        assert is_supported_text_file("doc.docx") is True


# ---------------------------------------------------------------------------
# Markov chain
# ---------------------------------------------------------------------------


class TestMarkovChain:
    def test_train_and_generate(self):
        chain = MarkovChain(order=1)
        chain.train(SAMPLE)
        assert chain.is_trained()
        text = chain.generate(max_words=20, rng=random.Random(42))
        assert isinstance(text, str)
        assert len(text) > 0

    def test_generate_with_seed(self):
        chain = MarkovChain(order=2)
        chain.train(SAMPLE)
        text = chain.generate(max_words=15, seed="the", rng=random.Random(1))
        assert text[0].lower() == "t"  # capitalised output

    def test_invalid_order(self):
        with pytest.raises(ValueError):
            MarkovChain(order=0)

    def test_generate_without_training(self):
        chain = MarkovChain(order=1)
        with pytest.raises(ValueError):
            chain.generate()

    def test_output_ends_with_punctuation(self):
        chain = MarkovChain(order=1)
        chain.train(SAMPLE)
        text = chain.generate(max_words=10, rng=random.Random(7))
        assert text[-1] in ".!?"


# ---------------------------------------------------------------------------
# Word-pool generator
# ---------------------------------------------------------------------------


class TestWordPoolGenerator:
    def test_generate_sentence(self):
        pool = WordPoolGenerator(SAMPLE)
        sentence = pool.generate_sentence(rng=random.Random(3))
        assert isinstance(sentence, str)
        assert sentence[0].isupper()
        assert sentence[-1] in ".!?"

    def test_generate_paragraph(self):
        pool = WordPoolGenerator(SAMPLE)
        para = pool.generate_paragraph(sentences=3, rng=random.Random(5))
        assert para.count(".") >= 3

    def test_empty_text_does_not_crash(self):
        pool = WordPoolGenerator("")
        # Should not raise even with an empty pool (falls back gracefully).
        sentence = pool.generate_sentence()
        assert isinstance(sentence, str)


# ---------------------------------------------------------------------------
# High-level TextGenerator facade
# ---------------------------------------------------------------------------


class TestTextGenerator:
    def test_add_file_and_word_count(self):
        gen = TextGenerator()
        gen.add_file(b"hello world hello", "test.txt")
        assert gen.word_count() == 3
        assert gen.unique_word_count() == 2
        assert "test.txt" in gen.filenames

    def test_generate_markov(self):
        gen = TextGenerator(order=1)
        gen.add_file(SAMPLE.encode(), "sample.txt")
        text = gen.generate_markov(max_words=20, rng=random.Random(10))
        assert isinstance(text, str)
        assert len(text) > 0

    def test_generate_random(self):
        gen = TextGenerator()
        gen.add_file(SAMPLE.encode(), "sample.txt")
        text = gen.generate_random(sentences=2, rng=random.Random(10))
        assert isinstance(text, str)
        assert len(text) > 0

    def test_frequency(self):
        gen = TextGenerator()
        gen.add_file(b"apple apple banana", "fruit.txt")
        freq = dict(gen.frequency())
        assert freq["apple"] == 2

    def test_all_unique_words(self):
        gen = TextGenerator()
        gen.add_file(b"zebra apple zebra", "animals.txt")
        words = gen.all_unique_words()
        assert "zebra" in words
        assert "apple" in words
        assert len(words) == 2

    def test_clear(self):
        gen = TextGenerator()
        gen.add_file(b"some text here", "x.txt")
        gen.clear()
        assert gen.has_text() is False
        assert gen.filenames == []

    def test_markov_ready(self):
        gen = TextGenerator(order=2)
        gen.add_file(b"one two", "tiny.txt")
        # Only 2 words, not enough for order=2 (need >= 3)
        assert gen.markov_ready() is False
        gen.add_file(b"three four five", "more.txt")
        assert gen.markov_ready() is True

    def test_add_text_manual(self):
        gen = TextGenerator()
        gen.add_text("hello there friend")
        assert gen.word_count() == 3
