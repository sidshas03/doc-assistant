---
title: BigQuery connector
source: https://docs.northwind.example/connectors/bigquery
---

# BigQuery connector

The BigQuery connector is a destination only. It loads data through staged files rather than streaming inserts, which keeps costs low for large loads. A load job that fails midway is rolled back, so a table is never left half-written. Set the dataset with the `dataset` key on the destination.
