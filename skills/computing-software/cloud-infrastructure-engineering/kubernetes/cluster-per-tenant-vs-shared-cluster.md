---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-per-tenant-vs-shared-cluster
name: cluster-per-tenant-vs-shared-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy, cluster-per-tenant, shared-cluster, blast-radius, cost-optimization, cluster-sprawl, control-plane-cost, compliance-isolation, fleet-sizing]
level: sme
status: docs-checked
description: "Decide between dedicated clusters per team and a shared multi-tenant cluster by weighing cost, blast radius, and operational load."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://github.com/loft-sh/vcluster"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster-per-tenant vs shared cluster — the real cost/isolation tradeoff

**Goal:** make this decision with numbers, not instinct. It's the axis every other
multi-tenancy skill in this set sits on: namespace soft multi-tenancy
(`computing-software.cloud-infrastructure-engineering.kubernetes.namespace-soft-multi-tenancy`)
and vcluster (`computing-software.cloud-infrastructure-engineering.kubernetes.vcluster-virtual-clusters`)
are ways to get *some* of cluster-per-tenant's isolation without its cost; this skill
is about recognizing when those middle grounds aren't enough and dedicated clusters are
the right call — or when they're cluster sprawl dressed up as "isolation."

## 1. Cost of cluster-per-tenant
- **Control-plane cost**: N tenants means N control planes, not amortized across a shared pool.
  On managed Kubernetes check your provider's per-cluster pricing; on self-hosted clusters the
  etcd and API server footprint is repeated for every tenant.
- **Node utilization**: dedicated clusters mean dedicated (or minimum-sized) node
  pools per tenant — bin-packing happens *within* a tenant's nodes only, so aggregate
  cluster utilization across the fleet is typically lower than one shared pool's
  bin-packing across all tenants' varying load patterns. A tenant with a predictable
  low baseline and occasional spikes pays for spike-sized capacity 24/7 unless
  autoscaling is tuned per cluster (N times the tuning work).
- **Operational load**: N clusters means N sets of upgrades, N cert rotations, N
  monitoring pipelines to keep healthy — even with CAPI/Fleet automating the mechanics
  (`computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-fundamentals`,
  `computing-software.cloud-infrastructure-engineering.kubernetes.rancher-fleet-management`),
  there is more to go wrong and more alerts to triage, and a bad rollout can still hit
  every cluster if the fleet GitOps config is shared.

## 2. When dedicated clusters are actually worth it
- **Compliance/regulatory isolation** that requires separate control planes, separate audit logs
  or separate encryption keys at the infrastructure level — namespace-based isolation shares the
  control plane and nodes, and virtual clusters may share worker nodes and kernels depending on
  the mode, which some requirements do not accept. Confirm the actual requirement text, not a
  guess — "needs isolation" often means namespace-level is fine; read the standard.
- **Mutually adversarial tenants** (e.g. a platform sold to external customers who are
  business competitors) where a container-escape or node-level side-channel blast
  radius must not include another tenant's workload under any circumstance.
- **Wildly different scaling/version/extension needs** — a tenant needing a custom
  kernel module, a GPU node pool nobody else uses, or an EOL Kubernetes minor version
  for a legacy dependency, where coexisting in a shared cluster's upgrade cadence isn't
  viable.
- **Blast-radius containment for platform mistakes**, not just tenant-vs-tenant: a bad
  cluster-wide CRD/webhook/CNI change on a shared cluster can take down every tenant at
  once; separate clusters cap that to one tenant (at the cost of N times the surface
  area for that mistake to occur on in the first place).

## 3. Middle grounds to try first
- Namespace soft multi-tenancy + policy enforcement for internal, trusted teams with
  similar needs — cheapest, usually sufficient.
- vcluster when a tenant needs cluster-scoped RBAC/CRDs but isolation requirements
  don't rise to regulatory/adversarial level.
- Separate **node pools** (not separate clusters) within one cluster when the actual
  concern is noisy-neighbor/kernel-level contention rather than control-plane isolation
  — much of cluster-per-tenant's benefit for a fraction of its control-plane cost.
- Separate clusters **by environment tier** (prod/staging) even when tenants share a
  cluster within a tier — a common hybrid that caps blast radius for the riskiest axis
  (a staging mistake can't touch prod) without full cluster-per-tenant sprawl.

## Gotchas
- "Cluster sprawl" creeps in gradually — each new tenant's dedicated cluster seems
  justified in isolation, but the aggregate fleet becomes unmanageable (hundreds of
  clusters, each slightly configured differently) without someone tracking the total
  cost and operational burden against the actual isolation requirement that drove each one.
- Reversing this decision later (merging dedicated clusters back into a shared one, or
  splitting a shared cluster apart) is a real migration project, not a config flip —
  decide with the multi-year trajectory in mind, not just today's tenant count.
- "It's more secure" is not sufficient justification by itself — name the specific
  threat/compliance requirement a dedicated cluster addresses that a vcluster or
  policy-enforced namespace does not, or the extra cost has no counterpart benefit.

## Verify
- [ ] The specific isolation requirement driving a cluster-per-tenant decision is
      written down (compliance clause, threat model, scaling need) — not just "more
      isolation is better."
- [ ] A cost model compares N-dedicated-clusters' node utilization and control-plane
      overhead against a shared-cluster alternative using real tenant load data, not
      assumed averages.
- [ ] The operational cost (upgrade cadence, monitoring, on-call surface) of N clusters
      is budgeted, not just the infrastructure bill.
- [ ] A middle-ground option (vcluster, node-pool separation, policy-enforced
      namespaces) was evaluated and explicitly rejected with a reason, not skipped.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026
- Confirmed in Kubernetes' multi-tenancy page that creating separate clusters per tenant and sandboxing are the stronger options when node-level or kernel isolation is a concern, that node isolation (dedicated nodes with taints) is easier to reason about for billing than sandboxing, and that virtual control planes address conflicts over cluster-scoped objects such as CRDs and webhooks.
- Replaced the unverifiable source title with the Kubernetes multi-tenancy page and removed the unsupported statements about named compliance regimes and universal per-cluster control-plane fees; the cost and operations points that remain are reasoning to be checked against your own pricing and tenant load, as the Verify list says.

Method: documentation only; no commands were run.
