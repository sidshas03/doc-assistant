---
title: Postgres connector
source: https://docs.northwind.example/connectors/postgres
---

# Postgres connector

The Postgres connector works as both a source and a destination. Connections use a read-only role when Postgres is a source, and the connector never issues DDL against a source database. Set the connection string in `${NW_POSTGRES_URL}`. Batched writes default to 5,000 rows per statement.
