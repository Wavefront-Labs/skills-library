---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dependency-criticality
name: dependency-criticality
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, dependency-criticality, hard-dependencies, soft-dependencies, dependency-map, control-plane-vs-data-plane, third-party-dependencies]
level: advanced
status: draft
description: "Classify each dependency as hard or soft, remove unnecessary hard ones, avoid control-plane dependencies in the recovery path, and document third-party dependency risks."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_withstand_component_failures_static_stability.html", "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/", "https://learn.microsoft.com/azure/well-architected/reliability/identify-flows"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency criticality

## Steps
1. **List dependencies** per service: internal services, data stores, identity, DNS, secrets,
   config stores, third-party APIs, provider control planes (APIs that create/modify resources).
   Use tracing service maps plus code review.
2. **Classify**:
   - *Hard*: the request cannot succeed without it (primary DB for writes).
   - *Soft*: the request can succeed degraded (recommendations, analytics events, avatars).
3. **Make soft dependencies actually soft**: timeouts, async/fire-and-forget via queue, cached
   fallbacks, feature flags to disable. Test by blocking them.
4. **Reduce hard dependencies**: cache auth decisions/JWKS, pre-provision capacity, local copies
   of config, avoid synchronous calls to non-critical services in the hot path.
5. **Control plane vs data plane**: data planes (serving requests) are usually more available
   than control planes (create/update APIs). Recovery that requires launching resources, changing
   DNS records or IAM during an event is fragile — prefer pre-provisioned, statically stable designs.
6. Third parties: record their SLA, status page, support path, and what you do when they're down.

## Gotchas
- Startup dependencies: a service that can't start without the config service turns a config
  outage into a full outage on the next deploy/scale-out.
- Circular dependencies between services prevent cold start of the system — check bootstrap order.

## Verify
- [ ] Dependency table with hard/soft and fallback per dependency.
- [ ] Blocking each soft dependency in staging leaves core flows working.
