"""A small document assistant: retrieve passages from a corpus, answer from them,
and cite the source — or say the answer isn't there."""

from .answer import Assistant, Answer
from .index import Retriever

__all__ = ["Assistant", "Answer", "Retriever"]
