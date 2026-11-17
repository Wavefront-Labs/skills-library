---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-monitoring-metrics-dashboards-uptime
name: cloud-monitoring-metrics-dashboards-uptime
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-monitoring, monitoring, dashboards, uptime-checks, metrics-scopes, metrics-scope, custom-metrics, mql, promql, metrics-explorer, dashboards-as-code, synthetic-monitors, monitoring-api, metric-descriptors, opentelemetry-metrics, log-based-metrics, groups, monitoring-iam]
level: practitioner
status: docs-checked
description: "Cloud Monitoring platform: metrics scopes across projects, OpenTelemetry custom metrics, PromQL, dashboards as code, and uptime checks."
sources: ["https://cloud.google.com/monitoring/docs/monitoring-overview", "https://cloud.google.com/monitoring/settings/multiple-projects", "https://cloud.google.com/monitoring/custom-metrics", "https://cloud.google.com/monitoring/dashboards/api-dashboard", "https://cloud.google.com/monitoring/uptime-checks", "https://cloud.google.com/monitoring/promql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Monitoring: metrics, dashboards and uptime checks

**Goal:** one place to query every project's metrics, dashboards that live in git, and
external probes that tell you the site is down before customers do.

## 1. Metrics scopes (multi-project first)
- Each project has a **metrics scope**; a *scoping project* can add other projects as monitored projects so dashboards and alerts there see all of them. Configuring this needs Monitoring Admin (`roles/monitoring.admin`) on the scoping project and on each project you add or remove; with VPC Service Controls, the added project must be in the same perimeter as the scoping project or bridged to it.
- Pattern: a scoping project per environment or per team; alert policies and dashboards live in the scoping project.
- Managed Service for Prometheus data follows the same metrics scope, so PromQL in the scoping project can query all clusters in it.

## 2. Metric model and custom metrics
A time series is identified by `metric.type`, `metric.labels`, and a monitored resource (`resource.type` plus `resource.labels`); Metrics Explorer shows the full metric name.
- For user-defined metrics the docs recommend **OpenTelemetry** (Prometheus or the Cloud Monitoring API directly also work). The Ops Agent OTLP receiver covers Compute Engine; on Cloud Run use the OpenTelemetry Collector as a sidecar.
- Use **log-based metrics** for things that exist only in logs (see `cloud-logging-queries-and-log-based-metrics`).
- Keep label cardinality low (user IDs are not labels).
- Monitor ingestion on the Metrics Management page. To keep data beyond the retention period, copy it to Cloud Storage or BigQuery; limits and retention are on the Quotas and limits page.

## 3. Query
PromQL works over Cloud Monitoring metrics: the metric name maps `kubernetes.io/container/cpu/limit_cores` to `kubernetes_io:container_cpu_limit_cores`, so the first `/` becomes `:` and other `.` and `/` become `_`.
```promql
sum by (cluster) (kubernetes_io:container_cpu_limit_cores)
```
(Check the metric name in Metrics Explorer before alerting on it.) For automation use the Cloud Monitoring API through the client libraries.

## 4. Dashboards as code
```bash
gcloud monitoring dashboards describe <DASHBOARD_ID> --format=json > dashboard.json
gcloud monitoring dashboards create --config-from-file=dashboard.json
```
A dashboard JSON uses a layout such as `mosaicLayout` with `tiles`, optional `dashboardFilters`, and widgets such as `alertChart` (a single-condition policy summary: line chart, threshold and open alert count). Build in the console, export, remove server-assigned fields before re-creating, and commit the JSON.

## 5. Uptime checks
```bash
gcloud monitoring uptime create web-home --resource-type=uptime-url \
  --resource-labels=host=www.example.com,project_id=<P> \
  --protocol=https --path=/healthz --port=443 --validate-ssl=true
```
- `uptime create` also takes `--period`, `--timeout`, `--regions`, `--status-codes`, `--matcher-type` and `--matcher-content`; identify at least three checkers (each USA_* region has one checker, and `USA` includes three).
- If the target is behind a firewall, allow the uptime-check server IP addresses (`gcloud monitoring uptime list-ips`).
- Targets on a private network need **private uptime checks**; the command also supports `--synthetic-target` for synthetic monitors (see its reference page).
- Pair a check with an alerting policy so failures notify someone.

## Gotchas
- Alerting policies and dashboards in a workload project only see that project's metrics; forgetting the metrics scope is a common cause of "metric not found".
- PromQL over Cloud Monitoring metrics uses the underscore/colon names above, not the original metric paths.

## Verify
- [ ] Metrics Explorer in the scoping project lists resources from the monitored projects.
- [ ] `dashboards create` from the committed JSON reproduces the dashboard.
- [ ] The uptime check passes from every selected region, and returning an error from `/healthz` makes it fail and the alert fire.

## Checked

2026-10-27. Confirmed in the Monitoring overview, multiple-projects (metrics scope), custom metrics, dashboards API, uptime checks and PromQL pages and the `gcloud monitoring uptime create`, `uptime list-ips` and `dashboards create/describe` reference pages: metrics scope and scoping project, Monitoring Admin requirement and VPC-SC perimeter validation, OpenTelemetry recommendation and OTLP routes, PromQL name mapping, `mosaicLayout`, `tiles`, `dashboardFilters` and `alertChart`, uptime flags (`--resource-type=uptime-url`, `--resource-labels`, `--protocol`, `--path`, `--port`, `--validate-ssl`, `--period`, `--timeout`, `--regions`, `--status-codes`, `--matcher-type`, `--matcher-content`, `--synthetic-target`), at least three checkers, firewall allowlisting of checker IPs, private uptime checks. Removed: `gcloud monitoring metrics-scopes create` (no reference page), the 375-project limit, ingestion delay and retention figures (24 months, 6 weeks), billing metric names and cost claims, IAM role list, the MQL and run_googleapis_com query examples, `timeSeries` method names, Terraform and sample-repository claims, synthetic monitor and Service Directory details (the synthetic monitors page returned 404), Cloud Armor/IAP gotchas, scope-deletion gotcha. Read end to end.

Method: documentation only; no commands were run.
