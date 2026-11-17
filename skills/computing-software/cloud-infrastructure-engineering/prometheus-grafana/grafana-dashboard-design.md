---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-dashboard-design
name: grafana-dashboard-design
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, dashboards, dashboard-design, red-method, use-method, template-variables, label-values, chained-variables, units, thresholds, heatmap, annotations, dashboards-as-code, provisioning, grafonnet, rate-interval, dashboard-uid]
level: practitioner
status: docs-checked
description: "Design Grafana dashboards readable mid-incident: overview-to-drilldown hierarchy, RED/USE layout, chained variables, units, heatmaps, annotations, dashboards as code."
sources: ["https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/", "https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/add-template-variables/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/", "https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/heatmap/", "https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/annotate-visualizations/", "https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/configure-standard-options/", "https://grafana.com/docs/grafana/latest/administration/provisioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana dashboard design — answer "is it broken, where, since when" quickly

**Goal:** a small set of dashboards, version-controlled, where an on-call engineer can
go from "something is wrong" to the failing service and component without writing a
query. Queries themselves: `computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-query-patterns`.

## 1. Pick a strategy, then a hierarchy
- USE (Utilization, Saturation, Errors) suits hardware resources such as CPU, memory and network devices. RED (Rate,
  Errors, Duration) suits services and is "a proxy for user experience". The Four Golden Signals (latency, traffic,
  errors, saturation) are RED plus saturation.
- Grafana's guidance is to alert on symptoms rather than causes, so alerting belongs on RED views.
- Hierarchical dashboards with drill-downs to the next level; service dashboards reflect the service hierarchy, e.g. RED
  with one row per service, row order following the data flow.
- Suggested levels: overview (one row per service) -> service dashboard (RED, then dependencies, then USE for its
  resources) -> rarely used component/debug dashboards. Link levels with dashboard links or data links.
- Write the strategy and design guidelines down so dashboards stay consistent.

## 2. Layout
- A dashboard should tell a story or answer a question, progressing from general to specific; if it has no goal,
  question whether it is needed.
- Reduce cognitive load: could someone else tell what each graph shows, and how long would it take?
- Compare like to like: split service dashboards when magnitudes differ so aggregates do not drown important series.
- Use left and right Y-axes for series with different units or ranges. Avoid unnecessary refresh (an hourly-changing
  source does not need a 30 s refresh).
- Document dashboards with a Text panel and panels with a description.

## 3. Variables
```
datasource : type Data source, Prometheus
cluster    : Label values, label cluster, metric up
namespace  : Label values, label namespace, metric kube_pod_info{cluster="$cluster"}
service    : Label values, label service, metric http_requests_total{cluster="$cluster", namespace="$namespace"}
```
- Use query variables instead of one dashboard per node, and make the data source a variable so one dashboard serves
  several clusters and backends.
- Variables whose queries reference other variables are linked; Grafana refreshes a variable when one it depends on
  changes. Custom variables for values that never change reduce the queries sent when chained variables update.
- Prometheus query variable types: Label names, Label values, Metrics, Query result, Series query; the Classic query
  type (`label_values(metric, label)`) is deprecated. Set Refresh to On time range change for variables that depend on
  `$__range`.
- With Multi-value or Include All, use `=~` not `=` in queries (the value becomes a pipe-joined regex).
- Custom all value: by default All expands to every value, which can be very long and slow; a wildcard regex such as
  `.+` can be better. Leave it blank if you want Grafana to format all values into one string.

## 4. Panels that tell the truth
- Set a **unit** on panels (Standard options > Unit); it applies to all fields except time. Normalise where you can,
  e.g. CPU as a percentage rather than a raw count, so 100% means all cores busy.
- Meaningful colour with thresholds (blue good, red bad is Grafana's example), and avoid relying on colour alone.
- Use `$__rate_interval` in `rate()` and `increase()`: it is `max($__interval + scrape_interval, 4 * scrape_interval)`,
  where the scrape interval is the query's Min step or else the data source's Scrape interval. Set the data source
  Scrape interval to match Prometheus; if it is left at 15s while Prometheus scrapes every 60s, `rate()` can return no
  data. In recording rules use a fixed range such as `[5m]` instead.
- Latency distributions: the Heatmap panel shows histograms over time; with pre-bucketed data set Calculate from data
  to No.
- Be careful with stacking: it can mislead and hide data, so Grafana recommends turning it off in most cases. Stack
  only additive values.

## 5. Context overlays
- Every dashboard has a built-in annotation query (the `-- Grafana --` data source) showing annotations stored in
  Grafana, including alert state history; annotations can also come from the HTTP Annotations API (for example from CI
  on deploy) or from annotation queries on any data source.
- Annotations do not follow a dashboard copied with Save As (new dashboard id); an annotation query filtered by tags
  can show them.
- Link panels to other dashboards, logs and traces with panel or data links.

## 6. Dashboards as code
- Grafana's maturity model: keep dashboard JSON in version control, generate dashboards with scripting libraries such as
  grafonnet (Jsonnet) or grafanalib (Python) for consistency, avoid editing in the browser, and experiment on a
  separate Grafana instance.
- Provision from files (`provisioning/dashboards/*.yaml`). A fixed `uid` in the JSON keeps URLs stable and lets
  provisioning update the same dashboard.
- With `allowUiUpdates: false` the UI cannot save a provisioned dashboard. With `true`, UI saves persist to the
  database but the provisioning file overwrites them on its next update. Choose one and tell people.
- Avoid dashboard sprawl: do not copy dashboards with small changes (use variables and URL parameters), do not copy
  tags, prefix temporary dashboards with `TEST:` and delete them, and review dashboards periodically.

## Verify
- [ ] A colleague unfamiliar with the service finds the failing component in a staged incident.
- [ ] Every panel has a unit and a title that says what "good" looks like.
- [ ] All `rate()` panels use `$__rate_interval`; no panel errors with "All" selected.
- [ ] Dashboard is in Git with a fixed `uid` and deploys from CI.

## Checked
Checked 2026-11-08 against the Grafana docs pages in sources (dashboard best practices, add template variables,
Prometheus template variables, heatmap, annotations, standard options, provisioning). Removed as not stated there:
the 20-panel and 3 s load budgets, the 6-12 h default range, the heatmap query and Heatmap query format, the
`label_values()` scan warning, the `changes(app_build_info[5m])` annotation query, data-link URL syntax, p50/p99
stacking example, schema-migration remark, and the Terraform and Foundation SDK mentions.
Method: documentation only; no commands were run.
