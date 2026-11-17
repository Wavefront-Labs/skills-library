---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-sql-overprovisioned-and-idle-recommenders
name: cloud-sql-overprovisioned-and-idle-recommenders
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, recommender, cloud-sql-overprovisioned-recommender, cloud-sql-idle-recommender, rightsizing, cloud-sql]
level: practitioner
status: docs-checked
description: "Use the Cloud SQL overprovisioned and idle instance recommenders: what they analyse, how to list recommendations and insights, roles needed, and how to act safely."
sources: ["https://cloud.google.com/sql/docs/mysql/recommender-sql-overprovisioned", "https://cloud.google.com/sql/docs/mysql/recommender-sql-idle", "https://cloud.google.com/recommender/docs/recommenders#cloud_sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SQL overprovisioned and idle recommenders

## Recommenders (Recommenders page)
| Recommender ID | Purpose |
|---|---|
| `google.cloudsql.instance.OverprovisionedRecommender` | Resize overprovisioned SQL instances |
| `google.cloudsql.instance.IdleRecommender` | Remove unused SQL instances |
| `google.cloudsql.instance.UnderprovisionedRecommender` | Optimise underprovisioned instances |
| `google.cloudsql.instance.OutOfDiskRecommender` | Prevent out-of-disk outage |
| `google.cloudsql.instance.PerformanceRecommender` | Performance (for example MySQL open tables, PostgreSQL transaction id utilisation) |

Both cost recommenders are in the Standard Recommender pricing tier and are included in the BigQuery export.

## How they work
- Both analyse only primary instances older than 30 days, using a 30-day observation period, and skip read replicas. Recommendations are generated every 24 hours.
- Overprovisioned: also skips instances configured for high availability (HA). It flags an instance when peak CPU and/or memory utilisation in the period is low, and generates a recommendation when estimated monthly savings reach the page's stated threshold. Thresholds are conservative, and the suggested machine type has at least 8 vCPUs and 32 GB. Subtypes: insights `LOW_CPU_UTILIZATION` / `LOW_MEMORY_UTILIZATION`, recommendation `CHANGE_INSTANCE_SIZE`.
- Idle: flags instances whose activity is below a threshold. Insight subtype `LOW_ACTIVITY`, recommendation subtype `SHUTDOWN_INSTANCE`.

## List and inspect
Roles: view with `recommender.cloudsqlViewer` or `cloudsql.viewer`; apply with `recommender.cloudsqlAdmin`, `cloudsql.editor` or `cloudsql.admin`. Enable the Recommender API.
```bash
gcloud recommender recommendations list --project=PROJECT_ID --location=LOCATION \
  --recommender=google.cloudsql.instance.OverprovisionedRecommender    # or IdleRecommender
gcloud recommender insights list --project=PROJECT_ID --location=LOCATION \
  --insight-type=google.cloudsql.instance.CpuUsageInsight
```
Insight types: `CpuUsageInsight` and `MemoryUsageInsight` (overprovisioned), `ActivityInsight` (idle). The idle insight panel shows disk bytes used, max CPU and memory utilisation, max disk read and write ops, and the observation start and end dates. The console route is the banner on the Cloud SQL Instances page or Active Assist, "Reduce Cloud SQL instance cost" card.

## Acting
- Evaluate the insights and in-context charts and consult the owning team first: Google warns the flagged instance may be inadvertently over-sized or idle.
- Overprovisioned: edit the instance to fewer vCPUs or less memory. You need not match the recommended size exactly; use your judgement. The page notes that the bigger the size, the greater the operational latency.
- Idle: it may be intentionally idle. If not, stop or delete it. Stopping suspends instance charges but storage and IP address charges continue. Create a backup first to avoid data loss.
- Dismiss de-emphasises a recommendation; Cancel closes the panel without acting.

## Gotchas
- HA instances and read replicas are not analysed by the overprovisioned recommender; size those by other means.
- 30-day windows can miss month-end or batch peaks; check your own metrics.

## Checked
Confirmed 2026-11-08 against the two Cloud SQL recommender pages and the Recommenders page. Removed claims the pages do not state: the `gcloud sql instances patch` commands, `mark-succeeded` usage, metric names beyond those listed, the p99/70 percent targets, restart/downtime behaviour, committed-use discount interplay, and the `--format` projection.
Method: docs-only read of cited pages, 2026-11-08
