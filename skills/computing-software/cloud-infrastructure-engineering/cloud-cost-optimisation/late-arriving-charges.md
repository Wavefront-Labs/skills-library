---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.late-arriving-charges
name: late-arriving-charges
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, billing-concepts, late-arriving-charges, billing-period, charge-period, month-end-close, data-restatement, focus-specification]
level: practitioner
status: draft
description: "Handle billing period vs charge period and late charges: why a closed month keeps changing, when data is final, and how to report restated and late-dated rows."
sources: ["https://focus.finops.org/", "https://docs.aws.amazon.com/cur/latest/userguide/understanding-report-versions.html", "https://learn.microsoft.com/azure/cost-management-billing/costs/understand-cost-mgt-data", "https://cloud.google.com/billing/docs/how-to/bq-examples"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Billing period vs charge period and late-arriving charges

Two time axes live on every row: when the usage happened (**charge period**) and which invoice it
lands on (**billing period**). Most "the numbers changed" complaints come from mixing them.

## Definitions (FOCUS)
- `ChargePeriodStart/End`: the usage window (hour or day).
- `BillingPeriodStart/End`: the invoice month the row belongs to.
- A charge for 30 September usage that arrives on 3 October normally still has billing period
  September, until the period is invoiced. After invoicing, corrections arrive in a later billing
  period (`ChargeClass = Correction`).

## Provider behaviour
- **AWS**: the current month's CUR is rewritten several times a day; the prior month is updated
  until the bill is finalised early in the following month; later refunds and credits land on a
  later bill.
- **Azure**: usage arrives 8-24 h late, some services up to 72 h; month-end data settles a few days
  into the next month; invoices issue after that.
- **Google Cloud**: rows can be inserted for past usage dates; load incrementally by `export_time`,
  analyse by `usage_start_time`, and use `invoice.month` for the billing period.

## Steps
1. **Load by billing period, replacing whole periods.** Overwrite the open month(s) each load
   instead of appending, or you double count rewritten rows.
2. **Keep both dates** in the model; analysis and trends use charge period, invoice reconciliation
   uses billing period.
3. **Close the month**: on working day N (e.g. 5) snapshot the finalised month into a closed table
   for finance; later corrections go to the next month in finance views.
4. **Flag late rows**: a row whose charge period is earlier than its billing period, or that arrived
   after close, gets a `late_flag` so analysts can explain variances.
5. **Explain to stakeholders**: dashboards mark the last 2-3 days as provisional.

```sql
-- rows booked to October that relate to earlier usage
SELECT ChargeCategory, ChargeClass, SUM(BilledCost)
FROM focus_costs
WHERE BillingPeriodStart='2026-10-01' AND ChargePeriodStart < '2026-10-01'
GROUP BY 1,2;
```

## Gotchas
- Appending each export load produces a month that grows 3x; always replace the period.
- Daily trend charts by billing period put all corrections on day 1.
- Monthly fees (support, marketplace, upfront commitments) carry a charge period of the whole month
  or term; spread them for daily views.

## Verify
- [ ] Loads are idempotent: re-running a load leaves totals unchanged.
- [ ] Finance month-end numbers come from a closed snapshot that does not change.
