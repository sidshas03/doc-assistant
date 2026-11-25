"""Load the corpus and split it into chunks.

Each chunk keeps a pointer back to the document it came from (title + source URL),
because the whole point of this assistant is that every answer can be traced to a
source. Chunk size is a parameter on purpose — the eval compares two sizes.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parents[2] / "corpus"


@dataclass(frozen=True)
class Chunk:
    doc_id: str          # file slug, e.g. "connectors-s3"
    title: str
    source: str          # source URL
    text: str
    ordinal: int         # position of the chunk within its document


def _parse(md: str) -> tuple[dict, str]:
    """Split simple `--- key: value ---` front matter from the body."""
    meta: dict = {}
    body = md
    if md.startswith("---"):
        _, fm, body = md.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def _chunk_words(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    if len(words) <= size:
        return [" ".join(words)]
    step = max(1, size - overlap)
    out = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if piece:
            out.append(" ".join(piece))
        if start + size >= len(words):
            break
    return out


def load_chunks(chunk_size: int = 90, overlap: int = 20,
                corpus_dir: Path = CORPUS_DIR) -> list[Chunk]:
    """Read every .md file in the corpus and return a flat list of chunks."""
    chunks: list[Chunk] = []
    for path in sorted(corpus_dir.glob("*.md")):
        meta, body = _parse(path.read_text())
        # Drop the leading "# Title" heading line from the body before chunking.
        body = re.sub(r"^#.*\n", "", body, count=1).strip()
        title = meta.get("title", path.stem)
        source = meta.get("source", "")
        for i, piece in enumerate(_chunk_words(body, chunk_size, overlap)):
            chunks.append(Chunk(path.stem, title, source, piece, i))
    return chunks
