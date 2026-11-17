---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.gcp-billing-export
name: gcp-billing-export
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, gcp-billing-export, bigquery-billing, detailed-usage-cost, pricing-export, cloud-billing-data]
level: practitioner
status: docs-checked
description: "Enable Google Cloud billing export to BigQuery (standard, detailed, pricing), understand credits and labels, and write cost queries that reconcile to the invoice."
sources: ["https://cloud.google.com/billing/docs/how-to/export-data-bigquery", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/detailed-usage", "https://cloud.google.com/billing/docs/how-to/bq-examples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Cloud billing export to BigQuery

## Export types
- **Standard usage cost**: account ID, invoice date, services, SKUs, projects, labels, locations,
  cost, usage, credits, adjustments and currency. Good for broad trends.
- **Detailed usage cost**: everything in standard plus resource-level data (for example the VM or
  SSD generating the usage) through `resource.name` and `resource.global_name` for supported
  services. Needed for resource-level allocation. For GKE you must also enable cost allocation.
- **FOCUS usage cost** (Preview): the detailed data normalised to the FOCUS specification.
- **Pricing**: account pricing data (SKUs, pricing units, currency, tiers). Also available from the
  console Pricing page and the Cloud Pricing API.
- **Committed use discounts metadata** (Preview) and a reseller-only **Rebilling** export exist.
- BigQuery storage and query usage is charged separately.

## Data availability (enable on day one)
- A dataset in a multi-region location (US or EU) is backfilled from the start of the previous
  month relative to first enablement; the backfill can take up to five days.
- A dataset in a supported region location only holds data from the date you enabled export.
- Pricing data is never backfilled.
- If you disable, re-enable or move the export to another project or dataset, earlier data is not
  copied; join the old and new datasets manually.
- Dataset location cannot be changed after creation, and only some regions are supported
  (otherwise saving fails with an Invalid dataset region error).

## Setup
1. Create a dedicated project and BigQuery dataset; choose its location deliberately.
2. In Cloud Billing, enable each export type into the dataset.
3. The detailed export table is named `gcp_billing_export_resource_v1_<BILLING_ACCOUNT_ID>`; the
   standard one follows the `gcp_billing_export_v1_<BILLING_ACCOUNT_ID>` pattern.

## Reconciling cost
Per Google's examples, the invoice total is `SUM(cost)` plus the sum of `credits.amount`, grouped
by `invoice.month`. Credits include committed usage discounts, so unnesting `credits` is required.
```sql
SELECT invoice.month,
  SUM(cost) + SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0)) AS total
FROM `PROJECT_ID.DATASET.gcp_billing_export_v1_XXXXXX-XXXXXX-XXXXXX`
GROUP BY 1 ORDER BY 1;
```
The examples also show `total_exact`, which casts to NUMERIC to avoid floating-point rounding.
Group by `invoice.month`, not usage date, to match invoices.

## Labels and projects
`labels` (resource labels), `project.labels` and `tags` (resource tags, with `inherited` and
`namespace` fields) are repeated key/value structs; UNNEST them to allocate. Newly created projects
may lack project information on usage within 24 hours of creation.

## Gotchas
- Forgetting to UNNEST credits gives gross, not net, cost.
- The detailed export is large; filter queries by time to control BigQuery cost.

## Verify
- [ ] Monthly total by `invoice.month` matches the invoice within tax/rounding.

## Checked

Method: docs-checked 2026-11-09 against Cloud Billing export-data-bigquery page, detailed usage cost table schema page (searched, not read in full) and BigQuery example queries page (invoice total example). Removed unconfirmed: partition column filter advice, the "credits are negative" note, org policy label enforcement, permission role names.
