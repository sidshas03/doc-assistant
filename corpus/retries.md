---
title: Retries and failure handling
source: https://docs.northwind.example/retries
---

# Retries and failure handling

A failed step is retried up to three times by default, with exponential backoff starting at two seconds. Retries apply only to transient errors such as network timeouts; a schema mismatch fails immediately and is not retried. Set `retries: 0` on a step to disable retries for that step. The exit code is non-zero if any step fails after its retries are exhausted.
