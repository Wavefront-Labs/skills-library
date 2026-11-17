---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cold-cache-and-slow-start-mitigation
name: cold-cache-and-slow-start-mitigation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cold-cache-mitigation, slow-start-protection, cascading-failures, cache-warming, envoy-slow-start, jit-warmup]
level: advanced
status: docs-checked
description: "Protect services from cold starts and cold caches: overprovisioning for cache misses, slow-start ramp in the load balancer, and staged traffic after failover."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/slow_start", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html#slow-start-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cold cache and slow start mitigation

SRE Book "Slow Startup and Cold Caching": processes are often slower right after starting, because of
required initialization (for example setting up connections on the first request needing a backend) and
runtime improvements in some languages such as Java (JIT compilation, hotspot optimization, deferred class
loading). Some binaries are also less efficient with empty caches: where most requests are served from
cache, a completely empty cache makes 100% of requests costly. Scenarios: turning up a new cluster, returning
a cluster to service after maintenance (cache may be stale), and restarts.

## Know your cache dependence
The book distinguishes a **latency cache** (the service can sustain its expected load with an empty cache)
from a **capacity cache** (it cannot). New caches should be latency caches or engineered well enough to work
as capacity caches; some caches wind up as hard dependencies. Measure backend load at zero hit rate against capacity.

## Mitigations
1. **Overprovision** the service for a cold cache (book).
2. **General cascading-failure techniques** (book): reject requests when overloaded or degraded, and test
   behaviour after events such as a large restart.
3. **Move the cache to a separate binary** such as memcache so it survives server restarts and is shared
   between servers, at the cost of another RPC and slight latency (book).
4. **Slow start at the load balancer**: ramp a new backend's share of traffic.
   - Envoy slow start mode progressively increases traffic to newly added upstream endpoints; it is set per
     cluster with a slow start window in seconds, and is supported for round robin, least request and
     client-side weighted round robin. It is most effective when few new endpoints come up (a scale event) and
     not very effective when all endpoints are new (a new deployment). Check the page for aggression and
     minimum-weight options. Not recommended for low traffic or a high number of endpoints.
   - AWS Application Load Balancer slow start mode: targets get time to warm up before receiving a full share;
     the load balancer linearly increases requests to a target during the duration; it cannot be combined with
     the least outstanding requests or weighted random routing algorithms. Newly registered targets enter slow
     start only if at least one healthy target is not in slow start.
5. **Ramp traffic gradually into a recovered cluster or region** instead of flipping DNS or the load balancer fully (practice).
6. **Request coalescing** so a cold key triggers one backend fetch, not many (practice).

## Readiness gating
Report ready only after warmup completes, and give the startup probe enough time for the worst-case warmup.

## Gotchas
- Mass restarts (config push to all pods at once) cold-start the whole fleet; roll gradually.
- Per Envoy, slow start does little if all backends are new at once; ramp at the global load balancer instead.
- Before restarting servers during a cascading failure, make sure it will not simply shift load or amplify a cold-cache problem (book).

## Verify
- [ ] Measured backend load at cold cache vs capacity documented.
- [ ] Restart test: latency of a fresh pod within SLO after the slow-start window; no backend overload.

## Checked
2026-11-01. Confirmed against the SRE Book cascading-failures chapter (cold cache causes, latency versus capacity
cache, overprovision, memcache), the Envoy slow-start page and the ALB target-group attributes page (slow start
behaviour and restrictions). Removed: the Envoy YAML values, ALB attribute name and 120 s duration, the
10/25/50/100 percent ramp, the Go snippet and the startup-probe formula (not on fetched pages).
Method: documentation only; no commands were run.
