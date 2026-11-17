---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.focus-specification
name: focus-specification
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, focus-specification, focus, finops-open-cost-and-usage-specification, billed-cost, effective-cost, list-cost, contracted-cost, focus-export, normalisation]
level: practitioner
status: docs-checked
description: "Normalise multi-provider billing data with FOCUS: key columns and cost metrics, native FOCUS exports per provider, mapping gaps, and validating a dataset."
sources: ["https://focus.finops.org/focus-specification/", "https://docs.aws.amazon.com/cur/latest/userguide/table-dictionary-focus-1-0-aws.html", "https://learn.microsoft.com/azure/cost-management-billing/dataset-schema/cost-usage-details-focus", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FOCUS: normalising cost data

FOCUS (FinOps Open Cost and Usage Specification) is an open specification defining a common schema
and minimum requirements for billing data, aligned with FinOps Framework terminology, so that
chargeback, allocation, budgeting and forecasting work the same on any compliant dataset. The
published specification was at version 1.4 when checked; exports from providers may lag, so
check the version your exports produce.

## Key columns (as listed in the Azure FOCUS dataset)
- Cost metrics: **ListCost** (ListUnitPrice x PricingQuantity), **ContractedCost**
  (ContractedUnitPrice x PricingQuantity), **BilledCost** (basis for invoicing, inclusive of
  reduced rates and discounts, excluding amortisation of upfront charges), **EffectiveCost**
  (amortised cost after discounts and the applicable portion of prepaid purchases; use it for
  allocation and unit costs).
- Who/what: `BillingAccountId`, `SubAccountId`, `ServiceName`, `ServiceCategory`, `ResourceId`,
  `RegionId`, `Tags` (custom key-value pairs as a JSON object), `SkuId`, `SkuPriceId`.
- When: `ChargePeriodStart`, `BillingPeriodStart` (with matching end columns).
- Type: `ChargeCategory`, `ChargeClass` (marks corrections to charges invoiced in a previous
  period), `PricingCategory`, `CommitmentDiscountId`, `CommitmentDiscountStatus` (consumption vs
  unused portion of a commitment; Azure's page notes it is currently empty there), `InvoiceId`.
- Quantity: `ConsumedQuantity` + `ConsumedUnit`, `PricingQuantity` + `PricingUnit`.

## Getting FOCUS data
- AWS: Data Exports offers "FOCUS 1.0 with AWS columns" (SQL table `FOCUS_1_0_AWS`, no table
  configurations) plus five AWS columns `x_CostCategories`, `x_Discounts`, `x_Operation`,
  `x_ServiceCode`, `x_UsageType`; a FOCUS 1.2 variant also exists. Management-account exports cover
  member accounts; member exports cover only their own account.
- Azure: Cost Management documents a FOCUS cost and usage details dataset.
- Google Cloud: a FOCUS usage cost export to BigQuery (Preview) whose columns generally map to the
  detailed usage cost export.
- Other vendors: check their documentation for native FOCUS data.

## Steps
1. Land each provider's FOCUS export in one warehouse table partitioned by `BillingPeriodStart`.
2. Union with a provider column; keep provider-specific extension columns (AWS uses an `x_` prefix)
   for edge cases.
3. Validate: `SUM(BilledCost)` per `InvoiceId` ties to invoices; no null `ChargeCategory`.
4. Normalise tags (key case, synonyms like `Team`/`team`/`owner`) in a view, not in source.

## Gotchas
- Provider implementations differ in edge cases (marketplace, support, credits); read each
  provider's mapping notes.
- Not every provider fills every column (see the CommitmentDiscountStatus note above).

## Verify
- [ ] One query returns month-to-date cost by service across all clouds.
- [ ] Billed cost per invoice reconciles.

## Checked

Method: docs-checked 2026-11-09 against the FOCUS specification page (cover page only; body not rendered), AWS FOCUS 1.0 table dictionary page, Azure FOCUS cost and usage details dataset page (column definitions), Google Cloud export-data-bigquery overview. Removed unconfirmed: allowed values of ChargeCategory, PricingCategory and CommitmentDiscountStatus, v1.0 release year, the EffectiveCost-vs-BilledCost term-equality check, Google FOCUS "view" description, OCI claim.
