---
id: computing-software.software-engineering.concurrency.workload-characterization-and-drill-down
name: workload-characterization-and-drill-down
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, workload-characterization, drill-down-analysis, methodology, brendan-gregg]
level: advanced
status: draft
description: "Apply Gregg's workload characterisation (who, why, what, how is load changing) and drill-down analysis to find performance problems systematically instead of guessing."
sources: ["https://www.brendangregg.com/methodology.html", "https://www.brendangregg.com/systems-performance-2nd-edition-book.html", "https://www.brendangregg.com/USEmethod/use-linux.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workload characterisation and drill-down analysis

Two methodologies from Brendan Gregg's Systems Performance that complement the USE method.

## Workload characterisation: understand the load, not the system
Answer four questions about the applied load:
1. **Who** is causing the load? (client IPs, tenants, users, processes, API keys, query templates)
2. **Why** is the load being called? (code path, stack trace, feature, cron job)
3. **What** are the load characteristics? (rate/IOPS, throughput, request size distribution, read/
   write mix, cache hit ratio, variance)
4. **How** is it changing over time? (daily pattern, growth, sudden step)

Often the biggest wins come from **eliminating unnecessary work** found this way: a misconfigured
client polling every 100 ms, a retry storm, a crawler, a duplicated batch job, a missing cache.

Tools: access logs aggregated by key (`awk '{print $1}' access.log | sort | uniq -c | sort -rn`),
`pg_stat_statements` by query, `iotop`/`biotop` by process, `nethogs`, `ss` by peer, tracing
backends grouped by endpoint/tenant, `bpftrace` one-liners counting syscalls by process.

## Drill-down analysis
Start broad, narrow by following the biggest contributor at each level:
1. **Monitoring**: which service/host/time window looks wrong?
2. **Identification**: which resource or component (CPU, disk, a dependency, a query)?
3. **Analysis**: drill into that component with specific tools (per-process, per-thread, per-
   function: `pidstat`, `perf top`, flame graphs, slow query log, `biolatency`), down to code or
   kernel stack.
Five whys at each layer: "the DB is slow" -> "one query is 80% of time" -> "seq scan" -> "missing
index after migration".

## Pair with
- **USE** (utilisation, saturation, errors per resource) to check resources quickly.
- **RED** (rate, errors, duration) per service.
- Avoid anti-methods: "streetlight" (using familiar tools only), "random change", "blame someone
  else".

## Output
A short statement of the workload ("80% of read IOPS come from the nightly export job, 4k random
reads, started 3 days ago") is often the whole diagnosis.
