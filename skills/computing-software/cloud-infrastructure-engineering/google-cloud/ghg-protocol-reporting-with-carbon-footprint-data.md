---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ghg-protocol-reporting-with-carbon-footprint-data
name: ghg-protocol-reporting-with-carbon-footprint-data
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, ghg-protocol-reporting, carbon-footprint-methodology, scope-3, location-based, market-based]
level: practitioner
status: docs-checked
description: "Use Google Cloud Carbon Footprint data in GHG Protocol reports: location- vs market-based figures, cloud as your scope 3, team allocation, and caveats."
sources: ["https://cloud.google.com/carbon-footprint/docs/methodology", "https://cloud.google.com/carbon-footprint/docs/export", "https://ghgprotocol.org/corporate-standard"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHG Protocol reporting with Carbon Footprint data

## What Carbon Footprint gives you
Monthly emissions (kgCO2e) per project, product and region, using the GHG Protocol's location-based and market-based
standards:
- **Location-based**: hourly energy use multiplied by the grid carbon intensity at that location and hour; it ignores
  energy purchasing contracts such as EACs or PPAs.
- **Market-based**: includes the effect of Google's carbon-free electricity purchases; the page says customers compiling
  annual Scope 3 inventories will likely find the market-based footprint most useful.
- Google Cloud allocates its own Scope 1, 2 and 3 emissions to customers by usage; you integrate that allocated data
  into your own reports as Scope 3 (indirect, value chain) emissions.
- Exported to BigQuery via the BigQuery Data Transfer Service: a monthly partitioned table named `carbon_footprint` in
  a dataset of your choice. Data for a month is exported on the 15th of the following month, and a backfill can request
  history back to January 2021.

## In your inventory
Treat the allocated cloud emissions as Scope 3 in your inventory. Example against the documented export columns:
```sql
SELECT
  usage_month,
  project.id AS project_id,
  carbon_footprint_total_kgCO2e.location_based AS total_location_based
FROM `PROJECT.DATASET.carbon_footprint`
ORDER BY usage_month DESC, total_location_based DESC
```
The export page's sample query also selects `billing_account_id`, `service.id`, `location.region`,
`carbon_footprint_kgCO2e.scope1`, `.scope2.location_based`, `.scope3` and `carbon_model_version`. Inspect the table
schema for the market-based columns before reporting them.

## Allocation
Group by `project.id` joined to project labels (team, cost centre) for internal chargeback of emissions alongside cost.

## Methodology notes to disclose
- Monthly data, exported on the 15th of the following month.
- Emissions are allocated by Google's model (SKUs purchased are the primary allocation basis), not metered per VM.
- Market-based figures use annual emission factors and a scaling factor updated once per year, so they reflect the
  previous year's renewable activity rather than a dynamic view.
- Scope 3 in the model includes embodied emissions of data centre equipment and buildings.
- The export records a `carbon_model_version`; keep exports versioned so figures can be compared across methodology changes.

## Gotchas
- The export wizard works per Cloud Billing account; you need access to the account (and project) to configure and view it.
- VPC Service Controls need an ingress rule for the BigQuery API and BigQuery Data Transfer Service API.

## Verify
- [ ] Annual figure reconciles between console and BigQuery export; methodology note attached to the report.

## Checked
2026-11-09: read the Carbon Footprint methodology and export pages in full-text form (location and market-based
definitions, Scope 3 use, 15th-of-month export, table name, sample query columns, VPC-SC note). Removed: the
market_based column name and Category 1 claim, reseller and marketplace gotchas, restatement claim (not stated on the
pages). GHG Protocol corporate standard page is listed for context only.
Method: documentation only; no commands were run.
