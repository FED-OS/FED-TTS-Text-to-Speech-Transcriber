"""Test the grammar checker module (No AI, deterministic)."""

import pytest
from src.fed_tts.grammar_checker import GrammarChecker


@pytest.fixture
def checker():
    return GrammarChecker()


class TestSpellCheck:
    def test_correct_spelling(self, checker):
        """Correctly spelled words should not be flagged."""
        results = checker.check_spelling("hello world this is a test")
        assert len(results) == 0

    def test_misspelled_word(self, checker):
        """Misspelled words should be flagged."""
        results = checker.check_spelling("helo wrld")
        assert "helo" in results
        assert "wrld" in results

    def test_empty_string(self, checker):
        """Empty string should return no misspellings."""
        results = checker.check_spelling("")
        assert len(results) == 0


class TestGrammarRules:
    def test_would_of(self, checker):
        """'would of' should be flagged."""
        results = checker.check_grammar("I would of gone to the store.")
        assert any("would have" in issue for issue in results)

    def test_could_of(self, checker):
        """'could of' should be flagged."""
        results = checker.check_grammar("I could of done that.")
        assert any("could have" in issue for issue in results)

    def test_should_of(self, checker):
        """'should of' should be flagged."""
        results = checker.check_grammar("You should of told me.")
        assert any("should have" in issue for issue in results)

    def test_double_space(self, checker):
        """Double spaces should be flagged."""
        results = checker.check_grammar("This has  double space.")
        assert any("Double space" in issue for issue in results)

    def test_passive_voice(self, checker):
        """Passive voice pattern should be flagged."""
        results = checker.check_grammar("The ball was kicked by John.")
        assert any("Passive voice" in issue for issue in results)

    def test_long_sentence(self, checker):
        """Sentences over 25 words should be flagged."""
        long_sentence = " ".join(["word"] * 30) + "."
        results = checker.check_grammar(long_sentence)
        assert any("long" in issue.lower() for issue in results)

    def test_clean_text(self, checker):
        """Clean text should have no grammar issues."""
        results = checker.check_grammar("This is a clean sentence with no errors.")
        assert len(results) == 0


class TestCheckMethod:
    def test_check_returns_dict(self, checker):
        """check() should return a dict with misspelled and issues keys."""
        results = checker.check("hello world")
        assert "misspelled" in results
        assert "issues" in results

    def test_check_with_errors(self, checker):
        """check() should detect both spelling and grammar errors."""
        results = checker.check("I would of gone their.")
        assert len(results["issues"]) > 0
