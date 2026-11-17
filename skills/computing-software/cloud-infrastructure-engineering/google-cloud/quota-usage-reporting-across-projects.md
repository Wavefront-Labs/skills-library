---
id: computing-software.cloud-infrastructure-engineering.google-cloud.quota-usage-reporting-across-projects
name: quota-usage-reporting-across-projects
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, quotas, quota-usage-report, quota-dashboards, cloud-monitoring, promql, capacity-planning]
level: practitioner
status: docs-checked
description: "Report quota usage against limits across many projects with serviceruntime quota metrics, a metrics scope, PromQL ratios, and a BigQuery-backed fleet report."
sources: ["https://cloud.google.com/monitoring/alerts/using-quota-metrics", "https://cloud.google.com/docs/quotas/view-manage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quota usage reporting across projects

## 1. The metrics (monitored resource `consumer_quota`)
| Metric | Meaning |
|---|---|
| `serviceruntime.googleapis.com/quota/allocation/usage` | allocation quota usage |
| `serviceruntime.googleapis.com/quota/limit` | the limit |
| `serviceruntime.googleapis.com/quota/rate/net_usage` | rate quota usage |
| `serviceruntime.googleapis.com/quota/exceeded` | quota exceeded errors |
All have the `quota_metric` label; only some have `limit_name` (a quota can have several limits, such as per-minute and per-day). The PromQL examples below also group by `project_id` and `location`.

## 2. One view for many projects
Create a monitoring project and add each project to its **metrics scope**
(`gcloud beta monitoring metrics-scopes create projects/<P> --project=<MON>`; command checked against the gcloud reference).
Then a dashboard chart in PromQL:
```promql
max by (project_id, quota_metric, location) ({"serviceruntime.googleapis.com/quota/allocation/usage", monitored_resource="consumer_quota", service="compute.googleapis.com"})
/
min by (project_id, quota_metric, location) ({"serviceruntime.googleapis.com/quota/limit", monitored_resource="consumer_quota", service="compute.googleapis.com", limit_name="CPUS-per-project-region"})
```
That is the documented pattern for Compute Engine CPU usage per region; the docs alert on it above a chosen ratio (0.75 in their example). For rate quotas use `increase({"serviceruntime.googleapis.com/quota/rate/net_usage", ...}[1m])` over the limit; a per-day window must be written as `[23h]` because a `[1d]` window cannot be saved.

## 3. Fleet report beyond a metrics scope
For the whole org, export periodically: Cloud Quotas API per project (`gcloud beta quotas info list --service=compute.googleapis.com --project=<P> --format=json` for limits) plus the Monitoring API time series for usage, written to BigQuery by a scheduled job.

## 4. Alert
Alert on the same ratio and on the `quota/exceeded` metric. A PromQL alerting policy can have only one condition. Find limit names with the "Identifying quota metrics and limit names" section of the using-quota-metrics page.

## Verify
- [ ] Dashboard lists the top quota ratios across all scoped projects.
- [ ] A synthetic test (use a sandbox quota up to the threshold) fires the alert.

## Checked

2026-10-28. Confirmed against: the Monitoring "using quota metrics" page (metric names, `consumer_quota` monitored resource, `quota_metric` and `limit_name` labels, the PromQL query patterns including `CPUS-per-project-region`, the `[23h]` window note, single-condition PromQL policies).

Removed: the unprefixed PromQL metric names and ratio join (not the documented form), the 0.8-for-10-minutes alert settings, the metrics-scope project-count claim, the professional-services solution (GitHub source not read), and the four gotchas (zero-usage series, per-region joins, rate windows, services without metrics).

Method: documentation only; no commands were run.
