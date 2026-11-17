---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.latency-budget
name: latency-budget
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, latency-budget, tail-latency, performance-requirements, critical-path]
level: practitioner
status: draft
description: "Set latency budgets per tier on the critical request path: derive from the user-facing SLO, allocate per hop, account for tail latency and fan-out, and monitor."
sources: ["https://sre.google/sre-book/service-level-objectives/", "https://research.google/pubs/the-tail-at-scale/", "https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-targets"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Latency budgets per tier

## Steps
1. **Start from the user-facing target**: e.g. p95 page API 300 ms, p99 800 ms, measured at
   the edge or client.
2. **Draw the critical path**: edge/CDN, load balancer, gateway, service A, its downstream
   calls (DB, cache, service B), serialisation. Mark parallel vs sequential calls.
3. **Allocate** budget per hop for sequential segments; parallel fan-out costs the slowest
   branch. Keep 10-20% unallocated for network variance and growth.
4. **Tail amplification**: a request fanning out to N backends sees roughly the backend's
   p(1 - 1/N)-ish tail; with 100 backends, the user's median hits each backend's p99.
   Budget fan-out services at p99/p99.9, not p50 (Dean and Barroso, The Tail at Scale).
5. **Set timeouts from budgets**: each hop's timeout slightly above its budgeted p99, and
   less than the caller's remaining budget (propagate deadlines, e.g. gRPC deadlines).
6. **Monitor per hop** with distributed tracing; alert on budget breach trends, not single spikes.

## Gotchas
- Averages hide tails; always budget percentiles.
- Cross-region calls (tens of ms each) blow budgets quickly; keep the critical path in-region.

## Verify
- [ ] Budget table per hop with owners.
- [ ] Traces show each hop's p99 within its budget.
