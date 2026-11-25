---
title: Logging
source: https://docs.northwind.example/logging
---

# Logging

Logs are written to stderr in plain text by default, or as JSON when `--log-format json` is set. The log level is controlled by `--log-level`, which accepts debug, info, warning, and error. Each log line carries the run id so logs from concurrent runs can be told apart. Northwind CLI never logs the values of secrets.
