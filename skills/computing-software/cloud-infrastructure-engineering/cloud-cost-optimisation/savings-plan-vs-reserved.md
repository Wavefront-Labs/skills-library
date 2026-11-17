---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.savings-plan-vs-reserved
name: savings-plan-vs-reserved
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, savings-plan-vs-reserved, savings-plans, reserved-instances, compute-savings-plan, commitment-discounts, aws]
level: practitioner
status: docs-checked
description: "Choose between AWS Savings Plans and Reserved Instances: Compute vs EC2 Instance SPs, standard vs convertible RIs, capacity reservations, and a layered mix."
sources:
  - https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html
  - https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-ris.html
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Savings plans vs reserved instances

Both trade a 1- or 3-year commitment for a discount. Savings plans commit **dollars per hour**;
RIs commit to **specific instance attributes** (type, Region, tenancy, platform). AWS itself
recommends Savings Plans over Reserved Instances for EC2.

## AWS options
| Option | Applies to | Flexibility | Max discount vs On-Demand |
|---|---|---|---|
| Compute Savings Plan | EC2 any family/size/OS/tenancy/Region, Fargate, Lambda | highest | up to 66% |
| EC2 Instance Savings Plan | one EC2 instance family in one Region; any size, OS, tenancy | medium | up to 72% |
| Standard RI (EC2) | instance type, Region, tenancy, platform; modifiable, not exchangeable | low; regional RIs are size-flexible | up to 72% |
| Convertible RI (EC2) | as above, but exchangeable manually for other Convertible RIs | medium | up to 66% |

SageMaker AI Savings Plans exist for SageMaker instances. RIs for other services (RDS,
ElastiCache and so on) are covered in `database-reservations`. Offerings change, so check
the current AWS docs for newer plan types before choosing.

## Decision
1. **EC2 + Fargate + Lambda baseline**: Compute SP sized to the always-on floor of compute
   spend; it follows family changes and Region moves.
2. **Stable, family-locked fleets**: EC2 Instance SP trades flexibility for the higher
   discount tier (72% vs 66% maximum).
3. **Capacity guarantee needed**: Savings Plans give no capacity reservation; allocate an
   On-Demand Capacity Reservation and the Savings Plan will apply to it.
4. **Payment**: All, Partial and No Upfront options exist for both; a higher upfront payment
   generally saves more. Choose by cost of capital (finance decides), not habit.

## Mechanics to remember
- A Savings Plan does not apply to Spot usage or to usage already covered by RIs.
- Savings Plans cannot be cancelled during the term. An RI purchase also cannot be
  cancelled, but RIs may be modified, sold on the Reserved Instance Marketplace, or
  (Convertible only) exchanged.
- RIs do not renew automatically; at expiry you pay On-Demand rates unless you buy again.
- No Upfront RIs require a successful billing history.
- Savings Plans prices for SUSE Linux Enterprise Server differ from the corresponding RI price.

## Gotchas
- Buying EC2 Instance SPs before a planned family migration strands the commitment, since
  the plan is tied to one family in one Region.

## Verify
- [ ] Commitment mix documented by layer (Compute SP, EC2 SP, RIs) with rationale.
- [ ] Utilisation and coverage tracked after purchase (Cost Explorer reports).

## Checked
Method: docs-checked 2026-11-09 against the three cited AWS pages (what-is-savings-plans, sp-ris, ec2-reserved-instances); read via summarising fetch, not raw HTML. Dropped unconfirmed: SageMaker discount figure, "highest discount first" application order, ~95% utilisation target, lowest-hourly-spend coverage rule, zonal RI claim.
