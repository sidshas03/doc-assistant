"""A few tests that lock in the behaviour that matters: answers come with a
source, and out-of-corpus questions are refused instead of answered."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from docassist import Assistant


def _assistant():
    return Assistant()


def test_known_question_cites_the_right_doc():
    ans = _assistant().ask("How many times is a failed step retried?")
    assert ans.found
    assert ans.sources
    assert ans.hits[0].chunk.doc_id == "retries"
    assert "three" in ans.text.lower()


def test_answer_always_has_a_source_when_found():
    ans = _assistant().ask("How do I install Northwind CLI?")
    assert ans.found
    assert ans.sources and ans.sources[0]["source"].startswith("http")


def test_out_of_corpus_question_is_refused():
    ans = _assistant().ask("What is the refund policy?")
    assert not ans.found
    assert "couldn't find" in ans.text.lower()
    assert ans.sources == []


def test_another_unanswerable_is_refused():
    ans = _assistant().ask("What is the phone number for support?")
    assert not ans.found
