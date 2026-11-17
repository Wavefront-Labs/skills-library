---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-bar-chart-pie-chart-and-histogram-panels
name: grafana-bar-chart-pie-chart-and-histogram-panels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [bar-chart-panel, pie-chart-panel, histogram-panel, grafana-visualizations, reduce-transformation]
level: practitioner
status: docs-checked
description: "Shape data for Grafana bar chart, pie chart and histogram panels: required fields, Show/Calculation options, orientation, stacking, bucket settings and pre-bucketed data."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/bar-chart/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/pie-chart/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/histogram/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/query-editor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bar chart, pie chart and histogram panels

## Bar chart
Needs a dataset with one string or time field and at least one numeric field (preferably more than one). The string or time
field labels the bars. With several text or time fields the first is used; change it with the **X Axis** option. Each row
becomes a group of bars, one per numeric field. Use one dataset only: several can give unexpected behaviour. For large
amounts of time-series data the page recommends the time series visualization displayed as bars.

Options: **Orientation** (Auto, Horizontal, Vertical), **Show values** (Auto, Always, Never), **Stacking** (Off, Normal, 100%),
**Group width** (hidden when stacking is on or there is only one numeric field), **Bar width**, **Bar radius**.

For Prometheus, an Instant query returns a single data point per series (the most recent value in the range). The data source
Format option "Table" works only in a Table panel, so for a bar chart keep the default format and shape the fields with
transformations as needed. Illustrative query: `sum by (route) (increase(http_requests_total{job="api"}[1h]))`.

## Pie chart
Displays only one pie regardless of how many datasets, fields or records are queried. By default **Show** is Calculate, which
reduces each series to a single value (the last row's data). Set Show to **All values** to display every value of a series
(then **Limit** caps the number shown); with Calculate pick a **Calculation**. **Fields** selects which fields are used.
Options: pie type **Pie** or **Donut**, slice sorting (Descending default, Ascending, None), labels, legend values **Percent**
and **Value**.

## Histogram panel
Calculates the distribution of values and presents it as a bar chart: each bar is a bucket, height is the count. It accepts
time series and any table with one or more numeric fields. If a data source returns pre-calculated histogram buckets, Grafana
renders the supplied frequencies instead of calculating buckets, and the bucket options become read-only.
Options: **Bucket count** (empty means automatic, 30), **Bucket size** (empty means automatic, about 10 percent of the full
range), **Bucket offset**, **Combine series** (merges all series and fields into one histogram), **Stacking** (Off, Normal, 100%).

## Verify
- [ ] The bar chart data has a string or time field plus numeric fields, and the X Axis option points at the right field.
- [ ] A pie chart showing several rows has Show set to All values.
- [ ] A histogram panel's bucket options match the data (read-only when the query already returns buckets).

## Checked
Checked 2026-11-07. Read the supported-data-formats and options sections of the bar chart, pie chart and histogram pages
(the three pages are 14k-21k characters; I did not read their tooltip, legend, axis, standard-option or override sections beyond the lines
returned by option-name searches) and the Format and Type parts of the Prometheus query editor page. Removed or corrected: the
"Instant query, Format = Table" recipe (the query editor page says Table format works only in a Table panel), `$__range` (not documented on the
pages read), X tick label rotation, the six-slice guideline, "Limit transformation or topk", the claim that the histogram panel only computes buckets from raw values
(it renders supplied buckets when the data source returns them), and the advice to use heatmap or bar gauge for `le` buckets.
The PromQL queries are illustrations and are not verified against any page.
Method: documentation only; no commands were run.
