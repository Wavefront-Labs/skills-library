---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-variables-links-and-time-controls
name: grafana-variables-links-and-time-controls
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, template-variables, query-variable, custom-variable, datasource-variable, interval-variable, adhoc-filters, dashboard-links, panel-links, url-variables, time-range-controls, relative-time-override, time-shift]
level: practitioner
status: gated
description: "Build navigable Grafana dashboards: each variable type, chained queries, URL variable passing in dashboard/panel/data links, and per-panel relative time and time shift."
sources: ["https://grafana.com/docs/grafana/latest/dashboards/variables/add-template-variables/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-data-links/", "https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/#query-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables, links and time controls

## Variable types
| Type | Example | Notes |
|---|---|---|
| Query | `label_values(kube_pod_info{cluster="$cluster"}, namespace)` | chain by referencing earlier variables (ran: `label_values(http_requests_total{job="$job"}, service)` listed the services of the chosen job); refresh `2` (on time range change) in the JSON |
| Custom | `p50 : 0.5, p99 : 0.99` | `text : value` pairs (with `var-qty=0.99` the panel title showed `p99`) |
| Text box | free text, e.g. a trace ID filter | |
| Constant | hidden value (not run) | |
| Data source | type `prometheus`, regex `/prod-.*/` | lets one dashboard serve every cluster; reference as `${datasource}` in panels (not run) |
| Interval | `1m,5m,1h` with Auto option (ran: `var-ival=5m` interpolated as `5m`) | `$__auto_interval_<name>` (not run) |
| Ad hoc filters | adds `key=value` matchers to every query of the data source (the picker shows "Filters" in 13.2.4) | Prometheus/Loki only (not run) |
Prometheus query helpers: `label_values(metric, label)` ran; `label_names()`, `metrics(regex)`, `query_result(topk(5, ...))` (with a regex to extract a value) were not run (gated: unconfirmed, source is paywalled or blocked).

Multi-value + Include All: use `=~"$namespace"`; set a custom All value `.*` (`allValue` in the JSON) to avoid giant regex alternations. With two values selected `${svc}` printed `checkout + search` in a title, `${svc:regex}` gave `(checkout|search)`, `${svc:pipe}` gave `checkout|search`, and the query `service=~"$svc"` returned both services.

## Links
- **Dashboard links** (settings -> Links): by tag or URL, with "Include current time range" and "Include current
  template variable values" -> carries `var-*` and `from/to` (those two option labels exist in the 13.2.4 frontend; the link itself was not clicked) (gated: unconfirmed, source is paywalled or blocked).
- **Data links** on fields (panel -> Data links): `/d/pod-detail?var-namespace=${__field.labels.namespace}&var-pod=${__field.labels.pod}&${__url_time_range}` (use `${__data.fields.pod}` in tables built from table-format frames: `__field.labels` is empty there).
  Useful tokens: `${__value.raw}`, `${__series.name}`, `${__field.labels.X}`, `${__data.fields.X}`,
  `${__all_variables}`, `${__url_time_range}` (all resolved; see the data links skill).
- URL format for variables: `?var-cluster=prod&var-namespace=a&var-namespace=b` (repeat for multi; `var-svc=checkout&var-svc=search` selected both values).

## Time controls
- Dashboard: time picker, refresh, "Now delay" (hide incomplete recent data), timezone, week start.
- Per panel (Query options): **Relative time** `now-24h` (panel ignores picker for a fixed range: "last 24h
  errors" next to a zoomable graph), **Time shift** `1w` (same panel a week ago; combine with a second query
  for overlays), Hide time info.
- Globals `$__range` (ran inside `increase(...[$__range])`), `$__interval`, `$__rate_interval`, `$__from/$__to` (the last four were not run here) (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Changing `cluster` updates all dependent variables and panels.
- [ ] Clicking a pod in a table opens the detail dashboard with the same time range and variables.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Playwright-driven Chromium, Prometheus 3.15.1.
- Dashboard with query (chained, multi, include All, custom All value), custom, interval and textbox variables opened with `var-*` URL parameters: panel titles and queries showed the interpolations above.
- Items marked gated were not run, so the skill is `gated`.
