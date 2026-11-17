---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-fleet-and-spot-allocation-strategies
name: ec2-fleet-and-spot-allocation-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, spot-instances, spot-fleet, ec2-fleet, allocation-strategy, price-capacity-optimized, diversification]
level: practitioner
status: docs-checked
description: "Launch Spot capacity with EC2 Fleet or ASG mixed instances: price-capacity-optimized allocation, instance diversification, On-Demand base, and why Spot Fleet is legacy."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-request-type.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-attribute-based-instance-type-selection.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 Fleet and Spot allocation strategies

## 1. Which API
- **Auto Scaling group with mixed instances policy** — default for long-running services
  (health checks, scaling policies, instance refresh).
- **EC2 Fleet** (`create-fleet`, type `instant`) — one-shot launch of a diversified set
  (batch, CI, HPC) returning instance IDs synchronously; `maintain` type keeps capacity.
- **Spot Fleet** (`request-spot-fleet`) — a legacy API with no planned investment; AWS recommends EC2 Fleet (`CreateFleet`) or an Auto Scaling group instead. The same applies to `request-spot-instances`.

## 2. Allocation strategies (Spot)
| Strategy | Picks | Use |
|---|---|---|
| `price-capacity-optimized` | pools with the most available capacity, then the lowest price among them | **recommended** for most workloads |
| `capacity-optimized` | pools with the most available capacity (`capacity-optimized-prioritized` honours instance type priorities best-effort) | workloads where an interruption is costly |
| `lowest-price` | cheapest pool with capacity | not recommended: highest interruption risk |
| `diversified` | spread across all Spot pools | spreading risk |
`lowest-price` is the default Spot strategy when you use the AWS CLI, so set the strategy explicitly. For Spot Fleet the CLI names are camelCase (`priceCapacityOptimized`). On-Demand portion: `lowest-price` (default) or `prioritized`.

## 3. EC2 Fleet example
```bash
aws ec2 create-fleet --type instant --cli-input-json '{
 "LaunchTemplateConfigs": [{"LaunchTemplateSpecification": {"LaunchTemplateName": "batch-worker", "Version": "$Latest"},
   "Overrides": [{"InstanceRequirements": {"VCpuCount": {"Min": 8, "Max": 16}, "MemoryMiB": {"Min": 32768},
      "BurstablePerformance": "excluded"}}]}],
 "TargetCapacitySpecification": {"TotalTargetCapacity": 64, "DefaultTargetCapacityType": "spot", "TargetCapacityUnitType": "vcpu"},
 "SpotOptions": {"AllocationStrategy": "price-capacity-optimized"},
 "OnDemandOptions": {"AllocationStrategy": "lowest-price"}}'
```
Attribute-based selection (`InstanceRequirements`) automatically uses new instance types as they are
released, which gives the fleet more pools to draw from. `TargetCapacityUnitType` can be `vcpu`, `memory-mib` or `units`, so target capacity need not be an instance count.

## 4. Diversification rules of thumb
- AWS's rule of thumb is to be flexible across at least 10 instance types per workload, and to use every Availability Zone.
- Don't pin to one size; let weights or vCPU units normalise.
- Keep an On-Demand base (ASG `OnDemandBaseCapacity`) for the minimum the service needs.

## Gotchas
- `instant` fleets return the instances that launched plus errors for those that could not — always check the errors array.
- Max price: leave it unset (you pay the current Spot price, never above On-Demand); a max price only makes interruptions more frequent.
- Spot quotas are in vCPUs per instance family group, for example "All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests".

## Verify
- [ ] Fleet/ASG launches across ≥ 3 instance types and all intended AZs (`describe-instances` by tag).
- [ ] Spot interruption rate over 30 days acceptable (EventBridge interruption events count).
- [ ] Cost per vCPU-hour tracked vs On-Demand baseline.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (allocation strategies, Spot best practices, fleet request types, attribute-based instance type selection, Spot requests and quotas) and the botocore EC2 model.
- Spot strategies (`price-capacity-optimized` recommended, `capacity-optimized`, `capacity-optimized-prioritized`, `lowest-price` default in the CLI, `diversified`) and the On-Demand strategies (`lowest-price` default, `prioritized`) confirmed on the allocation strategy page and in the `CreateFleet` model.
- Spot Fleet and `RequestSpotInstances` as legacy APIs with no planned investment, `instant` fleet behaviour, the 10-instance-type rule of thumb, the no-maximum-price recommendation and the vCPU-based Spot quota names confirmed.
- `TargetCapacityUnitType` values (`vcpu`, `memory-mib`, `units`) and `InstanceRequirements` fields (`VCpuCount`, `MemoryMiB`, `BurstablePerformance`) confirmed in the service model; automatic use of new instance types confirmed on the attribute-based selection page.
- Removed the `InsufficientInstanceCapacity` example error code, which was not on the pages read.

Method: documentation only; no commands were run.
