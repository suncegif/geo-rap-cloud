"""Tests for the deterministic 91 BPM timing planner."""

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("plan_rap_timing.py")
SPEC = importlib.util.spec_from_file_location("plan_rap_timing", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TokenSlotsTest(unittest.TestCase):
    """Verify topic-independent token-to-grid behavior."""

    def test_chinese_character_uses_one_slot(self) -> None:
        """A normal Chinese character should occupy one sixteenth-note slot."""
        self.assertEqual(MODULE.token_slots("知"), 1)

    def test_acronyms_follow_spoken_letter_count(self) -> None:
        """Acronyms should work generically rather than for one topic."""
        self.assertEqual(MODULE.token_slots("AI"), 2)
        self.assertEqual(MODULE.token_slots("BPM"), 3)

    def test_sentence_end_reserves_two_slots(self) -> None:
        """Sentence-ending punctuation should create a perceptible pause."""
        self.assertEqual(MODULE.token_slots("。"), 2)


if __name__ == "__main__":
    unittest.main()
