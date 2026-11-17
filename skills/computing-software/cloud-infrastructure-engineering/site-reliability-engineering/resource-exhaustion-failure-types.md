---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.resource-exhaustion-failure-types
name: resource-exhaustion-failure-types
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [resource-exhaustion-types, fd-exhaustion, thread-exhaustion, cascading-failures, cpu-saturation, memory-exhaustion, gc-death-spiral]
level: advanced
status: docs-checked
description: "Recognise each resource-exhaustion path to cascading failure (CPU, memory, threads, file descriptors, dependencies) by its symptoms and metrics, and the guard for each."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://man7.org/linux/man-pages/man2/getrlimit.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource exhaustion types

SRE Book "Addressing Cascading Failures" lists how running out of each resource leads to failures that
spread. Know the symptom of each so you can name it quickly during an incident.

## CPU
Effects: more in-flight requests (queues grow), larger queues -> more memory, thread starvation, missed
RPC deadlines, reduced CPU caching benefit, health checks time out.
Detect: CPU use near its limit and CPU throttling from your metrics system.
Guard: load shedding before 100%, CPU limits that match requests, queue bounds.

## Memory
Effects: tasks OOM-killed; GC thrash (more GC -> less CPU -> slower requests -> more memory: the
**GC death spiral**); cache hit rate drops (smaller caches) -> more backend load.
Detect: memory use against its limit, OOM kills, and GC pause metrics.
Guard: bounded queues/caches, memory limits with headroom, shed load on heap pressure.

## Threads
Effects: thread-per-request servers stall when pool exhausted; health checks queued behind work and fail;
in extreme cases the server runs out of process IDs.
Detect: thread count, pool active equal to max, queue length.
Guard: bounded pools with bounded queues; reject when queue full; separate health-check handling.

## File descriptors
Effects: cannot initialise network connections, which can fail health checks.
Detect: open descriptors against the process limit (see getrlimit(2) for `RLIMIT_NOFILE`).
Guard: raise limits deliberately, pool connections, close leaks, idle connection timeouts.

## Dependencies among resources
Exhaustion of one leads to others, so the observed bottleneck may not be the cause: e.g. a slow DB ->
more in-flight requests -> more threads -> more memory -> GC -> CPU. Trace back along the chain to the
first resource that changed.

## Service unavailability from exhaustion
Once some tasks crash, load shifts to others, they exhaust, and so on (the cascade). The LB may also mark
overloaded tasks unhealthy, shrinking capacity further (see `health-check-cascade-prevention`).

## Gotchas
- Container limits differ from host limits; check the cgroup values, not `free -m`.

## Verify
- [ ] Dashboard row per resource with saturation metric and limit.
- [ ] Alerts on descriptor, memory and CPU saturation, with thresholds you set from the limits.

## Checked
2026-11-01. Confirmed in SRE Book Addressing Cascading Failures (CPU, memory incl. the GC death spiral, threads incl. process IDs, file descriptors, dependencies among resources, load shifting to other tasks) and the getrlimit(2) man page for `RLIMIT_NOFILE`. Removed the metric names and queries, the 80% and 25% thresholds and the 1024 default, which were not in the fetched pages.
Method: documentation only; no commands were run.
