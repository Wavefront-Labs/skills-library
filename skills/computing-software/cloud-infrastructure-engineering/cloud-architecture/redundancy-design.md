---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.redundancy-design
name: redundancy-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, redundancy-design, n-plus-one, active-active, active-passive, zone-redundancy, redundancy-at-every-layer]
level: practitioner
status: docs-checked
description: "Design redundancy layer by layer (compute, data, network, managed services) with spare capacity for failure and checks that failover actually works."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/redundancy", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/use-fault-isolation-to-protect-your-workload.html", "https://docs.cloud.google.com/architecture/framework/reliability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redundancy design at every layer

The Azure Well-Architected recommendation RE:05 is to add redundancy at different levels,
especially for critical flows, to meet your reliability targets. The AWS Well-Architected
reliability pillar groups the same idea under fault isolation (REL10: deploy the workload to
multiple locations, automate recovery for components constrained to a single location, use
bulkhead architectures). Google's reliability pillar lists "build highly available systems
through resource redundancy" as a core principle.

## Layer checklist (Azure guidance)
| Layer | Redundancy |
|---|---|
| Managed services | Prefer serverless, SaaS and PaaS that add redundancy transparently; global services such as Entra ID, Azure DNS and Key Vault need no redundancy configuration |
| Compute | Prefer services with built-in multi-instance support; keep the compute layer stateless; design and test the scaling strategy to match the redundancy approach |
| Data | Replicate across regions; know the built-in replication of your platform services; choose synchronous or asynchronous replication per need; automate failover after a database instance failure; partition data so one failed shard affects only a subset |
| Networking | Hub-and-spoke or Virtual WAN topology; global or zone-redundant load balancing; enough IP address space for scale-out; watch outbound port limits; check that SKU supports zone redundancy; resilient DNS design |
| Whole workload | Deployment stamps: self-contained units, active-active or active-passive, that contain blast radius |
| Operations | Apply CanNotDelete locks to data stores, DNS zones and routing layers so deletion cannot remove redundancy; locks block deletion, not changes, and do not replace backups |

## Sizing
- Redundancy for reliability needs spare capacity. Azure's example: two nodes at 60% utilisation
  each cannot absorb a failure, because the survivor would need to run at 120%; add another node.
  The spare capacity must last as long as it takes to recover the failed nodes.
- Azure's alternative: deploy fewer replicas so the flow runs degraded until the problem is fixed,
  because large-scale failures are rare and full replicas are costly.
- Trade-offs the page names: more redundancy costs more; spreading across zones adds latency;
  per-flow designs add complexity.

## Steps
1. List components per critical flow; mark single instances and single-zone resources.
2. Choose redundancy per component to match the reliability target and cost.
3. Decide active-active (zero-downtime goal, higher cost and complexity), warm spare (shortest
   recovery of the active-passive options, highest cost of them) or cold spare (lower cost,
   longer recovery), per the Azure page.
4. Use availability zones for low-latency independent datacentres and distant regions for
   large-scale disasters; the Azure page notes regional events can still affect all zones.
5. Test by failing an instance or zone and measure recovery.

## Gotchas
- Redundant compute but a single-instance database, a single DNS or routing layer, or port
  exhaustion on a shared outbound path.
- Active-passive standby that has never taken traffic.

## Verify
- [ ] No single-instance component in any critical flow (or accepted in writing).
- [ ] Survivors can carry the load after the largest planned loss.
- [ ] Failure test passed at realistic load.

## Checked
2026-11-08. Confirmed against the Azure Well-Architected redundancy page (RE:05, layer guidance,
60%/120% example, deployment stamps, active-active vs active-passive options, availability zones,
locks), the AWS reliability pillar fault isolation overview (REL10 best-practice titles only; the
page is a short index) and the Google Cloud reliability pillar overview (core principle list
only). Removed: the N+1 and 150% zone sizing arithmetic, the specific per-provider product names
and the dual-NAT-gateway advice (not stated in the pages).
Method: documentation only; no commands were run.
