"""
Grammar Checker Module - No AI, deterministic rule-based checking.

Uses pyspellchecker (dictionary-based) for spelling and regex patterns
for grammar and style issues.
"""

import re
from spellchecker import SpellChecker


class GrammarChecker:
    """Deterministic grammar and spell checker (no AI/ML)."""

    def __init__(self):
        self.spell = SpellChecker()
        self.grammar_rules = [
            {
                "pattern": r"\bwould of\b",
                "message": "❓ 'would of' should be 'would have'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\bcould of\b",
                "message": "❓ 'could of' should be 'could have'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\bshould of\b",
                "message": "❓ 'should of' should be 'should have'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\bmust of\b",
                "message": "❓ 'must of' should be 'must have'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\balot\b",
                "message": "❓ 'alot' should be 'a lot'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\btheir\s+is\b",
                "message": "❓ 'their is' should be 'there is'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\byour\s+welcome\b",
                "message": "❓ 'your welcome' should be 'you're welcome'",
                "flags": re.IGNORECASE,
            },
            {
                "pattern": r"\bits\s+a\b",
                "message": "❓ Check 'its a' - might need 'it's a'",
                "flags": re.IGNORECASE,
            },
        ]

    def check_spelling(self, text):
        """Check spelling using dictionary-based lookup (no AI)."""
        words = re.findall(r"\b\w+\b", text)
        misspelled = self.spell.unknown(words)
        return misspelled

    def check_grammar(self, text):
        """Check grammar using regex pattern matching (no AI)."""
        issues = []

        # Apply grammar rules
        for rule in self.grammar_rules:
            if re.search(rule["pattern"], text, rule["flags"]):
                issues.append(rule["message"])

        # Double spaces
        if re.search(r"  ", text):
            issues.append("🔴 Double space found (consider removing)")

        # Passive voice indicator
        if re.search(r"\bwas\s+\w+ed\s+by\b", text, re.IGNORECASE):
            issues.append("📝 Passive voice detected. Consider active voice.")

        if re.search(r"\bwere\s+\w+ed\s+by\b", text, re.IGNORECASE):
            issues.append("📝 Passive voice detected. Consider active voice.")

        # Sentence length check
        sentences = re.split(r"[.!?]", text)
        for i, sent in enumerate(sentences):
            word_count = len(sent.split())
            if word_count > 25:
                issues.append(f"✂️ Sentence {i + 1} is long ({word_count} words). Consider splitting.")

        # Repeated words
        if re.search(r"\b(\w+)\s+\1\b", text, re.IGNORECASE):
            matches = re.findall(r"\b(\w+)\s+\1\b", text, re.IGNORECASE)
            for match in set(matches):
                if match.lower() not in ["that", "very"]:
                    issues.append(f"🔁 Repeated word: '{match} {match}'")

        # Capitalization at sentence start
        if re.search(r"[.!?]\s+[a-z]", text):
            issues.append("🔠 Sentence may not start with a capital letter.")

        return issues

    def check(self, text):
        """Run both spelling and grammar checks."""
        return {
            "misspelled": self.check_spelling(text),
            "issues": self.check_grammar(text),
        }
