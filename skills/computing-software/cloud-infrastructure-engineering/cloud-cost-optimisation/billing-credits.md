---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.billing-credits
name: billing-credits
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-billing, billing-credits, refunds, support-charges, tax, promotional-credits, charge-category, focus-chargecategory, credit-allocation]
level: practitioner
status: docs-checked
description: "Handle non-usage bill lines correctly: credits, refunds, support, tax, marketplace and purchases — how to identify them in billing data and allocate or exclude them in reports."
sources: ["https://focus.finops.org/focus-specification/", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-cur2-line-item.html", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/standard-usage", "https://learn.microsoft.com/en-us/azure/cost-management-billing/automate/understand-usage-details-fields"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credits, refunds, support and tax lines

Usage lines are the bulk of a bill, but the lines that aren't usage are where reports disagree with invoices.

## Identify them
- **FOCUS**: `ChargeCategory` is one of Usage, Purchase, Tax, Credit, Adjustment (never null). Refunds
  sit inside their category (Usage and Purchase "including refunds"), and Credit covers promotional
  credits or corrections to them. `ChargeClass` is null or `Correction`; `Correction` marks a row that
  corrects a previously invoiced billing period.
- **AWS CUR 2.0**: `line_item_line_item_type` includes `Usage`, `Credit`, `Refund`, `Tax`, `Discount`,
  `BundledDiscount`, `Fee`, `RIFee`, `DiscountedUsage`, `SavingsPlanUpfrontFee`,
  `SavingsPlanRecurringFee`, `SavingsPlanCoveredUsage` and `SavingsPlanNegation` (covered usage is
  offset by the matching negation line). `Discount` lines vary by discount: parse the line item
  description column.
- **GCP export**: `credits` is a repeated struct per row with `credits.type`, `credits.name` and
  `credits.amount`. Types include `SUSTAINED_USAGE_DISCOUNT`, `COMMITTED_USAGE_DISCOUNT`,
  `COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE`, `FEE_UTILIZATION_OFFSET`, `PROMOTION`, `FREE_TIER`,
  `DISCOUNT`, `RESELLER_MARGIN` and `SUBSCRIPTION_BENEFIT`. Net cost is `cost` plus the sum of
  `credits.amount` (the page's own queries add it, using `IFNULL` over `UNNEST(credits)`).
- **Azure** (usage details): `ChargeType` indicates usage (`Usage`), purchase (`Purchase`) or refund
  (`Refund`); reservation records also use `UnusedReservation`.

## Allocation rules (write them down)
1. **Promotional credits** (startup, migration incentives): report gross cost to teams so they
   see true run-rate; account for credits centrally — otherwise costs "jump" when credits expire.
2. **Commitment discounts**: amortise to consuming resources (effective cost).
3. **Negotiated enterprise discounts**: apply proportionally so team costs match the invoice, or
   show list-equivalent if contracts are confidential — be consistent.
4. **Support**: allocate proportionally to spend, or keep central.
5. **Tax**: usually excluded from team showback, included in finance reconciliation.
6. **Refunds/corrections**: apply to the period and owner of the original charge.

## Verify
- [ ] Sum of all lines for the month equals the invoice total (within rounding).
- [ ] Credit expiry dates tracked with forecast impact.

## Checked
2026-11-08. Confirmed against the FOCUS v1.2 ChargeCategory and ChargeClass column pages, the AWS CUR 2.0 line item table dictionary (allowed `line_item_line_item_type` values), the Google Cloud standard usage export schema (`credits` struct, credit types, net-cost queries) and the Azure usage details fields page (`ChargeType`).
Removed: `EdpDiscount`/`PrivateRateDiscount` (not listed by AWS), `UnusedSavingsPlan` and the Azure Prepayment statement (not on the Azure page), the EDP/PPA program names and the claim that support is often a percentage of spend. The allocation rules are practice guidance, not vendor claims.
Method: documentation only; no commands were run.
