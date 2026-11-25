---
title: The run command
source: https://docs.northwind.example/commands/run
---

# The run command

`nw run` executes the whole pipeline once, in the order sources, transforms, destinations. Add `--dry-run` to validate and plan without writing to any destination. Add `--only STEP` to run a single named step. The command returns exit code 0 on success and 1 if any step fails.
