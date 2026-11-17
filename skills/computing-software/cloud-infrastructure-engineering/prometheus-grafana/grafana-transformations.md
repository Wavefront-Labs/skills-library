---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-transformations
name: grafana-transformations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, transformations, transform-data, join-by-field, merge, outer-join, organize-fields, filter-by-value, reduce, group-by, add-field-from-calculation, series-to-rows, labels-to-fields, partition-by-values, config-from-query, sort-by, limit, rename-by-regex, table-panel, query-vs-transform, debug-transformations]
level: practitioner
status: gated
description: "Shape query results in Grafana with transformations: join/merge queries, labels to fields, organize/rename, reduce and group by, calculated fields, and when to push the work back into the query."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/transform-data/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/table/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana transformations

**Goal:** turn one or more raw query results into the exact table or series a panel needs,
without hand-editing data and without making the panel unmaintainable.

## 1. Rule zero: do it in the query if you can
Aggregation, filtering, rate math and joins on the same data source belong in PromQL/SQL/LogQL:
they run on the server, cache, and are testable. Transformations are for things queries
cannot do: combining **different data sources**, reshaping for table panels, cosmetic field
work, and per-row calculations across queries. Transformations run in the browser on every
refresh; keep result sets small (thousands of rows, not hundreds of thousands).

## 2. The ones you will actually use
| Transformation | Does | Typical use |
|---|---|---|
| **Labels to fields** | moves series labels into columns (mode: columns or rows; pick a *value field name*) | Prometheus instant query → table with `instance`, `job` columns |
| **Organize fields by name** | hide, reorder, rename columns | every table panel |
| **Join by field** (outer/inner) | SQL-style join of frames on a field (time, `instance`, `pod`) | combine CPU from Prometheus with cost from a SQL source |
| **Merge series/tables** (picker name; JSON id `merge`) | stacks frames with the same schema, matching rows on shared fields | several instant queries into one table |
| **Reduce** | collapse each series to one row/value (last, mean, max…) ; *Series to rows* or *Reduce fields* | summary tables; feed a stat panel one number |
| **Group by** | group rows by a field and aggregate others | top-N tables |
| **Add field from calculation** | binary op or reduce row across fields; *Replace all fields* to keep only the result | ratio between two queries from different sources |
| **Filter data by values** / **Filter fields by name** | drop rows/fields by condition or regex | hide `__name__`, `Time` |
| **Sort by**, **Limit** | ordering and top-N | |
| **Partition by values** | split one frame into many by a field value | one series per `status` from a SQL result |
| **Rename by regex** | bulk rename `(.*)_total` → `$1` | |
| **Config from query results** | use a query's values as thresholds/max/min on another | dynamic gauge max from a quota metric |
| **Prepare time series** / **Format time** | fix "wide" vs "long" shape for time series panels | SQL sources |
| **Convert field type** | string → number/time | CSV/JSON/Infinity sources |

## 3. Canonical recipes
**Prometheus multi-metric table (per pod):**
Queries A..C as *Instant* with *Format: Table*; legend doesn't matter.
1. Merge → one frame with `Time, pod, Value #A, Value #B, Value #C` (ran with `service` in place of `pod`: the Merge plus Organize output was the columns `service`, `CPU`, `Value #B`, `Value #C`).
2. Organize fields: hide `Time`, rename `Value #A` → `CPU`, set order.
3. Field overrides for units/thresholds per column (`Value #B` → `bytes`).
Alternative when label sets differ: Join by field on `pod` (outer). Ran on three instant queries: the result had one `service` column plus a `Time 1`, `Time 2`, `Time 3` and a value column per query, so hide the extra Time columns.

**Cross-datasource ratio:** A = Prometheus `sum(rate(...))`, B = PostgreSQL `SELECT $__time(ts), count` with the same step; Join by field `Time` (outer) → Add field from calculation (`A / B`, replace all fields). No PostgreSQL ran here, so the cross-source join is untested (gated: unconfirmed, source is paywalled or blocked). The calculation step ran on two Prometheus queries: with *Replace all fields* the output kept `Time` and the new field only (the `service` column was dropped), so the rows lose their label.

**Top-N with rest aggregated:** do `topk` in PromQL, then Reduce (last) → Sort by → Limit for the table (not run here) (gated: unconfirmed, source is paywalled or blocked).

**Labels to fields on a range query** (modes *Columns* / *Rows*; option *Value field name*) with `valueLabel: service` on a range query produced a `Time` column and one column per service value (`checkout`, ...), so a time-series panel gets one line per service with clean legends.

## 4. Debugging
- Each transformation has a **Debug** toggle (table icon) showing input/output frames;
  check the frame **count and schema** between steps—most failures are "two frames, not one"
  or a field typed as string.
- Transformations apply in order; Merge/Join must come before Organize. Each card has a *Debug* toggle and a *Disable transformation* (eye) action (labels from Grafana's shipped locale file).
- Field names after Merge are `Value #A`; after labels-to-fields they are the label value or
  the metric name; rename at the end, not in the middle.
- Query options → *Format: Table* and *Type: Instant* on Prometheus avoid 300-point frames
  per series when you only need the latest value.
- A dashboard variable can appear in transformation options (regex filters), but not in all.

## Gotchas
- Transformations are per panel; copying a panel copies them, library panels share them (not run here) (gated: unconfirmed, source is paywalled or blocked).
- Outer join on `Time` across sources with different steps yields nulls (not run, one source only) (gated: unconfirmed, source is paywalled or blocked); *Join by field* modes in the picker are `Inner`, `Outer (tabular)` and `Outer (time series)`.
- "Series to rows" on many series makes huge tables; put `topk`/`limit` in the query.
- Rename by regex runs in the browser, so it is a JavaScript regular expression, not Go RE2: `^(?!name)(.*)_total$` with replace `$1` (a negative lookahead) worked and renamed `requests_total` to `requests` while leaving `name` alone.
- Values transformed client-side are not used by **alert rules** (alerts evaluate queries +
  expressions server-side); replicate logic with Reduce/Math expressions in the alert.

## Verify
- [ ] Debug view shows exactly one frame entering Organize fields with the columns you expect.
- [ ] Panel JSON `transformations` list is short (≤ 5) and each step has a reason you can say aloud.
- [ ] Changing the time range or variables keeps the table shape (no column appears/disappears).

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 (Playwright-driven Chromium reading rendered table panels), Prometheus 3.15.1 and the bundled TestData data source.
- Built dashboards with Merge+Organize, Join by field (outer), Grouping to matrix, Add field from calculation, Labels to fields (range query), Reduce (series to rows), Rename by regex (lookahead), Partition by values, Group by, Extract fields and Rows to fields, and read the rendered tables. Picker names checked in the shipped frontend bundle and `public/locales/en-US/grafana.json`.
- Two recipes (PostgreSQL join, top-N) and two behaviours are gated, so the skill is `gated`.
