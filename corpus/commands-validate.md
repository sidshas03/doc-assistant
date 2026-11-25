---
title: The validate command
source: https://docs.northwind.example/commands/validate
---

# The validate command

`nw validate` checks `northwind.yaml` for schema errors, unknown keys, and unresolved `${VAR}` references without moving any data. It is safe to run in CI on every pull request. The command exits non-zero when the config is invalid, which makes it a useful pre-merge gate.
