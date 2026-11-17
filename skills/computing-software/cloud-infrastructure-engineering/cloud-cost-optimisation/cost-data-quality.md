---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-quality
name: cost-data-quality
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, cost-data-quality, data-validation, completeness-checks, dbt-tests, reconciliation]
level: practitioner
status: docs-checked
description: "Make cost data trustworthy with automated checks: completeness, invoice tie-out, nulls, duplicates and schema changes, run as dbt data tests."
sources: ["https://www.finops.org/framework/capabilities/data-ingestion/", "https://docs.getdbt.com/docs/build/data-tests", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/billedcost.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost data quality checks

Untrusted cost data kills FinOps adoption faster than anything. Test it like production data.

## What the FinOps Framework asks for
The Data Ingestion capability includes defining mechanisms to evaluate data quality and
consistency, notifying data source owners and data users of availability, quality or
consistency issues, maintaining data timeliness and availability, and building
observability and alerting so teams know when ingestion exceeds established boundaries.
Its listed practices include data completeness checks, regular validation of data source
content with a clear view of when it changes, and periodic reconciliation of invoices
and usage data against native provider tool data versus normalised data. Changes made
outside source systems should be minimised and reconciled back to source.

## Checks to automate (run after every load)
| Check | What to test |
|---|---|
| Completeness | Every expected billing account is present in the load; no day is missing |
| Final reconciliation | In FOCUS data, the sum of `BilledCost` for an `InvoiceId` must match the payable amount on the invoice with that id |
| Nulls | `BilledCost`, `ChargePeriodEnd`, `ChargeCategory` and `ServiceName` are mandatory columns that MUST NOT be null in a FOCUS dataset |
| Duplicates | A uniqueness test on your line-item id or row key per billing period |
| Schema drift | Expected columns present; alert on added or removed columns |
| FOCUS conformance | Run the FOCUS validator; the Framework lists "FOCUS validator checks complete successfully" as a data ingestion check |

## Implementation
dbt data tests are SQL select statements that return failing rows; zero rows means the
assertion passes. Singular tests are one-off `.sql` files in the tests directory, run by
`dbt test`. dbt ships four generic tests: `unique`, `not_null`, `accepted_values` and
`relationships`. Use `unique` and `not_null` on the keys above and a singular test for
the invoice tie-out. Alert the data owner on failure and mark dashboards stale instead of
silently showing wrong numbers.

## Gotchas
- Appending instead of replacing a partition double-counts cost: the classic duplicate.
- Provider schema changes can silently null columns your queries expect.

## Verify
- [ ] Every check has an owner and an alert route.
- [ ] Tie-out of finalised months against invoices is recorded.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Data Ingestion page and the dbt data-tests page (both downloaded and grepped), plus the FOCUS v1.2 BilledCost, ChargePeriodEnd, ChargeCategory and ServiceName column pages (raw GitHub).
Removed as unconfirmed by the pages read: freshness window (36 h), 1% tie-out tolerance, 2-point allocation drift, 3x outlier rule with 7-day median, "last 30 days" verify item, dbt_utils.recency, Great Expectations, AWS/Azure/BigQuery API commands, CUR legacy to 2.0 example, UnallocatedCost % check, snapshot-of-finalised-months advice. focus.finops.org specification page is a landing page only (columns read from the spec repository instead).
