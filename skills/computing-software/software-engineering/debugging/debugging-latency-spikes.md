---
id: computing-software.software-engineering.debugging.debugging-latency-spikes
name: debugging-latency-spikes
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, latency-spikes, slow-requests, tail-latency, distributed-tracing, gc-pauses]
level: advanced
status: draft
description: "Debug latency spikes and slow requests: percentile analysis, trace exemplars, correlating with GC, saturation, noisy neighbours, retries and lock contention."
sources: ["https://www.brendangregg.com/methodology.html", "https://opentelemetry.io/docs/concepts/signals/traces/", "https://research.google/pubs/the-tail-at-scale/", "https://www.brendangregg.com/offcpuanalysis.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging latency spikes and slow requests

## 1. Characterise the spike
- Which percentile moved (p50 vs p99/p99.9)? Median shifts = everything slower (saturation,
  regression); only tail = intermittent stalls (GC, locks, retries, cold caches, one bad host).
- Scope: all endpoints or one? All hosts or one AZ/pod? All tenants or one? Correlated with a deploy,
  traffic increase, cron job, backup window, cache expiry?
- Periodicity: every 60 s or on the hour suggests scheduled jobs, cache TTLs, log rotation, cron.

## 2. Find slow examples, then look inside them
- **Trace exemplars**: from the latency histogram jump to individual slow traces (Grafana exemplars,
  Honeycomb BubbleUp, Datadog/Jaeger trace search `duration > 2s`). The span waterfall shows which
  hop and whether time is in a call or in a gap (uninstrumented work, queueing).
- **Gaps between spans** = time in your process not covered: GC, thread pool queueing, CPU throttling,
  synchronous logging, lock waits.
- Slow query logs: Postgres `log_min_duration_statement`, `pg_stat_statements`, `auto_explain`;
  MySQL slow log.

## 3. Usual suspects and checks
| Suspect | Evidence |
|---|---|
| GC pauses | GC logs (`-Xlog:gc*`), `jstat`, .NET `dotnet-counters` gen2 counts, Go `GODEBUG=gctrace=1` |
| CPU throttling (containers) | `container_cpu_cfs_throttled_periods_total`, `/sys/fs/cgroup/cpu.stat` `nr_throttled` |
| Thread/connection pool saturation | pool wait time metrics, active == max |
| Lock contention | off-CPU flame graphs, JFR lock events, `pg_locks`/`pg_stat_activity` wait events |
| Retries/timeouts downstream | client retry metrics; latency clusters at timeout values (1 s, 2 s, 5 s) |
| Noisy neighbour / one bad host | per-host latency breakdown; steal time (`%st` in `mpstat`) |
| Cold caches / cache stampede | cache hit ratio drops at spike times |
| DNS, TLS handshakes, connection setup | trace spans for connect; connection reuse disabled |
| Disk / fsync | `iostat -x` await, `biolatency` |

Latency clustered exactly at round numbers is a timeout-plus-retry signature.

## 4. Confirm and fix
Reproduce under load if possible (k6 with the same request mix), change one thing, compare the
latency histogram before/after, not averages. Tail tolerance: hedged requests and timeouts help;
fixing the cause helps more.
