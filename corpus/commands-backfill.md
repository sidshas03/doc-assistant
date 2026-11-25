---
title: The backfill command
source: https://docs.northwind.example/commands/backfill
---

# The backfill command

`nw backfill --from 2026-01-01 --to 2026-01-31` reprocesses a historical date range. Backfill runs in daily chunks so a failure part way through only loses the current day, not the whole range. Backfill writes to the same destinations as a normal run; point it at a staging destination first if you want to check the output.
