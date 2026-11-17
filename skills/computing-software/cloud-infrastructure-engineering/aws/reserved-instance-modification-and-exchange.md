---
id: computing-software.cloud-infrastructure-engineering.aws.reserved-instance-modification-and-exchange
name: reserved-instance-modification-and-exchange
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, reserved-instances, ri-exchange, modify-reserved-instances, convertible-ri, normalization-factor, instance-size-flexibility]
level: advanced
status: docs-checked
description: "Re-fit EC2 Reserved Instances: modify AZ, scope and size within a family by size footprint, and exchange Convertible RIs with quote, true-up cost and payment option rules."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-modifying.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-convertible-exchange.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modifying and exchanging Reserved Instances

## 1. Instance size footprint
Footprint = number of instances x normalization factor of the size. A modification to different sizes must keep the same
total footprint or it is not processed. Factors: nano 0.25, micro 0.5, small 1, medium 2, large 4, xlarge 8, 2xlarge 16,
3xlarge 24, 4xlarge 32, 6xlarge 48, 8xlarge 64, 9xlarge 72, 10xlarge 80, 12xlarge 96, 16xlarge 128, 18xlarge 144,
24xlarge 192 (larger sizes and per-family bare metal factors are on the page). Example: one `t2.large` (4) can become four
`t2.small`; two `t2.small` (2) cannot become one `t2.large` (4).

## 2. Modifying Reserved Instances (Standard or Convertible)
- Changeable: Availability Zone within the Region (Linux and Windows); scope zonal or regional (Linux and Windows; going
  regional loses the capacity reservation, going zonal loses AZ and size flexibility); instance size within the same family
  and generation (Linux/UNIX only, default tenancy, and the RI must support size flexibility). `t1.micro` has one size.
- You can split one RI into several (10 in us-east-1a to 5 in 1a and 5 in 1b) or merge several into one.
- Requirements: RI is active, not modified at purchase time, no pending modification, not listed on the RI Marketplace, all
  originals the same type (all Standard or all Convertible), and Standard originals must expire within the same hour.
  EC2 also needs capacity for the new configuration where applicable.
```bash
aws ec2 modify-reserved-instances --reserved-instances-ids <RI_ID> --target-configurations file://configuration.json
aws ec2 describe-reserved-instances-modifications --reserved-instances-modification-ids <MODIFICATION_ID> \
  --query ReservedInstancesModifications[].Status
```
- Status is `processing`, `fulfilled` or `failed`. A request accepted as valid can still fail on unavailable capacity.
- Effect: effective immediately, with the benefit applied from the hour of the request. The original is retired and the new
  RI keeps the original end date. Modified RIs show a $0 fixed price. No fee. A pending modification cannot be changed or
  cancelled, but a completed one can be rolled back by another modification.
- Instances that no longer match the new parameters are charged at the On-Demand rate unless other reservations apply.

## 3. Exchanging Convertible RIs
- Exchange for other Convertible RIs currently offered by AWS, with a different family, operating system or tenancy, as long
  as the new one is of equal or higher value; the number of exchanges is unlimited. Standard RIs cannot be exchanged (modify them).
- The RIs must be active, not pending another exchange, and have at least 24 hours left. Same Region only. You can exchange
  one or more at a time for one Convertible RI only. A zonal exchange needs capacity in the Region.
- Payment: All Upfront and Partial Upfront can be swapped with each other; No Upfront can go to All or Partial Upfront;
  All or Partial Upfront cannot go to No Upfront; No Upfront to No Upfront needs an equal or higher hourly price.
- Cost: the exchange is free, but you may pay a true-up (prorated upfront difference). If value would fall short, AWS
  gives you enough instances to make it equal or higher (and the true-up at least $0.00). List-value ratios round up, with the
  extra reservation sharing the same end date.
- The end date carries over to the new reservation. Page merge examples: two 1-year RIs can only become a 1-year RI; a
  1-year plus a 3-year, or two 3-year, can only become a 3-year RI; the new end date is the later of the two in each example.
- To exchange part of an RI, modify it into two or more RIs first, then exchange some.
```bash
aws ec2 describe-reserved-instances-offerings --offering-class convertible ...
aws ec2 get-reserved-instances-exchange-quote --reserved-instance-ids <RI_ID> ... \
  --target-configurations OfferingId=<OFFERING_ID>,InstanceCount=<N>
aws ec2 accept-reserved-instances-exchange-quote --reserved-instance-ids <RI_ID> ... \
  --target-configurations OfferingId=<OFFERING_ID>,InstanceCount=<N>
```
The quote includes the number of RIs received and the true-up cost.

## Gotchas
- A modification retires the original, so anything keyed on the old RI ID needs updating.
- Reserved Instance Marketplace listings block modification.

## Verify
- [ ] `describe-reserved-instances-modifications` reports `fulfilled`.
- [ ] The exchange quote was reviewed for the true-up cost before accepting.

## Checked
Date: 2026-11-07. Read in full: "Modify Reserved Instances" (requirements, size footprint and the first half of the
bare-metal factors, console and CLI submission, troubleshooting) and "Exchange Convertible Reserved Instances"
(requirements, true-up calculation, merge and partial exchange examples, submit). Botocore `GetReservedInstancesExchangeQuote`
checked for flags (the CLI listing uses `...` where the page gives no full command). The third source, "apply_ri", was
dropped because it was not read.
Removed because no page read states them: "modification takes minutes to an hour", the Compute Savings Plans advice, RDS,
ElastiCache and OpenSearch RI notes, Marketplace seller requirements (US bank account), "no refunds", the platform-string
warning, the Cost Explorer utilisation check, the "merge small convertibles to minimise rounding" tip, and the claim that
modification can change network platform. I also corrected the earlier claim that regional Linux RIs get size flexibility
"automatically": the page says size modification needs Linux/UNIX with default tenancy and a size-flexible RI.
Method: documentation only; no commands were run.
