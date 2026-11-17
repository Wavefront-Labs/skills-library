---
id: computing-software.qa-testing-engineering.performance-testing.capacity-planning-and-soak-testing
name: capacity-planning-and-soak-testing
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [capacity-planning, soak-testing, endurance-testing, memory-leak, resource-leak, scalability-testing, horizontal-scaling, vertical-scaling, autoscaling, headroom, growth-projection, connection-leak, file-descriptor-leak, cache-eviction, long-running-test]
level: advanced
status: draft
description: "Find leaks and degrade-over-time failures with multi-hour soak tests, and turn load-test results into a defensible capacity/headroom number for the next 6-12 months of growth."
sources: ["https://sre.google/sre-book/service-level-objectives/", "https://www.usenix.org/legacy/publications/library/proceedings/usenix01/full_papers/weaver/weaver.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity planning and soak testing

**Goal:** answer two questions a single short load test cannot: "does this system
degrade if it runs under load for hours/days?" and "how much more traffic can we
take before we need to scale, and by when?"

## 1. Soak (endurance) testing — what a short test can't find
Run moderate (not peak) load continuously for 4-24+ hours. The point isn't to
break the system under volume — it's to catch failures that only accumulate over
time, invisible in a 10-minute run:
- **Memory leaks**: a slow, steady upward trend in heap/RSS that a 10-minute test
  reads as noise. Plot memory over the full soak; a monotonic climb (not sawtooth)
  that doesn't plateau is a leak, not normal GC behavior.
- **Connection/file-descriptor leaks**: pooled connections or handles not released
  on error paths, invisible until the pool exhausts hours in — check `ulimit`/pool
  metrics over time, not just at the end.
- **Cache/log-driven disk fill**: an unbounded cache or log file that eventually
  fills disk and takes the process down with it — a failure mode purely a function
  of elapsed time, not request rate.
- **Clock/counter overflow and token expiry edge cases**: a session or token that
  expires mid-test exposes a renewal path a short test never exercises.
Flat, stable resource graphs for the full duration = pass. Any resource metric
that climbs without bound = fail, even if latency and error rate stayed fine the
whole time — soak tests fail on trend, not on a threshold crossed at one instant.

## 2. Scalability testing — does adding capacity actually help?
Run the same workload at two or more instance counts (e.g., 2 vs. 4 app servers)
and check whether throughput scales near-linearly. If doubling instances yields
much less than double throughput, something doesn't scale horizontally — a shared
bottleneck (single DB, a global lock, a sticky-session load balancer forcing
uneven distribution) is capping it regardless of app-tier capacity. Find that
shared resource before promising "just add more servers" as the scaling plan.

## 3. From load-test results to a capacity number
1. Establish the current validated ceiling: highest load level that still met the
   SLO (e.g., p95 < 800ms, errors < 1%) in testing.
2. Get current real peak traffic from production monitoring (not an estimate).
3. **Headroom** = validated ceiling ÷ current real peak. A commonly used target is
   ≥ 1.5-2x headroom over current peak before action is needed — the exact number
   is a business risk decision, not a technical constant; state it explicitly in
   the report rather than implying a universal rule.
4. Apply the business's own growth projection (seasonal traffic, marketing
   calendar, YoY growth rate) to project when current peak will reach the
   validated ceiling, and recommend action by that date, not "soon."

## 4. Autoscaling needs its own test
If the system autoscales, test the **scaling response**, not just the scaled-out
steady state: ramp load faster than the autoscaler's reaction time and measure how
long requests queue/fail during the lag. A system that scales fine once warm can
still fail a sudden spike if scale-out takes 3 minutes and the spike peaks in 30
seconds — report the lag explicitly, it's a capacity property on its own.

## Unconfirmed / notes
Headroom target (1.5-2x) is a common industry heuristic, not derived here from any
specific SLA; always confirm the acceptable risk level with the business owner.

## Verify
- [ ] Soak test run long enough to distinguish a trend from noise (hours, not minutes).
- [ ] Memory, connections, file descriptors, disk all plotted over the full duration.
- [ ] Scalability checked at 2+ capacity levels, not assumed linear from one data point.
- [ ] Headroom number ties to a real measured peak and a stated target ratio.
- [ ] Autoscaling lag measured under a sudden ramp, not just steady-state capacity.
