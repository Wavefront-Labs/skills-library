---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-reshaping-transformations
name: grafana-reshaping-transformations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, transformations, convert-field-type, extract-fields, format-time, grouping-to-matrix, group-to-nested-table, rows-to-fields, prepare-time-series, time-series-to-table, concatenate-fields, merge-series]
level: practitioner
status: gated
description: "Reshape query results with Grafana transformations: convert, extract, format time, grouping to matrix, rows to fields, series to table, concatenate and merge."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/transform-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reshaping transformations

| Transformation | Turns | Typical use |
|---|---|---|
| **Convert field type** | string -> number/time/boolean/enum (ran: ISO strings to `time`, then Format time) | SQL/JSON fields that arrive as strings; `time` needed for time series |
| **Extract fields** | JSON / key=value / regex in a string field -> new fields (JSON ran: `{"a":1,"b":"x"}` gave columns `a` and `b`; the source column stays unless *Replace all fields*) | Loki log lines or Infinity JSON into columns |
| **Format time** | time field -> formatted string (format `dddd` gave `Thursday`) | "Day of week" columns, grouping by hour |
| **Grouping to matrix** | rows (A, B, value) -> matrix with A as rows, B as columns | pod x container CPU table, service x status-code |
| **Group to nested tables** (picker name) | groups rows with expandable sub-tables (not run here) (gated: unconfirmed, source is paywalled or blocked) | per-service rows expanding to endpoints |
| **Rows to fields** | name/value rows -> one field per row (ran: `cpu,40` and `mem,70` rows became fields `cpu` and `mem`; the `Max` column was not applied as config by default) | gauges whose thresholds come from the query |
| **Prepare time series** | wide <-> long / multi-frame formats | SQL results into multiple series per label |
| **Time series to table** | each series -> a row with a trend (sparkline) cell and reducer (picker name exists in 13.2.4; not run here) (gated: unconfirmed, source is paywalled or blocked) | table with sparklines |
| **Concatenate fields** | all frames' fields into one frame | combine several instant queries into one table |
| **Merge series/tables** | frames joined on shared fields (labels + time) into one table (ran with three instant queries) | one row per pod from several Prometheus instant queries |

## Recipe: one row per pod from three instant queries
Queries (Format: **Table**, Type: **Instant**): A = CPU, B = memory, C = restarts, each `by (namespace, pod)`.
Transformations: **Merge** -> **Organize fields** (hide `Time`, rename `Value #A` -> CPU) -> table panel (ran: columns `service`, `CPU`, `Value #B`, `Value #C`).
"Join by field" (outer, on `pod`) is the alternative when label sets differ slightly.

## Recipe: matrix
Query `sum by (service, code) (increase(http_requests_total[$__range]))` instant/table ->
**Grouping to matrix** (Column: code, Row: service, Cell value: Value) -> table (ran: header `service\code | 200 | 500`, one row per service; cell colouring is a table option not checked here) (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Range queries produce one frame per series; most row-oriented transformations want instant table queries.
- Field names after merges are like `Value #A`; rename with Organize fields or overrides.
- Transformations run in the browser (they appeared only in the rendered panel, never in alert evaluation): large results (10k+ rows) make dashboards slow (the 10k figure is a rule of thumb, not measured).

## Verify
- [ ] Table shows exactly one row per entity and expected columns.
- [ ] Debug view (transformation "Debug" toggle) shows input/output frames as expected.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Playwright-driven Chromium reading rendered panels, Prometheus 3.15.1 and TestData CSV content.
- Ran Extract fields (JSON), Convert field type plus Format time (`dddd`), Rows to fields, Merge, Grouping to matrix; transformation names from the frontend bundle.
- Group to nested tables and Time series to table, and cell colouring, were not run: gated markers, so the skill is `gated`.
