---
id: computing-software.cloud-infrastructure-engineering.observability.comparing-per-signal-telemetry-cost
name: comparing-per-signal-telemetry-cost
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [signal-cost-comparison, per-signal-cost, observability-cost, telemetry-budget, metrics, logs, traces]
level: practitioner
status: draft
description: "Estimate and compare storage and query cost of answering the same question with metrics, logs or traces, using bytes-per-event and series arithmetic."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://grafana.com/docs/loki/latest/operations/storage/", "https://opentelemetry.io/docs/concepts/signals/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comparing per-signal cost

Goal: pick the cheapest signal that answers a question, with numbers rather than opinion.

## Unit costs to measure (your own system beats any rule of thumb)
| Signal | Cost driver | How to measure |
|---|---|---|
| Metrics | active series x samples per series | `prometheus_tsdb_head_series`; ~1-2 bytes/sample compressed on disk |
| Logs | GB ingested and retained; query bytes scanned | Loki `loki_distributor_bytes_received_total`; bytes per line x lines/s |
| Traces | spans/s x bytes per span (attributes dominate) | `otelcol_exporter_sent_spans`, backend ingest bytes |
| Profiles | profiles/s x samples | backend ingest metrics |

## Worked comparison: HTTP error rate for 50 routes, 1,000 req/s
- Metrics: counter by route x status class (5) = 250 series; at 15s scrape that is ~1.4M samples/day, ~3 MB/day on disk. Query is instant.
- Logs: 1,000 lines/s x 400 bytes = ~34 GB/day ingested. A 24h error-rate query scans the whole set unless pre-aggregated.
- Traces at 10% sampling: 100 spans/s x 1 KB = ~8.6 GB/day, and error rate is now an estimate.
Conclusion: metrics for the rate, logs/traces for the examples behind it.

## Method
1. Write the question and the resolution needed (per minute? per request?).
2. Compute volume per signal with the table above.
3. Add query cost: logs and traces are paid again at read time.
4. Pick the cheapest signal that meets resolution; keep exemplars or trace ids to link to richer data.

## Gotchas
- SaaS pricing is often per active series, per GB, or per host; convert to the vendor unit before comparing.
- Cardinality makes metrics expensive fast: a `user_id` label turns 250 series into millions.
- Index-light log stores (Loki) shift cost from ingest to query; heavy daily queries may cost more than indexing.

## Verify
- [ ] Each high-volume signal has a written cost per day and an owner.
- [ ] Questions answered daily by scanning logs have been converted to metrics or recording rules.
