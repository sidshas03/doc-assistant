---
title: Writing transforms
source: https://docs.northwind.example/transforms
---

# Writing transforms

Transforms are SQL files referenced from the `transforms` section and run against the in-memory engine between source and destination. Each transform must be a single `SELECT`; statements that modify data are rejected. Transforms can reference the output of earlier transforms by name, which lets you build a small chain of steps.
