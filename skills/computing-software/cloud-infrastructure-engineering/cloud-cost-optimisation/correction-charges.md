---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.correction-charges
name: correction-charges
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, billing-concepts, correction-charges, charge-category, chargeclass, refunds, credits, adjustments, focus-specification]
level: practitioner
status: draft
description: "Handle charge categories and corrections in billing data: usage, purchase, tax, credit and adjustment rows, FOCUS ChargeClass correction, refunds and how to report them."
sources: ["https://focus.finops.org/", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2-line-item.html", "https://learn.microsoft.com/azure/cost-management-billing/automate/understand-usage-details-fields"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Charge categories and correction charges

Not every billing row is usage. Summing everything without looking at the category produces
negative days, double counted purchases and phantom savings.

## FOCUS categories
- `ChargeCategory`: **Usage**, **Purchase** (commitment fees, marketplace, support), **Tax**,
  **Credit**, **Adjustment** (refunds, rounding, other provider corrections).
- `ChargeClass = Correction` marks a row that corrects a charge from a previous billing period.
- `ChargeFrequency`: One-Time, Recurring, Usage-Based.

## Provider equivalents
AWS CUR `line_item_line_item_type`: Usage, DiscountedUsage (RI-covered), SavingsPlanCoveredUsage,
SavingsPlanNegation, RIFee, SavingsPlanRecurringFee, SavingsPlanUpfrontFee, Fee, Tax, Credit,
Refund, EdpDiscount, PrivateRateDiscount, BundledDiscount. Azure usage details use `ChargeType`:
Usage, Purchase, Refund, UnusedReservation, UnusedSavingsPlan, RoundingAdjustment.

## Steps
1. **Report usage by `EffectiveCost`** over Usage rows (including unused commitment) for
   engineering views; exclude Purchase rows to avoid counting an upfront commitment fee and its
   amortised share.
2. **Report cash by `BilledCost`** over all categories for finance and invoice reconciliation.
3. **Credits**: show as a separate line, not netted silently into team cost, unless the credit is
   genuinely theirs (e.g. a migration credit for their workload). Promotional credits expire;
   reporting cost net of credits hides the cliff.
4. **Corrections**: decide a policy. Either restate the original period (accurate trends, moving
   history) or book in the period received (stable history, noisy month). Finance usually wants the
   latter for closed months; trend charts the former. Keep both possible by keeping
   `ChargeClass` and `ChargePeriodStart`.
5. **Tax**: allocate pro rata to usage or keep central; most teams cannot influence tax.
6. **Refunds / SLA credits**: route to the team that suffered the incident or central, by policy.

```sql
SELECT ChargeCategory, ChargeClass, SUM(BilledCost) billed, SUM(EffectiveCost) effective
FROM focus_costs WHERE BillingPeriodStart = '2026-09-01'
GROUP BY 1,2 ORDER BY 1,2;
```

## Gotchas
- A large negative day is usually a credit or refund row, not an optimisation.
- Corrections dated in a closed period break month-end numbers already reported; flag them in the
  next month's pack.
- AWS SavingsPlanNegation rows offset covered usage; filtering only `Usage` line types loses them.

## Verify
- [ ] Every report states which categories and cost metric it includes.
- [ ] Invoice total equals SUM(BilledCost) over all categories for the billing period.
