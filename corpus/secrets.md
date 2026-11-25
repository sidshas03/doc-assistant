---
title: Managing secrets
source: https://docs.northwind.example/secrets
---

# Managing secrets

Secrets are never stored in `northwind.yaml`; the file holds only `${VAR}` references. At run time the values are read from environment variables or a `.env` file in the project root. A `.env` file should be listed in `.gitignore` and never committed. Northwind CLI redacts anything that looks like a key from its logs and error messages.
