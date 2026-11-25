---
title: Troubleshooting common errors
source: https://docs.northwind.example/troubleshooting
---

# Troubleshooting common errors

A run that stops with `config invalid` means `northwind.yaml` failed validation; run `nw validate` to see the exact line. A `connection refused` error from a source usually means the connection string or a firewall rule is wrong. If a run hangs, check whether a source API is rate limiting it. Raising the log level to debug shows the step that is stuck.
