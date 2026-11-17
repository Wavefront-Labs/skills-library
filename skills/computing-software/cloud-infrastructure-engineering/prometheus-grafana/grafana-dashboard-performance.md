---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-dashboard-performance
name: grafana-dashboard-performance
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [dashboard-performance, max-data-points, grafana-dashboards, query-optimization, recording-rules, min-interval]
level: practitioner
status: docs-checked
description: "Speed up slow Grafana dashboards: fewer and cheaper queries, max data points and min interval, shared queries, variable refresh, recording rules and the panel inspector."
sources: ["https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/query-transform-data/", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/", "https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/add-template-variables/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/", "https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/panel-inspector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana dashboard performance

## Measure first
- Panel inspector, Stats tab: shows how long the query takes, how many queries are sent and the number of rows returned. The Query tab shows the request and response.
- Browser developer tools: count the data requests made on load.

## Techniques
1. Fewer queries: one query returning several series instead of several panels with one each. The special `-- Dashboard --` data source reuses another panel's result set from the same dashboard.
2. Max data points (panel Query options) defaults to the panel's pixel width. Set it to a fixed lower value to request fewer points. Min interval corresponds to the min step in Prometheus: set it to the scrape interval to avoid sub-scrape steps.
3. For Prometheus rate queries use `$__rate_interval`, and set the data source Scrape interval (default 15s) to match your real `scrape_interval`; otherwise `rate()` windows can be too small and return no data.
4. Recording rules for expensive expressions over long ranges (histogram_quantile across many series, long-window SLIs).
5. Regex-heavy variables: with Include All option, set a Custom all value such as `.+` instead of letting Grafana expand every value into a long regex.
6. Variable Refresh: On dashboard load queries the data source on load only. On time range change also re-queries when the range changes; use it only when the variable query depends on the time range.
7. Prometheus data source settings: Query timeout (default 60s), Cache level (Low, Medium, High or None; higher is recommended for high-cardinality data sources) and Incremental querying (beta), which fetches only new data and re-requests an overlap window (default 10m).
8. Avoid unnecessary refreshing: the best-practices page advises not setting a fast dashboard refresh when the data changes slowly.

## Gotchas
- Changing the data source Scrape interval changes `$__rate_interval` results across every dashboard that uses it.

## Verify
- [ ] Query count and slowest query time are known from the Stats tab, and the default time range loads acceptably.

## Checked
Date: 2026-10-28. Confirmed against the Grafana query options, Prometheus data source configure, Prometheus template variables, add-template-variables, panel inspector and dashboard best-practices pages: Max data points default, Min interval = Prometheus min step, `-- Dashboard --` data source, `$__rate_interval` behaviour and Scrape interval default of 15s, Include All option and Custom all value, variable Refresh options, Query timeout default 60s, Cache level options, incremental querying (beta) with 10m default overlap, Stats tab contents. Removed unconfirmed claims: collapsed rows not querying, the `/api/ds/query` path, example figures (500 points, 1m refresh, 1-6h range, 3s load), table instant-query advice, and the repeated-panel query-count claim.
Method: documentation only; no commands were run.
