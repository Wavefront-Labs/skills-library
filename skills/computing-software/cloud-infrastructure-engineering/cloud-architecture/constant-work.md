---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.constant-work
name: constant-work
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, constant-work, bimodal-behaviour, static-stability, push-full-state, reliability-pattern]
level: practitioner
status: draft
description: "Apply the constant-work pattern (full-state push, fixed-rate polling) so systems do the same work in normal and failure modes and avoid bimodal overload."
sources: ["https://aws.amazon.com/builders-library/reliability-and-constant-work/", "https://aws.amazon.com/builders-library/static-stability-using-availability-zones/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constant work and avoiding bimodal behaviour

## The problem
Bimodal systems behave differently under stress: a config system that pushes deltas does little
work normally but floods when many things change at once; a cache-backed service suddenly hits the
database when the cache empties. The rarely exercised mode fails exactly when needed.

## Constant-work techniques
- **Push full state on a fixed schedule** instead of deltas on change (AWS Route 53 health
  checks and Hyperplane config: the whole config file is pushed every few seconds whether it
  changed or not).
- **Fixed-rate polling** rather than event storms on change.
- **Fixed-size work units**: process the same batch size every cycle.
- **Pre-provisioned capacity** sized for the failure case (static stability).
- **Cache warming / constant read-through rate** so the backing store always sees realistic load.

## Trade-offs
Constant work wastes resources in the steady state (it does the expensive thing always). Use it
for control planes and critical config distribution where the payload is bounded and predictability
matters more than efficiency.

## Steps
1. Identify components whose load spikes during failures (config fan-out, cache misses, retries,
   reconnect storms).
2. Redesign so steady-state load equals worst-case load, or cap worst-case.
3. Load test the failure mode explicitly.

## Verify
- [ ] Mass-change scenario produces the same load profile as normal operation.
