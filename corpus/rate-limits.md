---
title: Source rate limits
source: https://docs.northwind.example/rate-limits
---

# Source rate limits

When a source is an HTTP API, Northwind CLI respects a `rate_limit` key given in requests per second. If the API returns HTTP 429, the connector waits for the interval in the `Retry-After` header before trying again. There is no global rate limit across pipelines; each run is limited on its own.
