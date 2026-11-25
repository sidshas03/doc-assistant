"""The answer generator.

Default is an extractive MockLLM: it composes the answer from the retrieved
passages themselves, with no API key, so the project runs anywhere and the eval
is deterministic. Swap in a real model by implementing `compose(question, hits)`
and returning it from `get_generator()`; the retrieval and citation logic don't
change, because the model is only ever handed passages the retriever already
chose.
"""
from __future__ import annotations

import os
import re

# If the best passage scores below this, we say we couldn't find it rather than
# answer from a weak match. Tuned against the eval: the answerable and
# unanswerable score distributions overlap a little, so this trades a few missed
# answers for many fewer confident-but-wrong ones. See eval/evaluate.py.
MIN_SCORE = 0.14


class MockLLM:
    name = "mock-extractive"

    def compose(self, question: str, hits) -> str:
        if not hits or hits[0].score < MIN_SCORE:
            return "I couldn't find enough information in the documentation to answer that."
        # Take the single most relevant sentence from the top passage as the answer.
        top = hits[0].chunk
        sentence = _best_sentence(question, top.text)
        return sentence


def _best_sentence(question: str, passage: str) -> str:
    q_words = set(re.findall(r"[a-z0-9]{3,}", question.lower()))
    sentences = re.split(r"(?<=[.!?])\s+", passage)
    best, best_overlap = sentences[0], -1
    for s in sentences:
        overlap = len(q_words & set(re.findall(r"[a-z0-9]{3,}", s.lower())))
        if overlap > best_overlap:
            best, best_overlap = s, overlap
    return best.strip()


def get_generator():
    if os.environ.get("DOCASSIST_LLM", "mock") == "mock":
        return MockLLM()
    raise NotImplementedError(
        "Add your provider in get_generator(). Hand the model the question and the "
        "retrieved passages, and tell it to answer only from them and to cite the "
        "source. Default DOCASSIST_LLM=mock needs no key."
    )
