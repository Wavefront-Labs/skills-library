---
id: computing-software.cloud-infrastructure-engineering.aws.asg-az-distribution-and-capacity-distribution-strategy
name: asg-az-distribution-and-capacity-distribution-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, az-distribution, capacity-distribution-strategy, zonal-shift, azrebalance]
level: advanced
status: docs-checked
description: "Control how Auto Scaling spreads instances across AZs: AZRebalance, balanced-best-effort vs balanced-only capacity distribution, and AZ impairment with zonal shift."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-availability-zone-balanced.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-zonal-shift.html", "https://docs.aws.amazon.com/cli/latest/reference/autoscaling/update-auto-scaling-group.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AZ distribution and capacity distribution strategy

## 1. Default behaviour
Auto Scaling keeps an equal number of instances across the enabled AZs and automatically tries to fix an
imbalance between AZs (the `AZRebalance` process).

## 2. Capacity distribution strategy
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web \
  --availability-zone-distribution CapacityDistributionStrategy=balanced-only
```
| Strategy | If an AZ cannot launch |
|---|---|
| `balanced-best-effort` (default) | tries another healthy AZ for the launch |
| `balanced-only` | keeps trying to launch in the failing AZ to preserve balance |
| `reservations-then-balanced` | fills the group's Capacity Reservations first, then balances the rest; you must name the reservations or a reservation resource group |
`balanced-only` suits quorum-based workloads, or groups with enough spare capacity in the remaining AZs to tolerate losing one AZ.
With `reservations-then-balanced`, scale-in removes instances outside reservations first.

## 3. AZ impairment and zonal shift
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web \
  --availability-zone-impairment-policy ZonalShiftEnabled=true,ImpairedZoneHealthCheckBehavior=IgnoreUnhealthy
```
With zonal shift (ARC) active on the group, the AZ is treated as impaired: new capacity launches in the
healthy AZs, scaling policies cannot decrease desired capacity (increases are still allowed), and instance
refresh timeouts are extended. `IgnoreUnhealthy` stops replacing unhealthy instances in the shifted AZ;
`ReplaceUnhealthy` replaces them in all AZs. AWS recommends an instance maintenance policy with minimum healthy
percentage 100, and, for groups behind cross-zone-disabled load balancers, `balanced-only`; if both the ASG
and the load balancer are shifted, cancel the ASG shift first and let capacity rebalance before cancelling
the load balancer shift.

## Verify
- [ ] Instance counts per AZ differ by at most one in steady state.
- [ ] A practice zonal shift moves capacity out of the AZ without health-replacement storms.

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (Availability Zone distribution, zonal shift), the aws-cli update-auto-scaling-group reference and the botocore autoscaling 2011-01-01 model.
- Corrected: a third strategy `reservations-then-balanced` exists; `balanced-only` keeps retrying the failing AZ to preserve balance; zonal shift blocks scale-in (not scale-out), extends instance refresh timeouts and offers `ReplaceUnhealthy`/`IgnoreUnhealthy` behaviours; recommended minimum-healthy-percentage 100.
- Confirmed: `balanced-best-effort` is the default (model documentation), `AvailabilityZoneImpairmentPolicy` members and enum values.
- Removed: unsupported advice about three AZs and subnet-removal terminations.

Method: documentation only; no commands were run.
