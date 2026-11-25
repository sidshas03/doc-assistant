---
title: Testing a pipeline
source: https://docs.northwind.example/testing
---

# Testing a pipeline

`nw test` runs the assertions defined in the `tests` block against a sample of the output. An assertion can check row counts, non-null columns, or uniqueness of a key. Failing assertions return a non-zero exit code so `nw test` fits into CI. Tests run against sampled data, not the full dataset, so they are fast but not exhaustive.
