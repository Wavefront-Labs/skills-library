---
id: computing-software.software-engineering.concurrency.capacity-planning-with-littles-law
name: capacity-planning-with-littles-law
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, benchmarking, littles-law, capacity-planning, queueing-theory, utilization, pool-sizing, headroom, mm1-queue]
level: advanced
status: verified
description: "Size thread pools, connection pools and instance counts with Little's law and basic queueing theory, and see why latency explodes as utilisation approaches 100%."
sources: ["https://en.wikipedia.org/wiki/Little%27s_law", "Systems Performance, 2nd ed. (Gregg), ch2.6 Modeling (queueing theory)", "The Art of Computer Systems Performance Analysis (Jain), Part VI Queueing Models", "https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity planning with Little's law

**Goal:** back-of-envelope numbers for how many workers, connections and instances a
target load needs, before load testing confirms them.

## Little's law
`L = lambda x W`
- L: average number of items in the system (concurrency in flight)
- lambda: arrival rate (requests/s)
- W: average time in system (latency, s)
Holds for any stable system regardless of distribution.

## Applications
**Concurrency needed**: 2,000 req/s x 0.050 s = 100 requests in flight on average.
If each needs a thread for its whole duration, you need >= 100 threads (plus headroom
for variance; size for p99, not mean).

**DB connection pool**: requests hold a connection for 8 ms of DB time each, at 2,000
req/s -> 2,000 x 0.008 = 16 connections busy on average. A pool of ~20-30 suffices;
a pool of 200 just moves queueing into the database (HikariCP's pool sizing guidance:
small pools near `(core_count * 2) + effective_spindle_count` for the DB server often perform best; HikariCP's wiki says core count excludes hyperthreads and effective spindles are zero when the active data set is fully cached).

**Max throughput of a pool**: 50 workers, 200 ms per job -> max 50 / 0.2 = 250 jobs/s.
Arrivals above that grow the queue without bound.

**Instances**: one instance sustains 400 req/s at target latency (measured); peak 3,000
req/s -> 8 instances, plus N+1/N+2 for failures and deploys, plus growth headroom.

## Utilisation and latency (M/M/1 intuition)
For a single queue with random arrivals: `response time = service time / (1 - utilisation)`.
| Utilisation | Response time multiple |
|---|---|
| 50% | 2x |
| 80% | 5x |
| 90% | 10x |
| 95% | 20x |
So plan to run busy resources at 60-75%, not 95%. Variance makes it worse; multiple
servers (M/M/c) degrade more gracefully, which is why pooling helps. Computed with the Erlang C formula (response time as a multiple of service time): at 80% utilisation 1 server gives 5.0x, 4 servers 1.75x, 16 servers 1.10x; at 95% they give 20x, 5.5x and 2.0x. A simulated M/M/1 queue (400k jobs) gave 1.99x, 4.94x, 10.9x and 19.7x at 50, 80, 90 and 95%.

## Workflow
1. Measure service time per resource (profiling, DB time, downstream latency).
2. Forecast peak arrival rate (traffic history x growth x event peaks).
3. Compute concurrency and resource counts with Little's law; apply utilisation target.
4. Validate with an open-model load test; adjust.
5. Re-plan when latency or traffic mix changes.

## Verify
- [ ] Pool sizes and instance counts documented with the calculation behind them.
- [ ] Load test at forecast peak keeps resource utilisation below the target and latency within SLO.
