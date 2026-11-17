---
id: computing-software.cloud-infrastructure-engineering.kubernetes.commitment-discounts-for-baseline-node-capacity
name: commitment-discounts-for-baseline-node-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, savings-plans, reserved-capacity, committed-use-discounts, cost-optimisation, finops, karpenter]
level: advanced
status: docs-checked
description: "Cover the steady baseline of Kubernetes node spend with Savings Plans, RIs, CUDs or Azure reservations: measure the floor, size the commitment, and keep autoscalers aligned."
sources: ["https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/plan-types.html", "https://cloud.google.com/docs/cuds", "https://learn.microsoft.com/en-us/azure/cost-management-billing/savings-plan/savings-plan-overview", "https://karpenter.sh/docs/concepts/scheduling/", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/cluster/node-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment discounts for baseline node capacity

## Layering
- **Baseline** (always-on floor): commitments. AWS quotes up to 66% off On-Demand for Compute
  Savings Plans and up to 72% for EC2 Instance Savings Plans.
- **Variable daytime/peak**: on-demand.
- **Interruptible-tolerant**: spot/preemptible.
Commit only to the floor; over-commitment is waste because you pay for the commitment whether
or not you use it (Azure, for example, says unused hourly commitment expires and does not roll
over).

## Measure the floor
Use 60-90 days of node data, not pod requests:
```promql
# vCPUs of on-demand nodes over time (kube-state-metrics + node labels)
sum(kube_node_status_capacity{resource="cpu"} * on(node) group_left(label_karpenter_sh_capacity_type)
    kube_node_labels{label_karpenter_sh_capacity_type="on-demand"})
```
`kube_node_labels` only carries node labels allowed by kube-state-metrics'
`--metric-labels-allowlist`. Take a low percentile of hourly totals as the safe commitment, then
compare with the cloud's own recommendations (AWS Cost Explorer shows recommended Savings Plans
commitments).

## Pick the instrument
| Cloud | Flexible | Rigid (deeper discount) |
|---|---|---|
| AWS | Compute Savings Plan (any family, size, OS, tenancy or Region; also Fargate and Lambda) | EC2 Instance Savings Plan (one family in one Region), Reserved Instances |
| GCP | Spend-based CUDs (Compute Flexible CUDs, Flexible Savings Plans) | Resource-based CUDs (Compute Engine vCPUs, memory and more in one region) |
| Azure | Savings plan for compute (hourly spend commitment) | Reservations (specific resource, size and region; deeper discount) |
Kubernetes node fleets change instance types often (Karpenter, upgrades to new
generations), so prefer the flexible instrument for most of the commitment.

## Keep autoscalers aligned
- Commitments do not steer schedulers. With rigid commitments, make the matching
  instances preferred: a Karpenter NodePool restricted to the committed family with a higher
  `.spec.weight` and `.spec.limits` capped at the committed capacity (the pattern Karpenter's
  scheduling docs give for Savings Plans and RIs); the Cluster Autoscaler `priority` expander
  for node groups.
- Karpenter on AWS can target capacity reservations through EC2NodeClass
  `capacityReservationSelectorTerms`; such nodes get `karpenter.sh/capacity-type: reserved`, and
  a NodePool allowing several capacity types prefers `reserved`, then `spot`, then `on-demand`.
- Consolidation and rightsizing lower the floor over time: commit in tranches (e.g.
  quarterly) instead of one large 3-year purchase.

## Track
- **Coverage** (% of eligible spend under commitment) and **utilisation** (% of commitment
  used). Aim for utilisation near 100%; set the coverage target from your measured floor.
- Allocate commitment savings to teams in showback (OpenCost/Kubecost amortised costs),
  or teams see no benefit from efficiency.

## Verify
- [ ] Commitment utilisation stays near 100% for a month after purchase; on-demand spend
  falls by the expected amount.

## Checked
2026-10-27 against AWS Savings Plans docs (what-is and plan types pages), Google Cloud CUD
overview, Azure savings plan overview, Karpenter AWS provider docs (aws/karpenter-provider-aws
main: NodePools, scheduling, EC2NodeClass), the cluster-autoscaler FAQ and kube-state-metrics node
metrics docs. Confirmed: AWS plan scopes and the 66%/72% maximums, GCP spend-based vs
resource-based CUDs, Azure savings plan vs reservations and hourly expiry, NodePool `weight`,
`limits` and the Savings Plans pattern, `capacityReservationSelectorTerms`, the `reserved`
capacity type and its priority, the priority expander, and the KSM label allowlist. Replaced a
generic "30-70% off" figure and coverage targets no doc gives.
Method: documentation only; no commands were run.
