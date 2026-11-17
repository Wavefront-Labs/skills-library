---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cost-aware-autoscaling-and-bin-packing
name: cost-aware-autoscaling-and-bin-packing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cost-optimization, bin-packing, spot-instances, karpenter, cluster-autoscaler, least-waste, right-sizing, vpa, finops, consolidation, reserved-instances]
level: advanced
status: docs-checked
description: "Where Kubernetes autoscaling spend actually goes, and the concrete levers (bin-packing, spot mix, right-sizing, consolidation) that cut it without hurting reliability."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/nodepools.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/disruption.md", "https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/", "https://github.com/kubernetes-sigs/descheduler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost-aware autoscaling and bin-packing

**Goal:** reduce the gap between "capacity paid for" and "capacity actually used," which on most
clusters is the single biggest lever — bigger than picking a cheaper instance family.

## 1. Where the waste actually comes from
Three independent sources, each needing a different fix:
- **Over-requested pods** — requests set well above real usage "to be safe," so nodes report
  high allocation but low utilisation. Fixed by VPA (run in `Off` mode and review the recommendations,
  or use `Recreate` or `InPlaceOrRecreate` once trusted; `Auto` is deprecated since VPA 1.4.0) — see
  `computing-software.cloud-infrastructure-engineering.kubernetes.vertical-pod-autoscaler-internals-and-modes`.
  This is usually the largest single lever and the one teams check last.
- **Poor bin-packing** — correctly-sized pods spread thinly across many partly-empty nodes
  instead of packed densely. Fixed by the node autoscaler's packing strategy (below).
- **Wrong purchasing instrument** — paying on-demand/list price for capacity that tolerates
  interruption (batch, stateless web tiers with good redundancy) when spot/preemptible or
  committed-use pricing would cover it for less; check your own provider's price list.

## 2. Bin-packing levers by autoscaler
- **Cluster Autoscaler**: `--expander=least-waste` (the default) picks the node group that leaves
  the least idle CPU (then memory) per scale-up decision. For scale-down, a node becomes a
  candidate when the larger of its CPU-request and memory-request ratios against allocatable is
  below `--scale-down-utilization-threshold` (default 0.5) and its pods can be moved to other nodes;
  by default a node must stay unneeded for 10 minutes. CA does not otherwise repack live workloads
  across nodes for you.
- **Karpenter**: `consolidationPolicy` accepts `WhenEmptyOrUnderutilized` (the default),
  `Balanced` (same candidates, but only consolidates when estimated savings justify the
  disruption) and `WhenEmpty`. It can remove or replace under-used nodes, including replacing a node
  with a cheaper one while pods run on it. The tradeoff is more node churn; tune `consolidateAfter`
  and `spec.disruption.budgets` (default one budget of `nodes: 10%`).
- **Descheduler** (a Kubernetes SIG project; it can run as a Job, CronJob or Deployment): its
  `HighNodeUtilization` plugin evicts pods from under-utilised nodes so they pack onto fewer nodes,
  and is intended to be used with node autoscaling to trigger scale-down. It must be used with the
  scheduler scoring strategy `MostAllocated`. It adds a moving part; weigh that against
  migrating to Karpenter.

## 3. Spot/preemptible mixing
- Spot/preemptible capacity is cheaper but can be reclaimed with short notice (AWS Spot gives a
  2 minute interruption notice). Only safe for workloads that
  tolerate pod disruption cleanly: stateless, fast-starting, with PodDisruptionBudgets that don't
  block eviction and no local-only state.
- Karpenter: allow `spot` and `on-demand` in the NodePool `karpenter.sh/capacity-type`
  requirement; Karpenter prefers `reserved`, then `spot`, then `on-demand`, and launches on-demand
  when no spot offering is available (a spot-only NodePool never launches on-demand). Interruption
  handling needs an SQS interruption queue wired up on AWS.
- Cluster Autoscaler: typically a dedicated spot node group plus `priority` expander or a
  separate scheduler policy (taints + tolerations steering preferentially to spot) — more manual
  than Karpenter's native mixed-type NodePool.
- Never put a workload's **entire** capacity on spot unless it tolerates total unavailability
  during a correlated interruption event (spot capacity for a whole instance family/AZ can be
  reclaimed simultaneously) — keep an on-demand floor for anything user-facing.

## 4. Right-sizing feedback loop
Bin-packing and spot mixing only help if requests reflect real usage — a node autoscaler packing
grossly over-requested pods tightly still wastes the same money, just on fewer, fuller-looking
nodes. Run VPA in `Off` mode continuously even on mature workloads, and feed its `target`
recommendation (stored in the VPA `.status.recommendation` field) into a quarterly request-size review; this is cheaper and lower-risk than trusting
automatic `Auto`/`Recreate` mode everywhere.

## Gotchas
- `least-waste` expander and Karpenter consolidation both optimize **current** pending/scheduled
  pods, not **future** ones — a cluster with predictable daily growth can still end up repacking
  itself into a corner right before a scale-up burst; pair with the predictive/scheduled scaling
  skill for known traffic shapes.
- Aggressive consolidation (`WhenEmptyOrUnderutilized`) increases the rate of pod rescheduling,
  which costs reliability (brief unavailability during eviction/drain) to save money — this is a
  real tradeoff, not a free win; quantify acceptable churn before enabling it broadly.
- Reserved/committed-use discounts and savings plans are a procurement decision orthogonal to
  autoscaler config — don't expect either CA or Karpenter to "know" about committed capacity; size
  NodePool/node-group `limits` to steer baseline load onto committed capacity and burst onto
  on-demand/spot deliberately (the `priority` expander in Cluster Autoscaler, NodePool `weight` in
  Karpenter).
- Memory is rarely over-provisioned by a careless default the way CPU is, but once over-requested
  it's harder to safely shrink (OOM risk) — right-size memory requests more conservatively than CPU.

## Verify
- [ ] A per-node utilisation report (`kubectl top nodes` or your observability stack) shows median
      CPU/memory allocation-vs-usage gap shrinking after each lever is applied, tracked over time,
      not just a point-in-time snapshot.
- [ ] Spot-tolerant workloads have a PDB that doesn't block eviction and no local-only state;
      confirmed by a forced interruption/drain test.
- [ ] Cost-allocation reporting attributes spend correctly across spot vs on-demand vs committed
      capacity after any node-autoscaler change.
- [ ] Consolidation churn rate (node replacements/day) is within an agreed tolerance, not
      discovered after the fact via a surprised on-call engineer.

## Checked

Checked 2026-10-27. Documentation checked: Cluster Autoscaler FAQ (autoscaler master), Karpenter v1.15 docs (nodepools, disruption), Kubernetes website main tree VPA concept page (v1.38 dev; v1.37 latest release; VPA 1.8.1 is the latest autoscaler release), descheduler README (master). Confirmed: `least-waste` is the default expander and its definition; `--scale-down-utilization-threshold` default 0.5 and 10 minute unneeded time; Karpenter consolidation policies, default budget, capacity-type preference; VPA modes and `Auto` deprecation; descheduler run modes and HighNodeUtilization/MostAllocated requirement. Fixed: the Cluster Autoscaler scale-down description (nodes below the utilisation threshold are candidates, not only empty nodes) and the stray draft wording about VPA. Removed as unconfirmed: the 60-90% spot discount figure and GCP preemptible notice time.

Method: documentation only; no commands were run.
