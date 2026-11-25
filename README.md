# Document assistant you can check

A question-answering assistant over a set of documentation. You ask a question,
it finds the relevant passages, answers from them, and shows you the source. When
the answer isn't in the docs, it says so instead of making something up.

The reason it's built this way: a RAG system that can't be inspected is hard to
trust. So every answer carries its sources, and there's an evaluation harness
that measures how often retrieval finds the right document, how often the right
source is cited first, and how often an out-of-scope question is correctly
refused — on real numbers, not a made-up accuracy figure.

## What it looks like

```
$ python ask.py "How many times does a failed step retry?"

Q: How many times does a failed step retry?
A: A failed step is retried up to three times by default, with exponential backoff starting at two seconds.
Sources:
  - Retries and failure handling (https://docs.northwind.example/retries)  score=0.251

$ python ask.py "What is the refund policy?"

A: I couldn't find enough information in the documentation to answer that.
Sources: none (answer not found in the documentation)
```

The corpus is 19 short, made-up docs for a fictional tool called Northwind CLI,
so there's nothing scraped or copyrighted. The facts in them are specific enough
that the eval can check answers against the source.

## How it works

```
question -> retrieve top-k passages (TF-IDF) -> answer from them, cite the source
         -> if the best match is too weak, say "I couldn't find it"
```

Four small pieces in `src/docassist/`: `ingest` loads the corpus and splits it
into chunks that remember which document they came from; `index` is the retriever;
`llm` turns the retrieved passages into an answer; `answer` ties them together and
attaches sources.

Retrieval is TF-IDF by default — lexical, offline, no API key — which keeps the
whole thing runnable and the eval reproducible. The retriever and the generator
are both behind small interfaces, so you can swap in embeddings or a real model
without touching the rest (see below).

## The evaluation

This is the part worth reading. 30 questions: 20 that the docs can answer, 10 that
they can't. Retrieval and answer quality are measured separately, because they
break for different reasons, and two chunk sizes are compared.

```
$ make eval

metric                chunk=60      chunk=120
----------------------------------------------
retrieval_recall@3    1.0           1.0
answer_precision@1    0.8           0.8
refusal_accuracy      0.8           0.7
overall               0.8           0.767

Best overall: chunk_size=60 (80%)
```

What this says, read honestly:

- Retrieval is the strong part — the right document is in the top three every
  time, for both chunk sizes.
- The weaker parts are putting the right source *first* (0.8) and refusing
  out-of-scope questions (0.8). The answerable and unanswerable questions have
  overlapping similarity scores, so the "couldn't find it" threshold trades a
  couple of missed answers for a lot fewer confident-but-wrong ones. There's no
  threshold that gets both perfect on this corpus, and the eval shows exactly
  that.
- Smaller chunks (60 words) beat larger ones (120) here, mostly on refusals. The
  eval prints every case the best config still gets wrong, so the failures are
  visible rather than hidden behind an average.

These numbers are the real output of `make eval`, not a target. The useful part
is that the test set and the misses are both easy to read.

## Running it

```bash
make install     # scikit-learn, numpy, pytest
make ask         # ask the sample questions
make ask Q="How do I pin the version in production?"
make eval        # the 30-question eval + chunk-size comparison
make test        # a few behaviour tests
```

No API key, no services, no database. It runs on a laptop in a couple of seconds.

## Swapping in embeddings

TF-IDF matches on words, so it misses a question that means the same thing in
different words. To go semantic, install `sentence-transformers` and `faiss-cpu`,
embed the chunks in `index.py`, and search the FAISS index instead of the TF-IDF
matrix. Nothing else changes — `answer.py` and the eval only see hits with a
score, so the citation logic and the measurements stay the same. The same goes
for the answer step: point `get_generator()` in `llm.py` at a real model, hand it
the retrieved passages, and tell it to answer only from them and cite the source.

## Layout

```
corpus/            19 synthetic docs + the script that writes them
src/docassist/     ingest, index (retriever), llm (generator), answer
ask.py             command-line Q&A
eval/              30 questions + the evaluation and chunk-size comparison
tests/             behaviour tests
```

## Honest scope

Everything is made up — Northwind CLI isn't real. Retrieval is lexical, so it's
beatable by embeddings, and the answer step is extractive rather than a real
model. Both are swappable, as above. The point of the project isn't a
state-of-the-art number; it's a RAG system where you can see the sources and
measure whether it actually works.
