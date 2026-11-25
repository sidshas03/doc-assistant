.PHONY: install corpus ask eval test

install:   ## install dependencies
	pip install -r requirements.txt

corpus:    ## regenerate the synthetic corpus
	python corpus/_build_corpus.py

ask:       ## ask the sample questions (or: make ask Q="your question")
	PYTHONPATH=src python ask.py $(Q)

eval:      ## run the 30-question eval and compare two chunk sizes
	PYTHONPATH=src:. python -m eval.evaluate

test:      ## run the tests
	PYTHONPATH=src:. python -m pytest tests/ -v
