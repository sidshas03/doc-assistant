"""Evaluate the assistant, and compare two chunk sizes.

Two things are measured separately, because they fail for different reasons:

  retrieval  — for answerable questions, did the correct document show up in the
               top-k results at all? (If retrieval misses, nothing downstream can
               fix it.)
  answer     — did the assistant put the right source first on answerable
               questions, and did it correctly refuse the unanswerable ones?

Run:  python -m eval.evaluate
The numbers printed are the real results on this corpus, not a target.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from docassist import Assistant, Retriever   # noqa: E402
from eval.questions import QUESTIONS          # noqa: E402

K = 3


def evaluate(chunk_size: int, overlap: int = 20) -> dict:
    assistant = Assistant(retriever=Retriever(chunk_size=chunk_size, overlap=overlap), k=K)

    answerable = [q for q in QUESTIONS if q["doc"]]
    unanswerable = [q for q in QUESTIONS if not q["doc"]]

    retrieval_hits = 0      # gold doc somewhere in top-k
    answer_correct = 0      # gold doc is the top source cited
    refusal_correct = 0     # unanswerable correctly refused
    misses = []

    for item in answerable:
        ans = assistant.ask(item["q"])
        # Retrieval recall ignores the answer-stage threshold on purpose: did the
        # right document rank in the top-k at all?
        top_docs = [h.chunk.doc_id for h in ans.hits]
        if item["doc"] in top_docs:
            retrieval_hits += 1
        if ans.found and ans.hits and ans.hits[0].chunk.doc_id == item["doc"]:
            answer_correct += 1
        else:
            misses.append((item["q"], item["doc"], top_docs[:1] or ["<none>"]))

    for item in unanswerable:
        ans = assistant.ask(item["q"])
        if not ans.found:
            refusal_correct += 1
        else:
            misses.append((item["q"], "REFUSE", [ans.hits[0].chunk.doc_id]))

    na = len(answerable)
    nu = len(unanswerable)
    return {
        "chunk_size": chunk_size,
        "retrieval_recall@3": round(retrieval_hits / na, 3),
        "answer_precision@1": round(answer_correct / na, 3),
        "refusal_accuracy": round(refusal_correct / nu, 3),
        "overall": round((answer_correct + refusal_correct) / len(QUESTIONS), 3),
        "misses": misses,
    }


def main() -> int:
    runs = [evaluate(chunk_size=cs) for cs in (60, 120)]

    print(f"{'metric':<22}" + "".join(f"chunk={r['chunk_size']:<8}" for r in runs))
    print("-" * 46)
    for key in ("retrieval_recall@3", "answer_precision@1", "refusal_accuracy", "overall"):
        print(f"{key:<22}" + "".join(f"{r[key]:<14}" for r in runs))

    best = max(runs, key=lambda r: r["overall"])
    print(f"\nBest overall: chunk_size={best['chunk_size']} ({best['overall']*100:.0f}%)")
    print("\nWhere the best config still slips:")
    for q, gold, got in best["misses"]:
        print(f"  - {q}\n      wanted {gold}, top source {got[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
