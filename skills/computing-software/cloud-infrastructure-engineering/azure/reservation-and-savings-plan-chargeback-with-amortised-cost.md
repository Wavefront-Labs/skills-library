---
id: computing-software.cloud-infrastructure-engineering.azure.reservation-and-savings-plan-chargeback-with-amortised-cost
name: reservation-and-savings-plan-chargeback-with-amortised-cost
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, reservations, reservation-chargeback, amortised-reservations, savings-plans, unused-reservation, benefit-savings]
level: practitioner
status: docs-checked
description: "Charge reservation and savings plan costs back fairly: amortised cost, PricingModel/ChargeType fields, unused commitment, and calculating realised savings."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/reservations/charge-back-usage", "https://learn.microsoft.com/azure/cost-management-billing/savings-plan/charge-back-costs", "https://learn.microsoft.com/azure/cost-management-billing/reservations/calculate-ea-reservations-savings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reservation and savings plan chargeback

**Goal:** teams pay for the discounted usage they consumed, the central team owns unused commitment, and the savings are visible.

## Actual vs amortised
- **Actual cost** shows the purchase as its own charge; use it to see purchases and refunds.
- **Amortised cost** spreads the purchase over the term. For usage that gets a reservation (or savings plan) discount, `EffectivePrice` is the prorated hourly cost of the commitment rather than zero, so you can charge back the value consumed by a subscription, resource group, resource or tag. The dataset also includes the unused hours.
- EA and MCA billing readers can see amortised data. Individual subscriptions get it from the usage file, where `AdditionalInfo` carries the reservation or savings plan details.
- In Cost analysis pick the Amortized cost metric; in exports and Usage Details choose amortised data.

## Fields that matter
- `PricingModel` (for example `SavingsPlan`, `OnDemand`) and `ChargeType` (`Usage`, `Purchase`, `Refund`, `UnusedReservation`, `UnusedSavingsPlan`).
- `EffectivePrice`, `UnitPrice`, `Quantity`.

Savings plan report recipes from the docs:
- Savings plan usage: ActualCost with `ChargeType = 'Usage'` and `PricingModel = 'SavingsPlan'`.
- Unused: AmortizedCost with `ChargeType = 'UnusedSavingsPlan'` and `PricingModel = 'SavingsPlan'`.
- Purchases: `ChargeType = 'Purchase'`; refunds: `ChargeType = 'Refund'`.
- Reservation unused report (Cost Details API filter): `properties/ChargeType eq 'UnusedReservation'` with metric AmortizedCost.

## Chargeback model
1. Amortised cost grouped by subscription, resource group or tag gives each team its covered usage at the prorated rate.
2. Unused rows (`UnusedReservation`, `UnusedSavingsPlan`) are cost nobody consumed; allocate them to the commitment owner or a shared pool.
3. Publish monthly.

## Savings calculation (EA reservations, from the docs)
- Used savings per covered row: `(UnitPrice - EffectivePrice) * Quantity`; sum them.
- Unused cost: filter `ChargeType = UnusedReservation`; per row `EffectivePrice * Quantity`; sum.
- Reservation savings = total used savings minus total unused. A negative result means many unused reservations.
- MCA amortised files do not carry `UnitPrice` for reservations, so the calculation differs; the Cost Management Power BI app for EA also shows RI savings.

## Verify
- [ ] Amortised cost for the month reconciles with actual cost allowing for purchase timing.
- [ ] Unused commitment is reported separately and has an owner.

## Checked

Method: docs-checked 2026-11-09 against the reservation chargeback, savings plan chargeback and EA reservations savings pages (downloaded, converted to text and read). Dropped unconfirmed claims: the `PricingModel` Spot value, `BenefitId`/`BenefitName` and `PayGPrice` fields, the FOCUS/Kusto query, shared-scope hourly movement, savings plan versus reservation ordering, and the PAYG/CSP dataset remark.
