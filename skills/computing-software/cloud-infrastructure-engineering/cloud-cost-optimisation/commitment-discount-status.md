---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-discount-status
name: commitment-discount-status
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, billing-concepts, commitment-discount-status, commitment-discount-columns, amortisation, unused-commitment, focus-specification, cur-2]
level: practitioner
status: draft
description: "Read commitment discount columns in billing data: FOCUS CommitmentDiscount fields, used vs unused status, amortised effective cost, and the AWS, Azure and GCP equivalents."
sources: ["https://focus.finops.org/", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2-savings-plan.html", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2-reservation.html", "https://learn.microsoft.com/azure/cost-management-billing/reservations/understand-reserved-instance-usage-ea"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Commitment discount columns in billing data

Commitments (RIs, savings plans, CUDs) change cost data in three ways: a purchase charge, discounted
usage rows, and unused capacity. Reading the right columns gives coverage, utilisation and fair
allocation straight from the export.

## FOCUS columns
- `CommitmentDiscountId`, `CommitmentDiscountName`, `CommitmentDiscountType` (provider label, e.g.
  Savings Plan, Reservation, Committed Use Discount).
- `CommitmentDiscountCategory`: **Spend** (money-per-hour commitment) or **Usage** (units such as
  instance hours).
- `CommitmentDiscountStatus`: **Used** or **Unused**; unused rows carry the cost of idle commitment.
- `CommitmentDiscountQuantity` / `CommitmentDiscountUnit` (newer versions).
- Costs: `ListCost` (on-demand), `ContractedCost`, `EffectiveCost` (amortised: includes the
  upfront share), `BilledCost` (cash in this period).

## Calculations
```sql
-- utilisation per commitment for a month
SELECT CommitmentDiscountId,
  SUM(CASE WHEN CommitmentDiscountStatus='Used' THEN EffectiveCost END) /
  NULLIF(SUM(EffectiveCost),0) AS utilisation
FROM focus_costs
WHERE CommitmentDiscountId IS NOT NULL AND ChargeCategory='Usage'
GROUP BY 1;

-- savings vs on-demand for covered usage
SELECT SUM(ListCost - EffectiveCost) FROM focus_costs
WHERE CommitmentDiscountStatus='Used';
```

## Provider equivalents
- **AWS CUR 2.0**: `savings_plan_savings_plan_a_r_n`, `savings_plan_savings_plan_effective_cost`,
  `savings_plan_used_commitment`, `savings_plan_total_commitment_to_date`;
  `reservation_reservation_a_r_n`, `reservation_effective_cost`,
  `reservation_unused_amortized_upfront_fee_for_billing_period`, `reservation_unused_recurring_fee`.
  Line types DiscountedUsage, SavingsPlanCoveredUsage, SavingsPlanNegation, RIFee.
- **Azure**: the amortised cost dataset spreads purchases onto usage via `BenefitId`/`BenefitName`
  (older: `ReservationId`), plus `ChargeType = UnusedReservation` / `UnusedSavingsPlan`.
- **Google Cloud**: CUD fees and credits (`credits.type` COMMITTED_USAGE_DISCOUNT and
  COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE) in the standard export; Google is moving spend-based CUDs to
  a model where discounted prices appear directly; check which model your billing account uses.

## Gotchas
- Using BilledCost for team reports puts the whole upfront fee on the purchasing account's month.
- Unused commitment has no resource; decide who carries it (central vs pro rata to purchasers).
- Size-flexible RIs apply normalised units; per-instance coverage maths must use normalised units.

## Verify
- [ ] Utilisation computed from billing data matches the provider's utilisation report within 1%.
- [ ] Unused commitment cost is visible as its own line.
