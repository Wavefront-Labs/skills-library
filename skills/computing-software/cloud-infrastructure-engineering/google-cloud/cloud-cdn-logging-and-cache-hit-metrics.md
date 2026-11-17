---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-cdn-logging-and-cache-hit-metrics
name: cloud-cdn-logging-and-cache-hit-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-cdn, cdn-logging, cache-hit-metrics, load-balancer-logs, monitoring]
level: practitioner
status: docs-checked
description: "Measure Cloud CDN effectiveness: enable LB request logging, query cacheHit and cacheLookup fields, compute hit ratio by path, and chart cache metrics to tune cache keys and TTLs."
sources: ["https://docs.cloud.google.com/cdn/docs/logging", "https://docs.cloud.google.com/cdn/docs/caching", "https://docs.cloud.google.com/cdn/docs/using-cache-keys", "https://docs.cloud.google.com/load-balancing/docs/https/https-logging-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud CDN logging and cache hit metrics

## 1. Enable logging on the backend
```bash
gcloud compute backend-services update web-be --global --enable-logging --logging-sample-rate=1.0
```
Lower `--logging-sample-rate` on very high traffic and scale counts accordingly.

## 2. Query
```
resource.type="http_load_balancer"
httpRequest.cacheLookup=true
httpRequest.cacheHit=false
```
Useful fields: `httpRequest.cacheHit`, `cacheLookup`, `cacheValidatedWithOriginServer` (revalidation),
`jsonPayload.statusDetails` (`response_from_cache`, `response_from_cache_validated`, `response_sent_by_backend`),
`jsonPayload.cacheId` (IATA code of the cache location plus an opaque instance id, for example `AMS-85e2bd4b`).

Hit ratio by path with a log sink to BigQuery:
```sql
SELECT REGEXP_EXTRACT(httpRequest.requestUrl, r'https?://[^/]+(/[^?]*)') AS path,
       COUNTIF(httpRequest.cacheHit) / COUNT(*) AS hit_ratio, COUNT(*) AS reqs
FROM `<P>.lb_logs.requests_*` WHERE httpRequest.cacheLookup GROUP BY path ORDER BY reqs DESC LIMIT 50;
```

## 3. Metrics
Monitoring: `loadbalancing.googleapis.com/https/request_count` and `.../backend_request_count` grouped by
`cache_result` (HIT, MISS, DISABLED, PARTIAL_HIT, UNKNOWN).

## 4. What low hit ratio usually means
- Origin sends `Cache-Control: private` or `no-store`: not cached under `CACHE_ALL_STATIC`. With `USE_ORIGIN_HEADERS`, responses
  without valid caching headers are not cached either.
- Query strings with tracking params fragment the cache: exclude them in the cache key (`--cache-key-query-string-blacklist`, or
  `--cache-key-query-string-whitelist` to include only listed ones).
- A `Vary` header with values outside the documented allowed list prevents caching, even under `FORCE_CACHE_ALL`.
- Short TTLs: raise `--default-ttl`.

## Verify
- [ ] Repeat requests for static paths show `cacheHit=true` in the logs after tuning.

## Checked
2026-10-28. Confirmed against the Cloud CDN logging, caching and cache-key pages and the load balancer logging/monitoring page: log fields,
`statusDetails` values, `cacheId` format, `cache_result` values, `backend_request_count`, cache modes, cache-key query-string flags, `Vary` rule.
Removed: backend-bucket logging note, `Set-Cookie` claim, `Age` header and 90% target.
Method: documentation only; no commands were run.
