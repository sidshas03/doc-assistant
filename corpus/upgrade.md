---
title: Upgrading and versioning
source: https://docs.northwind.example/upgrade
---

# Upgrading and versioning

Upgrade with `pip install --upgrade northwind-cli`. Northwind CLI follows semantic versioning, so a minor upgrade never breaks an existing `northwind.yaml`. A major upgrade may change the config format, and the release notes list a migration command when one is needed. Pin the version in production with `northwind-cli==MAJOR.MINOR.PATCH`.
