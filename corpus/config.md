---
title: The northwind.yaml config file
source: https://docs.northwind.example/config
---

# The northwind.yaml config file

Every project is driven by a single `northwind.yaml` file at the project root. It has three top-level sections: `sources`, `transforms`, and `destinations`. Environment variables are referenced with the `${VAR}` syntax and resolved at run time. The file is validated before every run; an invalid file stops the run before any data moves.
