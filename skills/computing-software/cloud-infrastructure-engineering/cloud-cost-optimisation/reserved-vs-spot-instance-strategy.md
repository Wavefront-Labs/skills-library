---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.reserved-vs-spot-instance-strategy
name: reserved-vs-spot-instance-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, purchasing-strategy, reserved-instances, savings-plans, committed-use-discounts, cud, azure-reservations, azure-savings-plan, spot-instances, spot-vms, preemptible, on-demand, break-even, coverage, utilisation, commitment-laddering, workload-classification, interruption-handling, spot-interruption-notice, capacity-rebalancing, mixed-instances-policy, price-capacity-optimized, karpenter, ec2-fleet, spot-placement-score, checkpointing]
level: advanced
status: draft
description: "Build a layered purchasing mix: classify workloads, compute commitment break-even, size commitments to the floor, and engineer spot use with diversification and interruption handling."
sources: ["AWS documentation - Savings Plans, Reserved Instances and EC2 Spot best practices", "Azure documentation - Reservations, savings plan for compute and Spot VMs", "Google Cloud documentation - Committed use discounts and Spot VMs", "FinOps Foundation - Rate optimization capability"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reserved vs spot instance strategy — layer the rates to the workload shape

**Goal:** each unit of compute is bought at the cheapest rate that its interruption tolerance
and stability allow: committed for the steady floor, spot for interruptible work, on-demand
only for what's left.

Commitment product options and discount ranges are summarised in
`computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments`;
this skill is the decision method and the spot engineering.

## 1. Classify workloads
| Class | Example | Rate |
|---|---|---|
| Steady, 24/7, interruption-intolerant | prod databases, core APIs at base load | commitment |
| Variable but intolerant | daytime API peaks | on-demand (+ autoscaling) |
| Interruptible, stateless or checkpointable | CI runners, batch, rendering, ML training with checkpoints, queue workers | **spot** |
| Interruptible but needs some floor | K8s worker pools | on-demand/committed base + spot burst |
| Short-lived or uncertain | new product, pre-migration | on-demand until 2-3 months of data |

## 2. Commitment break-even
A commitment is billed whether used or not. Break-even utilisation = 1 − discount.
At 40% discount you must use the commitment > 60% of the term to beat on-demand; at 25%, > 75%.
Method:
1. Take hourly usage (normalised to commitment units, e.g. $/h for Savings Plans) for 30-90 days **after rightsizing**.
2. Commit to roughly the **minimum or p10 hour**, not the average — that portion is used 100% of the time.
3. Re-run monthly; buy additional tranches as the floor rises (laddering), so expiries are staggered and you can step down if usage drops.
4. Prefer flexible instruments (Compute Savings Plans, Azure savings plan, GCP spend-based/flexible CUDs) when roadmaps include family changes (e.g. ARM migration) — the extra discount of rigid RIs is lost if the family changes.
Track **coverage** (share of eligible spend on commitments) and **utilisation** (share of commitment used; aim ~95-100%).

## 3. Spot engineering
Discount is high (often 60-90%) because capacity can be reclaimed. Make that cheap:
- **Diversify:** many instance types and sizes across all AZs; use `price-capacity-optimized` allocation (AWS) or equivalent. A pool of one type in one AZ will be reclaimed together.
- **Handle notice:** AWS gives a 2-minute interruption notice (plus earlier rebalance recommendations); Azure and GCP give about 30 seconds. Drain on notice: stop taking work, checkpoint, deregister from the LB. On K8s, use the node termination handler or Karpenter's interruption handling with an SQS queue.
- **Stateless or checkpointed** work only; jobs > ~1 hour must checkpoint.
- **Fallback:** ASG mixed-instances policy with an on-demand base (`OnDemandBaseCapacity`) and percentage above base; or Karpenter NodePools with `capacity-type: [spot, on-demand]` (it falls back to on-demand when spot is unavailable).
- Check AWS Spot placement score before choosing regions for large spot fleets.
- Spot cannot be covered by commitments, and there is no bidding strategy needed any more on AWS — you pay the current spot price, capped at on-demand.

## 4. Example layering
A K8s platform averaging 400 vCPU, floor 250, peak 600:
- 250 vCPU covered by a Compute Savings Plan (used ~100%).
- Interruptible workers (≈150 vCPU at peak) on spot, diversified across 10+ instance types.
- Remaining peak on on-demand via autoscaling.

## Gotchas
- Buying 3-year all-upfront before a migration or rearchitecture locks in obsolete capacity; 1-year no-upfront is the safest first purchase.
- Commitments bought in one account but not shared (sharing disabled) go unused.
- Spot savings evaporate if interruption retries re-run long jobs from scratch.
- Stateful sets, single-replica services and databases on spot cause outages, not savings.
- Commitment-management vendors that buy and resell RIs take a share of savings — compare against doing it in-house.

## Verify
- [ ] Each workload class has a rate decision recorded.
- [ ] Commitment utilisation ≥ ~95% and coverage reported monthly.
- [ ] Commitment expiries are staggered across months/quarters.
- [ ] Spot pools use ≥ several instance types across all AZs, with tested interruption drain.
- [ ] Spot jobs checkpoint or are short enough to retry cheaply.

Uncertain: discount and notice figures change; confirm current provider documentation and pricing before purchasing.
