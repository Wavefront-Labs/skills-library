---
id: computing-software.qa-testing-engineering.performance-testing.workload-modelling-and-bottleneck-analysis
name: workload-modelling-and-bottleneck-analysis
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-testing, load-testing, stress-testing, soak-testing, spike-testing, capacity-testing, capacity-planning, workload-model, workload-modelling, littles-law, throughput, latency, percentiles, p95, p99, slo, sla, saturation, bottleneck-analysis, use-method, coordinated-omission, apm, observability, connection-pool, garbage-collection, performance-report]
level: advanced
status: draft
description: "Tool-agnostic performance testing: derive a workload model from production data, pick test types, size users with Little's Law, find the bottleneck with the USE method, report capacity."
sources: ["https://www.brendangregg.com/usemethod.html", "https://en.wikipedia.org/wiki/Little%27s_law", "https://sre.google/sre-book/service-level-objectives/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance testing: workload models, bottlenecks, capacity findings

**Goal:** answer a concrete question — *"Can the system handle peak with p95 < 800 ms
and < 1% errors, and where does it break?"* — with evidence. Scripting the load in a
specific tool is in computing-software.qa-testing-engineering.jmeter-k6.load-test-scripts-and-ramp-profiles.

## 1. Start from a question and an SLO
Write the acceptance criteria first, per key transaction: target throughput
(requests or business transactions per second), latency percentile (p95/p99), error
rate, and resource ceilings. Without them a test produces numbers, not a verdict.

## 2. Build the workload model from real data
From production logs/APM/analytics for the **peak hour** (not the daily average):
- **Transaction mix:** e.g. 70% browse, 20% search, 8% add-to-cart, 2% checkout.
- **Arrival rate** at peak, and the expected growth (e.g. ×1.5 for a sale + headroom).
- **Think time and session length**, payload sizes, cache-hit ratio, data cardinality
  (100k distinct products, not the same 10 — or every request hits a warm cache).
- Background load: batch jobs, cron, replication that also run at peak.

**Little's Law** sizes concurrency: *concurrent users = arrival rate × time in system*.
Example: 40 sessions/s arriving, each lasting 90 s of activity + think time → ~3,600
concurrent virtual users in a closed model. Or drive an **open model** (fixed arrival
rate) directly, which better matches public web traffic: closed models slow their
own request rate when the system slows, hiding the problem.

## 3. Choose the test types
| Type | Shape | Question it answers |
|---|---|---|
| Load | Ramp to expected peak, hold 30–60 min | Meets SLO at peak? |
| Stress | Keep stepping up past peak | Where and how does it break; does it recover? |
| Spike | Jump from normal to many × in seconds | Autoscaling, queues, cold caches |
| Soak / endurance | Moderate load for hours | Memory leaks, connection/file-handle leaks, log/disk growth |
| Capacity / step | Fixed steps, hold each | Max sustainable throughput per instance |

## 4. Prepare an environment whose results mean something
Production-like sizing and configuration (or a known scale factor), production-like
data volumes, the same observability as production, and isolation from other teams'
tests. Record versions and config with every run; change one thing between runs.

## 5. Watch the system, not just the load tool
Client metrics show *that* it's slow; server metrics show *why*. Use the **USE
method** (Brendan Gregg) on every resource: **U**tilisation, **S**aturation (queue
length, wait), **E**rrors — CPU, memory, disk I/O, network, and software resources:
thread pools, DB connection pools, locks, GC pauses, file descriptors.
Classic signatures:
- Throughput plateaus while latency climbs, CPU low → a queue or pool limit (DB
  connections, worker threads, rate limiter), or lock contention.
- CPU pegged on one tier → that tier is the bottleneck; profile it.
- Saw-tooth latency spikes → GC pauses; check heap sizing and allocation rate.
- Latency fine for an hour then degrades (soak) → leak or unbounded cache/table growth.
- Errors appear before latency rises → timeouts or a downstream dependency limit.
Fix the first bottleneck, rerun; the next one appears. Use APM traces to see which
span the time goes into.

## 6. Measurement traps
- **Averages hide pain**; report percentiles and the full distribution.
- **Coordinated omission:** a closed-loop tool waiting on slow responses sends fewer
  requests during stalls, under-reporting tail latency. Arrival-rate (open) executors
  mitigate it.
- Exclude ramp-up and warm-up from steady-state figures; JIT and caches distort the start.
- A saturated load generator invalidates the run — monitor it too.

## 7. Report the finding
One page: question and SLO; workload model and its data source; environment and
versions; result per transaction vs. SLO (pass/fail table with p95/p99, errors,
throughput); the bottleneck identified and evidence (graph of the resource
saturating); capacity statement ("one instance sustains ~420 req/s at SLO; peak needs
5 + 1 headroom"); risks and recommended fixes; what wasn't tested.

## Unconfirmed / notes
Method rather than a tool recipe, so nothing to run here; numbers in examples are
illustrative. Scale-factor extrapolation from a smaller environment is a judgement call
and frequently wrong for shared resources like databases — say so in the report.

## Verify
- [ ] SLOs written per transaction before the run.
- [ ] Workload mix, arrival rate and data volumes traced to production data.
- [ ] Server-side USE metrics captured for every tier during the run.
- [ ] Bottleneck named with evidence, not inferred from client latency alone.
- [ ] Report includes capacity number, headroom and untested risks.
