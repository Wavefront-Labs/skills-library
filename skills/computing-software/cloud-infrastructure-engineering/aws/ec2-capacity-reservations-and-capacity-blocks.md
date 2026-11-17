---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-capacity-reservations-and-capacity-blocks
name: ec2-capacity-reservations-and-capacity-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, capacity-reservation, capacity-reservations, capacity-blocks, odcr, gpu, disaster-recovery]
level: practitioner
status: docs-checked
description: "Guarantee EC2 capacity with On-Demand Capacity Reservations (open vs targeted, groups, end dates, sharing) and buy Capacity Blocks for ML GPUs; combine with Savings Plans."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-reservations.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cr-concepts.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/capacity-reservations-pricing-billing.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/capacity-blocks-how.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/capacity-blocks-purchase.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cr-groups-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity Reservations and Capacity Blocks

**Goal:** the instances you need exist when you need them — DR failover, big launch events,
scarce GPU types — without paying for idle hardware longer than necessary.

## 1. On-Demand Capacity Reservations (ODCR)
```bash
aws ec2 create-capacity-reservation --instance-type m7i.2xlarge --instance-platform Linux/UNIX \
  --availability-zone eu-west-1a --instance-count 20 \
  --instance-match-criteria open --end-date-type limited --end-date 2026-11-30T23:59:59Z
```
- Billed at the equivalent On-Demand rate whether used or not, from when the reservation becomes active (per second, 60-second minimum); an immediate reservation has **no term commitment** and can be cancelled at any time. With `--end-date-type limited` it ends within an hour after the end time; instances already running keep running.
- `open`: any matching instance (type, platform, AZ, tenancy) in the account uses it
  automatically. `targeted`: only launches that name the reservation (or its group).
- Savings Plans/Regional RIs discount the reservation charges — buy ODCR for *capacity*, SP for *price*.
- Share with other accounts through AWS RAM; CloudWatch metrics include `InstanceUtilization`, `UsedInstanceCount`, `AvailableInstanceCount` and `TotalInstanceCount`.

Targeted use via a resource group (lets ASGs/launch templates reference many reservations):
```bash
aws resource-groups create-group --name dr-capacity --configuration \
 '[{"Type":"AWS::EC2::CapacityReservationPool"},{"Type":"AWS::ResourceGroups::Generic","Parameters":[{"Name":"allowed-resource-types","Values":["AWS::EC2::CapacityReservation"]}]}]'
# launch template: CapacityReservationSpecification={CapacityReservationTarget={CapacityReservationResourceGroupArn=...}}
```
Future-dated ODCRs can be requested for planned events 5 to 120 days ahead (8 weeks or more recommended), targeted matching only, minimum 32 vCPUs and a commitment duration of at least 14 days (12 weeks for U and X instances). EC2 assesses the request (typically within 5 days) and may mark it `unsupported`.

## 2. DR pattern
Warm-standby/pilot-light region: ODCRs for the minimum fleet that must start during a
regional event (when everyone else is launching too); scale beyond it on demand.

## 3. Capacity Blocks for ML
Reserve GPU instances (for example P5, P4d, Trn) for 1 to 14 days in 1-day steps, or in 7-day steps up to 182 days, starting up to 8 weeks ahead, up to 64 instances per block and 256 across blocks:
```bash
aws ec2 describe-capacity-block-offerings --instance-type p5.48xlarge --instance-count 4 \
  --capacity-duration-hours 72 --start-date-range 2026-11-01T00:00:00Z --end-date-range 2026-11-08T00:00:00Z
aws ec2 purchase-capacity-block --capacity-block-offering-id cb-0abc --instance-platform Linux/UNIX
```
Paid upfront (the reservation is `payment-pending`, then `scheduled`) and cannot be cancelled. Launch
into the block with `--instance-market-options MarketType=capacity-block` plus the reservation as the capacity target.
Instances start terminating 30 minutes (60 for UltraServers) before the block ends, and an EventBridge event is emitted
10 minutes before that starts, so checkpoint training.

## Gotchas
- An open reservation silently absorbs unrelated launches of the same type; use targeted for DR pools.
- A reservation without an end date stays active until you cancel it; alarm on `AvailableInstanceCount` > 0 for long periods.
- ODCRs are AZ-specific: spread across AZs to match your ASG.

## Verify
- [ ] `describe-capacity-reservations` shows the reservation `active` with the expected count and end date.
- [ ] A launch with the targeted resource group succeeds during a capacity crunch test; `UsedInstanceCount` increments.
- [ ] Capacity Block start/end times are in the training schedule, with checkpointing before the end.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (Capacity Reservations concepts, pricing and billing, sharing, metrics, resource groups; Capacity Blocks overview, how it works, purchase and launch) and the botocore EC2 model.
- `create-capacity-reservation` options (`InstancePlatform`, `EndDateType`, `EndDate`, `InstanceMatchCriteria`), open versus targeted, Savings Plans and Regional RI discounts, RAM sharing, the four CloudWatch metrics and the resource group configuration confirmed.
- Future-dated reservation limits (5 to 120 days, 32 vCPUs, 14 days or 12 weeks commitment, targeted only) confirmed on the concepts page.
- Capacity Block durations, instance counts, 8-week lead time, payment states, no cancellation, termination 30 or 60 minutes before the end, the 10-minute EventBridge event and `MarketType=capacity-block` confirmed; the offering ID prefix is `cb-`, not `cbr-`.
- The warning that an `open` reservation absorbs any matching launch follows the documented `open` definition; no prices are stated.

Method: documentation only; no commands were run.
