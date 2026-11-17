---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.compute-resource-consolidation
name: compute-resource-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-implementation-patterns, compute-resource-consolidation, bin-packing, kubernetes, multi-tenant-compute, cost-optimisation]
level: practitioner
status: docs-checked
description: "Consolidate multiple tasks onto shared compute units: grouping criteria by scaling, lifetime and resource profile, isolation trade-offs, and when not to consolidate."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/compute-resource-consolidation", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://karpenter.sh/docs/concepts/disruption/", "https://learn.microsoft.com/azure/app-service/manage-scale-per-app"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute resource consolidation

## Steps
1. **Inventory** tasks that are often idle or not cost effective in their own computational unit. Each unit consumes
   chargeable resources even when idle or lightly used.
2. **Group by compatible characteristics** (Azure pattern guidance):
   - similar scalability, lifetime and processing requirements; do not group conflicting scaling needs (a rare
     queue poller with a bursty high-volume handler)
   - different resource profiles: a compute-intensive task can share with a memory-heavy one, but two compute-intensive
     or two memory-heavy tasks should not; long-running compute-intensive tasks should not share a unit
   - tolerable release coupling: redeploying a unit stops and restarts every task in it
   - matching security needs: shared security context and a larger attack surface
3. **Observe first**: consolidate only systems that have run in production long enough to build a resource heat map.
4. **Consolidation targets** (Azure examples): shared App Service plans, shared Container Apps environments, AKS nodes
   grouped into node pools by CPU or memory needs, a shared VM set for tenants, and consumption-based serverless that
   scales to zero.
5. **Kubernetes**: set container resource requests and limits. The scheduler uses requests to place pods; the kubelet
   enforces limits (CPU by throttling, memory by OOM kills). Karpenter consolidation can remove empty or underutilised
   nodes, governed by `consolidationPolicy` (`WhenEmpty`, `WhenEmptyOrUnderutilized`) and `consolidateAfter`.
6. **App Service**: per-app scaling places chosen apps on a subset of plan workers; it is fixed and does not respond to
   demand, and is available on Standard, Premium, Premium V2, Premium V3 and Isolated tiers.
7. **Measure** utilisation and cost before and after; reconsider if tenants interfere with each other.

## Gotchas
- A failing task can affect others: a task that fails to start can fail the unit's whole startup logic.
- The unit may be recycled by the infrastructure; long-running tasks need checkpointing or protection from recycling.
- Consolidation adds code complexity, making testing, debugging and maintenance harder.
- Not suitable for critical fault-tolerant operations, highly sensitive data needing its own security context, or
  tasks that need an isolated environment.

## Verify
- [ ] Each consolidated unit documents its tasks, resource profile and owners.
- [ ] Utilisation up and cost per workload down, with no rise in cross-task incidents.

## Checked
2026-11-08. Confirmed against the Azure Compute Resource Consolidation pattern page (grouping criteria, considerations,
when to use and not use, hosting examples, heat-map note), the Kubernetes container resources page (requests drive
scheduling, kubelet enforces limits, CPU throttling, memory OOM kills), the Karpenter disruption page (consolidation,
`consolidationPolicy`, `consolidateAfter`; policy value names read from the page) and the App Service per-app scaling
page (tiers, fixed placement). Removed: `ResourceQuota`, `LimitRange`, priority classes, network policy advice and
per-workload identity advice (not on these pages).
Method: documentation only; no commands were run.
