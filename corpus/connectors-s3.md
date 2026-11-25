---
title: S3 connector
source: https://docs.northwind.example/connectors/s3
---

# S3 connector

The S3 connector reads and writes CSV, JSON, and Parquet. Parquet is recommended for anything over one million rows because it is far smaller and faster to scan. Credentials come from the standard AWS environment variables or an instance role. Objects are written under a `date=YYYY-MM-DD` prefix by default so downstream tools can partition by day.
