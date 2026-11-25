---
title: Scheduling pipelines
source: https://docs.northwind.example/scheduling
---

# Scheduling pipelines

Northwind CLI does not run a scheduler of its own. Instead, `nw run` is designed to be called by cron, Airflow, or any external scheduler. Each run is independent and writes a run record to the state directory. Use `nw run --since LAST` to process only data added after the previous successful run.
