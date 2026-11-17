---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-exchange
name: commitment-exchange
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimisation, commitment-exchange, convertible-reserved-instances, ri-marketplace, reservation-exchange, reservation-refund]
level: practitioner
status: docs-checked
description: "Modify commitments after purchase: exchange convertible RIs, sell on the RI Marketplace, Azure reservation exchange and refund limits, GCP CUD constraints."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-convertible-exchange.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-general.html", "https://learn.microsoft.com/azure/cost-management-billing/reservations/exchange-and-refund-azure-reservations", "https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts", "https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-ris.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment exchange / resale / return

## AWS
- **Convertible RIs** can be exchanged for another Convertible RI (different instance family, OS or
  tenancy) of equal or higher value, any number of times. Exchanging is free, but you may pay a
  prorated upfront **true-up cost**. Requirements: the RI is active, has no pending exchange and has
  at least 24 hours left; the new RI must be currently offered, in the same Region, and a single
  exchange can swap several RIs for one new RI only. A single RI exchanged must keep the same term;
  merging RIs of different terms gives a 3-year term. The old end date carries over (furthest end
  date when merging). To exchange part of an RI, modify (split) it first. CLI flow:
  `describe-reserved-instances-offerings`, `get-reserved-instances-exchange-quote`, then
  `accept-reserved-instances-exchange-quote`.
- **Standard RIs** cannot be exchanged but can be modified. They can be **sold on the RI
  Marketplace**: register as a seller (bank with a US address; AWS India accounts cannot sell);
  Standard regional or zonal EC2 RIs only (not Convertible, RDS or ElastiCache); at least one month
  of term left; active for at least 30 days; not bought with a volume discount; AWS keeps a service
  fee of 12 percent of the upfront price. You cannot edit a listing; cancel and relist.
- **Savings Plans** suit variable usage without exchanges or modifications, but cannot be cancelled
  during the term. Choose term and type carefully.

## Azure
- **Reservations** can be exchanged for another reservation in the same product family (for example
  VM, Dedicated Host, VMware Solution), including to change region or term, and you may exchange a
  smaller quantity than you bought. Policy change: reservations bought on or after 1 February 2027
  are not exchangeable if the service is supported by savings plans; earlier ones keep one final
  exchange. Trade-in of reservations for a savings plan is unchanged.
- **Refunds**: total cancelled commitment is limited to USD 50,000 in a rolling 12-month window per
  billing scope (EA enrollment, MCA billing profile, or MPA customer). Microsoft was not charging
  early termination fees at the time of the page but reserves the right to.
- You need owner or Reservation administrator access to exchange or refund.

## Google Cloud
- Resource-based CUDs cannot be cancelled or deleted after purchase. They can be merged or split in
  some cases (merged commitments take a CANCELED status for the originals; discounted prices can
  change on the day the new commitment starts). Software license commitments cannot be merged.
  The purchasing project cannot be changed, but with CUD sharing enabled the benefit spreads across
  the billing account. Spend-based (flexible) CUDs reduce shape risk.

## Procedure
1. Monthly review of under-utilised commitments.
2. Exchange convertibles toward current usage before letting them waste.
3. Sell or refund only after confirming no future need (forecast).
4. Record the economic impact (savings retained vs loss).

## Verify
- [ ] Commitment utilisation above target after exchanges.

## Checked

Method: docs-checked 2026-11-09 against AWS ri-convertible-exchange, AWS ri-market-general (first sections), Azure exchange-and-refund page (searched), Compute Engine signing-up-committed-use-discounts (searched), Savings Plans vs RIs page. Removed unconfirmed: Savings Plans return window and "no resale" wording, Azure savings plan refund statement, "Linux only" standard RI modification detail.
