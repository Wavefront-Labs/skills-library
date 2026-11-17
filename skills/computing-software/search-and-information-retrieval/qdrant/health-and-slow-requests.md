---
id: computing-software.search-and-information-retrieval.qdrant.health-and-slow-requests
name: health-and-slow-requests
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [healthz, readyz, livez, slow-request-log, mon-health]
level: practitioner
status: docs-checked
description: "Probe liveness and readiness with /healthz, /livez and /readyz and capture slow requests in the slow request log."
sources:
  - "https://qdrant.tech/documentation/ops-monitoring/slow-request-log/"
  - "https://qdrant.tech/documentation/ops-monitoring/monitoring/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Kubernetes health endpoints (available as of v1.5.0): `/healthz`, `/livez` and `/readyz`. They give the most basic status, returning HTTP 200 if Qdrant is started and ready. They are always accessible, whether or not an API key is configured, so probes need no credentials.

```yaml
livenessProbe:
  httpGet: { path: /livez, port: 6333 }
readinessProbe:
  httpGet: { path: /readyz, port: 6333 }
```

Slow request log (v1.16.0, beta, so behaviour may change):

- It records the slowest unique operations on a node since startup, to show which queries cause high latency. It is enabled by default and cannot be disabled.
- It captures shard-level operations slower than 50 ms: `core_search`, `query_batch`, `count`, `retrieve`, `facet` and writes such as upsert and delete.
- It keeps up to 32 entries per request type, deduplicated by a content hash of the request body and collection name, with an approximate count of how often each pattern was seen. When full, a new entry replaces the fastest one only if it was slower.
- It is in memory only and resets on restart, so restart after a deploy or config change for a clean baseline.
- It is per node: query each node of a cluster and aggregate.
- Read it with `GET /profiler/slow_requests`, which needs `manage` access and is REST only. Parameters are `limit` (default 10) and `request` (substring filter on request type, for example `search`). Entries show `collection_name`, `duration` in seconds, `datetime`, `request_name`, `approx_count`, optional `cpu_usage_ratio` and the full `request_body`, sorted slowest first.

```bash
curl "http://YOUR_NODE_URL:6333/profiler/slow_requests?limit=20&request=search" -H "api-key: <your-key>"
```

## Checked

Method: docs-checked 2026-11-09 against the Qdrant slow request log page (landing_page repo, ops-monitoring/slow-request-log.md) and the Kubernetes health endpoints section of the monitoring page (ops-monitoring/monitoring.md), both read in full. Removed the unconfirmed readiness/liveness usage advice and startup allowance, and corrected the claim that API key settings apply to health endpoints (the docs say they are always accessible).
