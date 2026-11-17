---
id: computing-software.cloud-infrastructure-engineering.google-cloud.carbon-footprint-dashboard-and-export
name: carbon-footprint-dashboard-and-export
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, carbon-footprint-dashboard, carbon-footprint-export, scope-3, ghg-reporting]
level: practitioner
status: docs-checked
description: "Read the Google Cloud Carbon Footprint dashboard per billing account, export monthly data to BigQuery via Data Transfer Service, location vs market based."
sources: ["https://docs.cloud.google.com/carbon-footprint/docs/view-carbon-data", "https://docs.cloud.google.com/carbon-footprint/docs/export", "https://docs.cloud.google.com/carbon-footprint/docs/iam"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Carbon footprint dashboard and export

## 1. Access
Carbon Footprint data is per billing account. Permission `billing.accounts.getCarbonInformation` (plus
`billing.accounts.list` and `billing.accounts.get` for the dashboard) comes from `roles/billing.carbonViewer`
(cannot see detailed billing data), `roles/billing.admin`, `roles/billing.viewer` or `roles/billing.linkAdmin`.
Grant them from the Billing account settings page by a billing account administrator, not project-level IAM.
No billing spend access is needed and there is no API to enable. The dashboard is under Tools in the console.

## 2. What the numbers are
- Estimated emissions for covered Google Cloud services for the selected billing account. Shown in tCO2e on the
  dashboard and kgCO2e in the export.
- Two tabs, using Greenhouse Gas Protocol Scope 2 definitions: **Market-based** (scope 1, scope 2 market-based,
  scope 3) and **Location-based** (scope 1, scope 2 location-based, scope 3). Scope 1 and 3 are identical across
  tabs. Corporate reporting usually needs both, so state which one you use.
- Data for the previous month can take up to 21 days to appear.
- Summary cards: annual footprint (past 12 complete months) and the past month versus the previous one. Charts:
  monthly emissions and emissions by region on both tabs; by project and by product on the location-based tab only.
- An Active Assist Unattended Project Recommender card suggests reclaiming or shutting down unattended projects.

## 3. Export to BigQuery
The export uses BigQuery Data Transfer Service and creates a monthly partitioned table `carbon_footprint` in your
dataset. Each month's data is exported on the 15th of the following month. You pay for the BigQuery storage and
queries.
```bash
bq mk --transfer_config --target_dataset=DATASET --display_name=NAME \
  --params='{"billing_accounts":"BILLING_ACCOUNT_IDS"}' \
  --data_source='61cede5a-0000-2440-ad42-883d24f8f7b8'
```
- Needed on the project: `resourcemanager.projects.update`, `serviceusage.services.enable`,
  `bigquery.transfers.update`; on the billing account `billing.accounts.getCarbonInformation`.
- Outside the console, enroll the data source first with the Enroll Data Sources API.
- Backfill is not automatic: schedule a backfill (earliest start 2021-02-15, which carries January 2021 data).
- With VPC Service Controls, add an ingress rule for the BigQuery API and BigQuery Data Transfer Service API
  with source "All sources allow" for the identity named on the export page.
- Billing account IDs use the format XXXXXX-XXXXXX-XXXXXX; separate several with commas.

Example, location-based total by service per month (column names from the export page):
```sql
SELECT usage_month, service.description,
       SUM(carbon_footprint_total_kgCO2e.location_based) AS kg
FROM `<PROJECT>.<DATASET>.carbon_footprint`
GROUP BY 1, 2 ORDER BY usage_month DESC, kg DESC;
```
Other columns include `project.id`, `location.region`, `carbon_model_version`,
`carbon_footprint_kgCO2e.scope1`, `.scope3` and `.scope2.location_based`.

## Verify
- [ ] Dashboard totals match the BigQuery export for the same month and billing account, allowing for the model version.

## Checked
2026-11-09. Confirmed against View Carbon Footprint data, Export your carbon footprint (both read in full) and
Cloud Billing IAM permissions and roles for Carbon Footprint (read in full). The methodology page was not read.
Removed: the reading-the-numbers claims about restating history and rounding, the "create early" gotcha, the
"low CO2" region-picker advice and idle-VM advice, and the claim that the dashboard filters by service.
Method: documentation only; no commands were run.
