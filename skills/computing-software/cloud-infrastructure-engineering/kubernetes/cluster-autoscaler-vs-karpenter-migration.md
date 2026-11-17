---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-autoscaler-vs-karpenter-migration
name: cluster-autoscaler-vs-karpenter-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-autoscaler, karpenter, migration, node-groups, asg, eks, cutover, taints, coexistence]
level: advanced
status: docs-checked
description: "When to pick Cluster Autoscaler vs Karpenter, and how to run both briefly and cut over without double-provisioning or orphaned node groups."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/getting-started/migrating-from-cas/_index.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/nodepools.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/disruption.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster Autoscaler vs Karpenter, and migrating between them

**Goal:** make the choice on real architectural differences, not vendor marketing, and if
migrating, do it without a window where pods lose capacity or nodes are left unowned.

## 1. The core architectural difference
- **Cluster Autoscaler** scales **node groups**: pre-configured groups that usually map to a cloud
  resource group such as an ASG, MIG or VMSS. When provisioning it adds nodes to the group that best
  fits the pending pods, and when consolidating it selects specific nodes to remove. It needs an
  explicit integration per cloud provider (see the provider list in the Cluster Autoscaler repo).
- **Karpenter** provisions from **NodePool** configuration and manages the whole node lifecycle. It
  launches individual cloud resources (usually single VMs) and does not rely on resource groups.
  The Karpenter core is cloud-neutral, but each cloud needs its own provider implementation; the
  AWS provider is the one documented at karpenter.sh. Check the implementations list in the
  kubernetes-sigs/karpenter README for your cloud before committing.
- Consequence: Cluster Autoscaler can only grow the groups you defined; Karpenter chooses instance
  types per batch of pending pods within the NodePool's `requirements`. Measure scale-up latency on
  your own workload rather than trusting published comparisons.

## 2. When Cluster Autoscaler still wins
- Clouds without a Karpenter provider you are willing to run.
- Organisations that model capacity as ASGs for cost or compliance reporting and want autoscaling to
  stay inside those boundaries exactly.

## 3. When Karpenter wins
- Heavy spot usage with diverse instance-type tolerance: one NodePool can allow many instance types
  and capacity types. When a NodePool allows several capacity types Karpenter prefers `reserved`,
  then `spot`, then `on-demand`, and falls back only to types the NodePool allows.
- Workloads with very different shapes (GPU batch plus small web pods), where covering every
  combination with fixed node groups becomes unmanageable.
- Active consolidation is acceptable: with `consolidationPolicy: WhenEmptyOrUnderutilized` (the
  default) Karpenter removes or replaces under-used nodes, which suits stateless workloads that
  tolerate rescheduling.

## 4. Cutover sequence (from the Karpenter migration guide)
The Karpenter guide for migrating from Cluster Autoscaler on AWS EKS does this:
1. Create the IAM roles, tag the subnets and security groups, and allow the Karpenter node role to
   join the cluster.
2. Deploy Karpenter with node affinity so its own pods run on an **existing** node group
   (`karpenter.sh/nodepool` `DoesNotExist` plus the node group label). The controller must not depend
   on nodes it provisions.
3. Create a default NodePool.
4. Optionally pin other critical workloads (for example CoreDNS and the metrics server) to the static
   node group.
5. Scale the Cluster Autoscaler Deployment to zero replicas.
6. Scale the old node groups down gradually, keeping a minimum for Karpenter and critical services
   (the guide suggests at least 2 instances for a single multi-AZ group, or 1 per group for
   single-AZ groups). Without PodDisruptionBudgets this step makes workloads unavailable, so set
   PDBs first and shrink a few instances at a time while watching the transition.
7. Confirm Karpenter creates nodes as the group nodes drain.
- Pick one owner per pool of capacity: do not point a NodePool and a Cluster Autoscaler node group at
  the same capacity.
- When several NodePools match a pod, Karpenter uses the highest `weight` first (default weight 0),
  so make overlapping NodePools mutually exclusive or weighted explicitly.

## 5. What does not change
HPA and VPA objects are untouched by swapping the node provisioner. Karpenter respects
PodDisruptionBudgets, and NodePools honour zonal topology spread constraints rather than balancing
zones themselves, so keep those constraints on workloads that need multi-zone durability.

## Gotchas
- Cost reporting keyed on ASG tags stops covering Karpenter nodes, which are not launched from an
  ASG; update tagging and cost-allocation pipelines before cutover.
- Karpenter's default `consolidateAfter` is `0s` and the default disruption budget is `nodes: 10%`.
  Teams coming from Cluster Autoscaler may see more node replacement than before; tune
  `consolidationPolicy`, `consolidateAfter` and `spec.disruption.budgets`.
- Cluster Autoscaler's `priority` expander ConfigMap has no one-to-one Karpenter equivalent;
  NodePool `weight` is the closest mechanism, so re-derive the policy.

## Verify
- [ ] Every node is traceable to exactly one owner (ASG tag or `karpenter.sh/nodepool` label).
- [ ] After cutover the Cluster Autoscaler Deployment is at zero replicas (or removed) and no old
      node group has a stray nonzero desired count.
- [ ] Workloads that matter have PDBs and survive draining a node group one step at a time.
- [ ] Cost-allocation tags or labels on Karpenter-launched nodes reach the same reporting pipeline
      the ASG nodes used.

## Checked

Checked 2026-10-27. Documentation checked: Karpenter docs v1.15 (latest release v1.15.1), Cluster Autoscaler FAQ on the autoscaler master branch, and the Kubernetes node autoscaling concept page (website main, v1.38 dev tree; v1.37 is the latest release). Confirmed: Cluster Autoscaler works on pre-configured node groups with per-cloud integrations; Karpenter provisions from NodePools without resource groups; capacity-type preference order reserved, spot, on-demand; NodePool `weight` selection; default `consolidationPolicy: WhenEmptyOrUnderutilized`, `consolidateAfter: 0s` and 10% default budget; the migration guide steps (Karpenter pinned to an existing node group, Cluster Autoscaler scaled to zero, node groups shrunk gradually with PDBs). Removed as unconfirmed: the claim that running both controllers causes a provisioning race, the taint-partition coexistence recipe, the 2017 history and release-cadence remarks, community GCP/Azure provider maturity, and relative latency claims.

Method: documentation only; no commands were run.
