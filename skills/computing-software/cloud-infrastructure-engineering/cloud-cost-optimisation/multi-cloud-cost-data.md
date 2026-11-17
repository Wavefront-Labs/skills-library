---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.multi-cloud-cost-data
name: multi-cloud-cost-data
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, multi-cloud-cost-data, saas-cost-data, billing-export, data-exports, cur-2-0, azure-cost-exports, bigquery-billing-export, cost-data-lake]
level: practitioner
status: draft
description: "Ingest cost data from AWS, Azure, GCP and SaaS into one store: which export to enable per provider, landing layout, refresh and restatement handling, and currency."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/what-is-data-exports.html", "https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery", "https://www.finops.org/framework/capabilities/data-ingestion/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-cloud and SaaS cost data ingestion

## Enable the right export per provider
| Provider | Export | Scope | Notes |
|---|---|---|---|
| AWS | Data Exports: CUR 2.0 and/or FOCUS 1.0 → S3 Parquet | management (payer) account | include resource ids; hourly granularity if you need it; overwrite mode per month |
| Azure | Cost Management exports (actual + amortised, or FOCUS) → storage account | EA enrolment / MCA billing account or billing profile | subscription-level exports miss reservations purchased elsewhere |
| GCP | Cloud Billing export to BigQuery: standard + **detailed** (resource-level) + pricing | billing account | only from the time it's enabled — **no backfill**; enable on day one |
| OCI / others | FOCUS / cost reports to object storage | tenancy | |
| SaaS (Datadog, Snowflake, GitHub, OpenAI…) | vendor usage APIs / FOCUS where offered | org | normalise to FOCUS columns |

## Pipeline
1. Land raw exports unchanged (bronze), partitioned by provider/billing period.
2. **Handle restatements**: providers rewrite the current and previous month repeatedly; replace
   whole billing-period partitions on each load instead of appending.
3. Transform to a common schema (FOCUS) in a silver layer; add enrichment (team, product) in gold.
4. Convert currency at a documented rate (billing currency → reporting currency) and keep both.
5. Schedule loads after provider refresh cadence (several times a day); show "data as of" on dashboards.

## Gotchas
- Missing linked accounts/subscriptions: reconcile account lists against the org/billing account each month.
- Detailed exports are large (GBs/day at scale) — partition and cluster; query costs add up.
- Permissions: billing data reveals the whole estate; restrict raw access, expose curated views.

## Verify
- [ ] Monthly totals per provider match each provider's console within rounding.
- [ ] Dashboards display data freshness.
