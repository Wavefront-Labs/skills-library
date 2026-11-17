---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.azure-reservation-management
name: azure-reservation-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, azure-reservation-management, azure-reservations, azure-savings-plan, instance-size-flexibility, commitment-discounts, azure]
level: practitioner
status: docs-checked
description: "Manage Azure reservations and savings plans: scope, instance size flexibility, exchange and refund limits, the 2027 exchange change and savings plan trade-in."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/reservations/save-compute-costs-reservations", "https://learn.microsoft.com/azure/cost-management-billing/savings-plan/savings-plan-compute-overview", "https://learn.microsoft.com/azure/cost-management-billing/reservations/exchange-and-refund-azure-reservations", "https://learn.microsoft.com/azure/virtual-machines/reserved-vm-instance-size-flexibility"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure reservations and savings plan

## Options
- **Reservations** (1 or 3 years): VMs, SQL Database and Managed Instance, Cosmos DB, storage
  capacity, Databricks and more; each covers only the charges Microsoft lists (for example VM and cloud
  services compute, not software, networking or storage). Applied hourly (except Databricks); a billing
  discount that does not affect runtime. Matched by SKU, region where applicable, and scope.
- **Savings plan for compute** (1 or 3 years): a fixed dollars-per-hour commitment that applies
  automatically across eligible services and regions: Virtual Machines, App Service, Functions Premium
  plan, Container Instances, Dedicated Host, Container Apps and Spring Apps for Enterprise. There is
  also a savings plan for databases. Benefits go first to usage that earns the highest discount; unused
  hourly commitment expires and does not roll over; usage above the commitment is pay-as-you-go.
- Reservations suit stable, predictable workloads with deeper discounts; savings plans suit dynamic ones.
- The pages read do not state the order in which reservations and savings plans apply to the same usage;
  check "How a savings plan discount is applied" before modelling overlap.

## Scope
A reservation's scope selects where its savings apply, and after purchase you can update the scope to a
different subscription, change who manages it, split it, or change instance size flexibility. Wider scopes
raise utilisation; narrower scopes help chargeback but can strand benefit. See "Scope reservations" for the list of scopes.

## Instance size flexibility
When buying a Reserved VM Instance you choose to optimise for instance size flexibility or capacity priority.
With flexibility, the reservation applies to sizes in the same flexibility group using ratios (example in the
docs: a Standard_DS4_v2 reservation, ratio 8, covers eight DS1_v2 VMs of ratio 1, or covers half a DS5_v2 of ratio 16).
Sizes in a different group (for example DSv2 High Memory) are not covered. Ratios are fetched through the API or
PowerShell; the published CSV stops receiving updates from May 9, 2026.

## Exchanges, refunds and savings plan trade-in
- Exchange a reservation for another of the same type; new reservation total must be equal to or greater than
  the remaining commitment of the original, and the new term starts at exchange. Different product
  families cannot be exchanged (Cosmos DB for SQL Database), and Red Hat, SUSE and pre-purchase plans are excluded.
- Refunds (cancellations) are limited to USD 50,000 of cancelled commitment in a rolling 12-month window per
  billing scope; refunds from exchanges do not count. Microsoft is not currently charging an early termination fee but may.
- Policy change: reservations purchased on or after February 1, 2027 for services supported by savings plans
  (VMs, App Service, SQL Database and similar) will not be exchangeable; older ones keep one final exchange.
  Reservations can be traded in for a savings plan.
- Savings plan purchases cannot be cancelled or refunded.

## Operating
1. Recommendations: Azure Advisor (VMs only), the portal purchase experience, the Cost Management Power BI
   app and APIs for reservations; Advisor, the portal and Benefit Recommendation APIs for savings plans.
2. Review utilisation and unused cost in the portal or via APIs, and set owners with permission to exchange or refund.
3. Pay up front or monthly; the total cost is the same.
4. `az reservations reservation-order list` and `az costmanagement` for automation.

## Gotchas
- Resizing VMs into a different flexibility group breaks coverage; coordinate rightsizing with reservations.
- Reservations do not cover Windows or SQL licence costs; Azure Hybrid Benefit can cover licensing, so
  price comparisons must include both.
- Wider scopes mean subscription owners see benefits they did not buy; allocate via amortised data.

## Verify
- [ ] Utilisation of every reservation order is reviewed on a schedule.
- [ ] Scope choice documented; unused reservation cost reported monthly.

## Checked
Date: 2026-11-08. Confirmed against the four cited Microsoft Learn pages (What are Azure Reservations, savings plan
overview, exchanges and refunds, VM size flexibility). Removed claims the pages do not make: reservation-first benefit
order, the shared-scope definition, the 7/30/60-day lookback, the 95 percent utilisation alert, auto-renew timing, the
BenefitName and UnusedReservation fields, and the AKS node claim. Added the February 1, 2027 exchange policy change.
Method: documentation only; no commands were run.
