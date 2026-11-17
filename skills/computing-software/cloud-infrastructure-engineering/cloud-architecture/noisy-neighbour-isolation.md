---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.noisy-neighbour-isolation
name: noisy-neighbour-isolation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, noisy-neighbour-isolation, tenant-isolation, resource-quotas, per-tenant-throttling, multitenant-performance]
level: practitioner
status: docs-checked
description: "Prevent noisy neighbours in shared platforms: per-tenant quotas and throttles, resource limits, workload partitioning, tiered pools and per-tenant usage monitoring."
sources: ["https://learn.microsoft.com/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor", "https://kubernetes.io/docs/concepts/policy/resource-quotas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noisy neighbour isolation

The noisy neighbour problem occurs when one tenant's performance is degraded by another tenant's activity on shared
resources. It can happen with two tenants colliding at peak, or with many small tenants whose combined usage peaks.
Microsoft's guidance: sharing a resource carries a risk you cannot completely avoid, so treat it as a resource
governance problem and apply usage quotas, throttling and governance controls.

## Controls (service provider side)
- **Monitor** overall usage and per-tenant usage; alert on spikes; automate scaling where known problems exist. Log a
  tenant identifier in telemetry (for example Cosmos DB request units per request) so consumption can be aggregated
  per tenant. Failures for a tenant that is not itself consuming much can indicate it is a victim.
- **Resource governance**: quotas enforced through the Throttling or Rate Limiting patterns.
- **Provision more**: scale up, or scale out with extra shards (Sharding pattern) or stamps (Deployment Stamps).
- **Reserved or pre-provisioned capacity** that tenants can buy.
- **Balance tenants**: rebalance across instances or stamps; place tenants with complementary usage patterns together
  to flatten peaks; run non-time-sensitive background work asynchronously off-peak.
- **Downstream controls**: Kubernetes pod limits; Azure Container Apps workload profiles.
- **Restrict operations**: for example a maximum returnable record count or query time limit, or make heavy
  operations asynchronous.
- **Quality of service**: prioritise high-priority work under resource pressure.
- Be transparent with clients about throttling and quotas so they handle failures gracefully.

### Kubernetes
A ResourceQuota limits aggregate resource consumption per namespace (and object counts by kind). The admin creates at
least one per namespace; when quota covers cpu or memory, every new pod must set requests or limits for them or may be
rejected. A LimitRange can supply defaults. Protect the quota from deletion or edits, for example with a
ValidatingAdmissionPolicy.

## Client side
Handle throttling and retry transient failures, buy reserved capacity, move to a tier with stronger isolation (for
example Service Bus premium), or a single-tenant instance.

## Steps
1. Instrument per-tenant consumption.
2. Identify outlier tenants and their effect on others.
3. Apply limits with headroom and communicate them.
4. Offer upgrade paths (reserved or dedicated capacity).

## Gotchas
- Detection from the client side: a request that succeeds at other times but fails randomly; record baseline metrics.
- Limits without per-tenant metrics make throttling hard to explain.

## Verify
- [ ] Load test with one tenant far above normal: other tenants' latency stays within tolerance.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Azure Architecture Center Noisy Neighbor antipattern and the Kubernetes Resource Quotas page.
Removed: the AWS SaaS whitepaper source (page returned empty), 429/Retry-After, API gateway usage-plan, per-tenant
storage prefix, database resource-governor and "top 1%" claims (not in the cited pages).
