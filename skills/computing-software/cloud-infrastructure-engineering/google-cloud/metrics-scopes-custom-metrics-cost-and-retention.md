---
id: computing-software.cloud-infrastructure-engineering.google-cloud.metrics-scopes-custom-metrics-cost-and-retention
name: metrics-scopes-custom-metrics-cost-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-monitoring, metrics-scope-multi-project, add-monitored-project, write-custom-metric, custom-metrics-write, monitoring-cost, metrics-ingestion-cost, metric-retention, metric-exports]
level: practitioner
status: docs-checked
description: "Organise Cloud Monitoring across projects with metrics scopes, write custom metrics within API limits, and know the retention and quota figures."
sources: ["https://docs.cloud.google.com/monitoring/settings/multiple-projects", "https://docs.cloud.google.com/monitoring/custom-metrics/creating-metrics", "https://docs.cloud.google.com/monitoring/quotas", "https://cloud.google.com/products/observability/pricing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics scopes, custom metrics, cost and retention

## 1. Metrics scopes
The metrics scope of a project determines the time-series data it can chart or alert on. The **scoping
project** is the project selected in the console; there is a one-to-one relationship between a scoping project
and its metrics scope.
- Default and supported size: a scope can include 375 projects. Up to 3,500 can be added by raising the
  "Monitored Projects / Monitoring Metrics Scope" quota, but Google guarantees performant queries and charts
  only for 375 (custom metrics and historical data queries suffer first).
- Console: Monitoring Settings, Metric Scope tab, Add Projects. Changes take about 60 seconds to propagate.
- Permissions: Monitoring Admin (`roles/monitoring.admin`) on the scoping project and on each project added or
  removed.
- Read access to Monitoring on the scoping project lets a principal view charts and alerting policies showing
  data stored in the scoped projects, so plan IAM accordingly.
- VPC Service Controls: the perimeter check runs when a project is added. If the perimeter exists first, the
  project must be in the same perimeter or bridged to the scoping project or the addition fails; configure the
  scope first to span perimeters.
- Removing a project means the scoping project can no longer chart or monitor its data. Charts, dashboards and
  alerting policies keep their configuration, but the series they display may change.
```bash
gcloud beta monitoring metrics-scopes create projects/<MONITORED_PROJECT> --project=<SCOPING_PROJECT>
gcloud beta monitoring metrics-scopes list projects/<SCOPING_PROJECT>
```

## 2. Write a custom metric
Use `timeSeries.create` with a `custom.googleapis.com/...` metric type and a monitored resource such as
`generic_task` (user-defined task) or `generic_node`; Google advises these over `global` for most uses.
- Do not write to a single time series faster than one point every 5 seconds (point end times must be at least 5
  seconds apart). To write more than one point to the same series, use a separate call per point; different time
  series have no such rate limit. Batch several series per request, and Google recommends at least 10 objects.
- Points must be written in order.
- If you write to a metric with no descriptor, one is created automatically with assumptions and defaults that
  may not match what you want; consider creating the descriptor yourself.
- User-defined metrics are a chargeable feature; see the Cloud Monitoring section of the pricing page.
- Delete a user-defined metric by deleting its descriptor (`metricDescriptors.delete`); this makes existing data
  inaccessible and it expires per the retention policy. Built-in descriptors cannot be deleted.

## 3. Retention (Monitoring quotas page)
- Custom, external, agent and Managed Service for Prometheus / OTLP metrics: 24 months. The same 24 months
  applies to metrics of some Google Cloud services (Compute Engine, GKE, Cloud Storage, BigQuery, Cloud SQL,
  load balancing).
- All other metric types (other Google Cloud metrics, Istio, AWS, log-based): 6 weeks.
- Where 24 months applies, data is kept at original sampling for 6 weeks, then down-sampled to 10-minute
  intervals. For Prometheus and OTLP data it is 1 week original, 5 weeks at 1-minute, then 10-minute intervals.
- Need longer or finer history? Read series with the Monitoring API on a schedule and store the results elsewhere.

## Verify
- [ ] The scoping project's charts show series from every intended project.
- [ ] Writers send at most one point per series every 5 seconds.

## Checked
2026-11-09. Confirmed against Configure a metrics scope (read in full), Cloud Monitoring quotas and limits (data
retention, monitored projects and ingestion rate sections), Creating user-defined metrics (searched for
rate limits, descriptor auto-creation, resource types and deletion) and the `gcloud beta monitoring metrics-scopes`
commands (reference check passed). Removed: the Python sample, the "hundreds" figure, the Metrics Management page,
cardinality and scrape-interval cost tips, the BigQuery export pipeline (the export-metrics page returned 404),
and which metric families are chargeable beyond the page statement.
Method: documentation only; no commands were run.
