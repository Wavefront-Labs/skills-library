---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.tail-latency-analysis
name: tail-latency-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, tail-latency-analysis, percentiles, p99, histograms, hdrhistogram, coordinated-omission, hedged-requests]
level: practitioner
status: draft
description: "Analyse tail latency correctly: histograms not averages, aggregating percentiles, coordinated omission, fan-out amplification and the tactics that cut p99/p99.9."
sources: ["https://research.google/pubs/the-tail-at-scale/", "https://hdrhistogram.github.io/HdrHistogram/", "https://prometheus.io/docs/practices/histograms/", "https://sre.google/sre-book/monitoring-distributed-systems/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tail latency and percentile analysis

## Steps
1. **Record distributions, not means.** Use histograms (Prometheus native/classic histograms,
   OpenTelemetry exponential histograms, HdrHistogram) at the server and the client. Report
   p50, p90, p99, p99.9 and max per endpoint and per dependency.
2. **Aggregate correctly.** Percentiles cannot be averaged across instances or time windows.
   Merge histogram buckets, then compute the quantile:
   `histogram_quantile(0.99, sum by (le, route) (rate(http_server_duration_seconds_bucket[5m])))`.
   Classic-bucket boundaries must bracket your SLO threshold or the estimate is meaningless.
3. **Check for coordinated omission.** Closed-loop load generators that wait for each response
   under-report stalls. Use open-model tools (wrk2 `-R`, k6 `constant-arrival-rate`,
   Gatling open injection) or HdrHistogram's expected-interval correction.
4. **Account for fan-out.** A request touching N backends sees the backend p99 on
   `1 - 0.99^N` of requests (N=100 means 63%). Measure the per-leaf tail and the end-to-end tail.
5. **Find the cause with exemplars.** Link histogram buckets to trace IDs (OpenMetrics exemplars)
   and inspect the slowest traces: GC pauses, lock contention, cold caches, noisy neighbours,
   TCP retransmits, queueing behind large requests, cross-AZ hops.
6. **Apply tail-tolerant techniques** (Dean and Barroso, *The Tail at Scale*): hedged requests
   after the p95 delay, tied requests with cancellation, micro-partitioning, selective
   replication of hot items, latency-induced probation of slow replicas, and good-enough
   responses for fan-out leaves that miss the deadline.
7. **Reduce variability at source**: bound queue depth, separate large and small request pools,
   tune GC (ZGC/Shenandoah, `GOGC`), pin CPU for latency-critical work, avoid synchronous logging.

## Gotchas
- Summaries (client-side quantiles) cannot be aggregated across pods; prefer histograms.
- p99 over 1 minute on a low-traffic service is a handful of requests; show request counts.
- Hedging without a budget (for example, max 5% extra load) amplifies overload.
- Load balancer latency includes client upload time; compare with server-side spans.

## Verify
- [ ] Dashboards show p99/p99.9 from merged histograms with request counts.
- [ ] Load tests use an open model at a fixed arrival rate.
- [ ] Top tail contributors identified from exemplar traces, with a fix owner each.
