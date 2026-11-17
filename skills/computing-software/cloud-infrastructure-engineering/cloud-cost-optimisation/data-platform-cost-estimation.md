---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.data-platform-cost-estimation
name: data-platform-cost-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, planning-and-estimating, data-platform-cost-estimation, data-warehouse-cost, snowflake, bigquery, databricks, cost-estimation]
level: advanced
status: draft
description: "Estimate data and analytics platform cost: storage growth, ingestion, transform and query compute in credits, slots or DBUs, concurrency, and the cloud infrastructure beneath."
sources: ["https://www.snowflake.com/pricing/", "https://cloud.google.com/bigquery/pricing", "https://www.databricks.com/product/pricing", "https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Estimating data and analytics platform cost

Data platform cost scales with data volume, query patterns and freshness requirements, not with
servers. Estimate each of those explicitly.

## Drivers to collect
- Raw data ingested per day, compression ratio, retention, number of copies (raw, staged, curated,
  time travel / fail-safe, backups).
- Transform workload: jobs per day, data scanned per job, runtime on a reference size.
- Query workload: BI users, dashboards and refresh frequency, ad-hoc analysts, peak concurrency.
- Freshness: batch daily vs hourly vs streaming (streaming keeps compute on all the time).

## Model per platform
**Snowflake** (credits): warehouse size credits/hour (XS=1, S=2, M=4, L=8, ...) x hours running
(including auto-suspend tail, default 600 s, set to 60 s) per warehouse; plus serverless features
and cloud services above 10% of daily compute; storage per TB-month (compressed).

**BigQuery**: on-demand = TiB scanned x price per TiB (first 1 TiB/month free), or editions =
slots x hours (baseline + autoscaling) x slot-hour price; storage active vs long-term
(90 days unmodified), logical vs physical billing model; streaming inserts / Storage Write API.

**Databricks**: DBUs per hour per cluster type (jobs compute cheaper than all-purpose; SQL
warehouses; serverless includes infrastructure) x hours, plus the cloud VMs and storage for classic
compute.

## Steps
1. Build a per-workload table: workload, compute size, runtime/day, days/month -> compute units.
2. Price at your contracted rate (capacity commitments discount credits/DBUs).
3. Add storage growth month by month for 12-36 months; storage compounds.
4. Add egress (BI tools outside the cloud region), orchestration, catalogue and monitoring.
5. Run low/expected/high and identify the dominant driver (usually query compute).

## Gotchas
- Unpartitioned tables make BigQuery on-demand scans grow with history; assume partition pruning
  only if the design enforces it.
- Dashboards with auto-refresh every few minutes keep warehouses awake all day.
- Proofs of concept on small data underestimate join and shuffle cost at production scale.

## Verify
- [ ] Estimate separates storage, ingestion, transform and query compute.
- [ ] Assumptions about auto-suspend, partitioning and refresh rates are written down.
