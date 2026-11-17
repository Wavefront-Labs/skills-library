---
id: computing-software.search-and-information-retrieval.apache-solr.circuit-breakers-rate-limiters
name: circuit-breakers-rate-limiters
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [circuit-breakers, rate-limiting, load-shedding, warn-only, http-429]
level: advanced
status: docs-checked
description: "Protect a Solr node under load with circuit breakers (heap, CPU, load average, 429, warnOnly) and the query rate limiter set through the cluster API (allowedRequests)."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/circuit-breakers.html
  - https://solr.apache.org/guide/solr/latest/deployment-guide/rate-limiters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# circuit-breakers-rate-limiters

Circuit breakers trade throughput for stability: under duress, requests fail with HTTP 429, and clients must retry. A breaker may run in warn-only mode, which logs instead of rejecting, so thresholds can be tuned safely. The check happens on the node handling the initial request, so load balance clients across nodes. The error code is changed with `solr.circuitbreaker.errorcode`.

Global: environment variable or system property per resource and request type, for example `SOLR_CIRCUITBREAKER_QUERY_MEM=75` (`solr.circuitbreaker.query.mem`), `..._UPDATE_CPU=95`, `..._LOADAVG`. Add `_WARNONLY=true` (or `.warnonly`) for warn-only mode.

Per collection: `<circuitBreaker class="org.apache.solr.util.circuitbreaker.MemoryCircuitBreaker"><double name="threshold">75</double></circuitBreaker>` in `solrconfig.xml`, with `CPUCircuitBreaker` similarly. By default only search requests are affected, and per-collection breakers are checked before global ones. The heap threshold is a percentage of `-Xmx` between 50 and 95.

Rate limiter (per JVM, not per collection): applies to requests with header `Solr-Request-Type: QUERY`. Configure with `POST /api/cluster` and `set-ratelimiter`: `enabled`, `allowedRequests` (default cores times 3), `guaranteedSlots`, `slotBorrowingEnabled`, `slotAcquisitionTimeoutInMS`. Excess requests get 429.

## Checked

2026-11-04. Confirmed against the Circuit Breakers and Rate Limiters pages: 429 behaviour, warn-only mode, `solr.circuitbreaker.errorcode`, global variables (for example `SOLR_CIRCUITBREAKER_UPDATE_CPU=95`), per-collection precedence, heap range 50-95, `POST /api/cluster` with `set-ratelimiter`, default `allowedRequests` of cores * 3, `Solr-Request-Type: QUERY`. Nothing removed.

Method: documentation only; no commands were run.
