---
title: Deploying Northwind CLI
source: https://docs.northwind.example/deployment
---

# Deploying Northwind CLI

The recommended deployment is a small container that runs `nw run` on a schedule from an external scheduler. The state directory must be on persistent storage so incremental runs work across restarts. A single run is single-process and does not need more than one CPU for typical workloads. Scale by running independent pipelines rather than threading a single one.
