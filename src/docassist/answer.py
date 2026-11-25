"""Tie retrieval and generation together into an answer with citations.

The contract: never answer without a source, and say plainly when the answer
isn't in the documents instead of guessing.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .index import Hit, Retriever
from .llm import MockLLM, MIN_SCORE, get_generator


@dataclass
class Answer:
    text: str
    found: bool
    sources: list[dict] = field(default_factory=list)   # [{title, source, score}]
    hits: list[Hit] = field(default_factory=list)


class Assistant:
    def __init__(self, retriever: Retriever | None = None, generator=None, k: int = 3):
        self.retriever = retriever or Retriever()
        self.generator = generator or get_generator()
        self.k = k

    def ask(self, question: str) -> Answer:
        hits = self.retriever.search(question, k=self.k)
        found = bool(hits) and hits[0].score >= MIN_SCORE
        text = self.generator.compose(question, hits)
        sources = []
        if found:
            seen = set()
            for h in hits:
                if h.score >= MIN_SCORE and h.chunk.doc_id not in seen:
                    seen.add(h.chunk.doc_id)
                    sources.append({"title": h.chunk.title,
                                    "source": h.chunk.source,
                                    "score": round(h.score, 3)})
        return Answer(text=text, found=found, sources=sources, hits=hits)
