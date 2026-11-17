---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-data-links-and-field-links
name: grafana-data-links-and-field-links
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [data-links-config, field-data-links, grafana, signal-correlation, dashboard-links, url-variables]
level: practitioner
status: gated
description: "Configure Grafana panel and field data links that carry time range, variables and series labels into Explore, other dashboards, traces and logs."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/configure-data-links/", "https://grafana.com/docs/grafana/latest/dashboards/variables/variable-syntax/", "https://grafana.com/docs/grafana/latest/explore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data links and field links

Data links attach URLs to values in a panel; clicking a point/cell opens them with context interpolated.

## Where
- Panel edit > Data links and actions (field config `links`), per field via overrides.
- Data source level links (Loki derived fields, Tempo trace-to-logs) are separate and configured on the data source.

## Variables you can use
| Variable | Value |
|---|---|
| `${__field.labels.pod}` | label of the clicked series: works on series from a range query in *Time series* format (resolved to `checkout`), but is EMPTY in a table built from *Format: Table* frames (the label is a column there) |
| `${__value.raw}`, `${__value.time}`, `${__value.text}`, `${__value.numeric}` | value of the clicked cell and the row timestamp in epoch ms (`__value.time` was the same on every cell of a row; `__value.numeric` is `NaN` for a string cell) |
| `${__series.name}` | series name as displayed, e.g. `{service="checkout"}` or `Series (A)` for a table frame |
| `${__data.fields.trace_id}` | another field in the same row (tables); `${__data.fields.service}` gave `checkout` |
| `${__url_time_range}` | `from=now-10m&to=now&timezone=browser` on Grafana 13.2.4 (it now includes `timezone`) |
| `${__all_variables}` | all dashboard variables as URL params (`var-job=api&var-svc=checkout&var-svc=search&var-qty=0.99&var-ival=5m&var-tb=hello` appeared) |
| `${service}` / `${service:queryparam}` | dashboard variable; `${svc:queryparam}` gave `var-svc=checkout&var-svc=search` |

## Examples
To another dashboard with the clicked pod:
```
/d/abc123/pod-details?${__url_time_range}&var-namespace=${__field.labels.namespace}&var-pod=${__field.labels.pod}
```
To Explore logs for the clicked series (build in Explore, use "Copy shortened link" or construct the `panes` JSON) (not run here) (gated: unconfirmed, source is paywalled or blocked). A simpler option: add an "internal link" via a correlation or data source setting rather than hand-building Explore URLs.

## Tips
- Tick "Open in new tab" for outbound links so on-call keeps the dashboard (UI option not clicked) (gated: unconfirmed, source is paywalled or blocked).
- In tables, put links on the id column with an override "Fields with name = trace_id" (a default-level link rendered on every cell of the table: `Time`, `service` and `Value` each got the anchor).

## Gotchas
- Labels not present on the series (aggregated away by `sum by`) interpolate as empty; keep needed labels in the query. In tables use `${__data.fields.<column>}` instead of `${__field.labels.<label>}`.
- Explore URL format changed across versions (`left=` to `panes=`); prefer correlations for durable links (version history not re-checked here) (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Clicking a spike opens the target with the same time range and the correct label filled in.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Playwright-driven Chromium reading the `href` of table cell links, Prometheus 3.15.1.
- Built table panels with a field-level data link containing each variable, in Format: Table (instant) and Time series (range) modes, and read the generated URLs.
- Explore URL and the new-tab option were not run: gated markers, so the skill is `gated`.
