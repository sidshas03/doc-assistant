"""The retriever.

Default is TF-IDF cosine similarity — lexical, offline, no API key, which keeps
the whole project runnable and the eval reproducible. The interface is small on
purpose so you can drop in embeddings (sentence-transformers + FAISS) later
without touching the answer or eval code; see README "Swapping in embeddings".
"""
from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ingest import Chunk, load_chunks


@dataclass
class Hit:
    chunk: Chunk
    score: float


class Retriever:
    def __init__(self, chunk_size: int = 90, overlap: int = 20):
        self.chunks = load_chunks(chunk_size=chunk_size, overlap=overlap)
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        # Index the title alongside the chunk text — the document title is a
        # strong signal (e.g. "S3 connector") and cheap to include.
        self._matrix = self._vectorizer.fit_transform(
            f"{c.title} {c.text}" for c in self.chunks
        )

    def search(self, query: str, k: int = 3) -> list[Hit]:
        qv = self._vectorizer.transform([query])
        scores = cosine_similarity(qv, self._matrix)[0]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in ranked]
