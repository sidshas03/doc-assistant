#!/usr/bin/env python3
"""Ask the assistant a question from the command line.

    python ask.py "How do I install Northwind CLI?"
    python ask.py            # a few sample questions
"""
from __future__ import annotations

import sys

from docassist import Assistant

SAMPLES = [
    "How do I install Northwind CLI?",
    "What format should I use in S3 for large data?",
    "How many times does a failed step retry?",
    "Does Northwind have its own scheduler?",
    "What is the refund policy?",   # not in the docs -> should say it can't find it
]


def show(assistant: Assistant, q: str) -> None:
    ans = assistant.ask(q)
    print("\nQ:", q)
    print("A:", ans.text)
    if ans.sources:
        print("Sources:")
        for s in ans.sources:
            print(f"  - {s['title']} ({s['source']})  score={s['score']}")
    else:
        print("Sources: none (answer not found in the documentation)")


def main() -> int:
    assistant = Assistant()
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else SAMPLES
    for q in questions:
        show(assistant, q)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
