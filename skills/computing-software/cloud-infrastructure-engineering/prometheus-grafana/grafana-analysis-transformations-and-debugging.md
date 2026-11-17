---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-analysis-transformations-and-debugging
name: grafana-analysis-transformations-and-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, transformations, regression-analysis, histogram-transformation, transformation-order, debug-transformation-output, add-field-from-calculation, filter-data-by-values]
level: practitioner
status: gated
description: "Use Grafana's analytical transformations (regression analysis, histogram, add field from calculation, filter by value) and debug transformation chains step by step."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/transform-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysis transformations and debugging chains

## Analytical transformations
- **Trendline** (named "Regression analysis" in older versions; id `regression`): fits a linear or polynomial regression (model types `Linear`, `Polynomial` with a Degree option up to `Decic`) to an X/Y field pair and outputs a predicted series; the option to extend beyond the data is `Predicted points`. Quick capacity trend on a dashboard
  without PromQL `predict_linear` (which is better for alerts).
- **Histogram**: buckets a numeric field's values into a histogram frame (picker name exists; its options were not run here) (gated: unconfirmed, source is paywalled or blocked).
  Use for distributions of per-entity values (pod memory across the fleet), not for Prometheus histogram
  metrics (use the heatmap/histogram panel with bucket data).
- **Add field from calculation**: modes `Reduce row`, `Binary operation` (ran: `Value #C / Value #B` gave 0.1), `Unary operation`, `Row index`, with `Cumulative functions` and `Window functions` options (mode and option names from the 13.2.4 locale file; only Binary operation was run).
- **Filter data by values**: drop rows by condition (`Include` / `Exclude`, `Match all` / `Match any`); **Filter fields by name** hides fields; **Limit** keeps first N rows; **Sort by** orders rows (not run here; names from the picker) (gated: unconfirmed, source is paywalled or blocked).
- **Reduce**: series -> rows of calculations (Last, Max, Mean) for summary tables.

## Ordering matters
Transformations run top to bottom, each on the previous output. Common correct order:
1. Shape (Merge / Join / Prepare time series)
2. Compute (Add field from calculation)
3. Filter (Filter data by values, Limit)
4. Present (Organize fields, Sort by, Convert field type for display)
Filtering before a join drops rows you later need; any step after Organize fields must reference renamed
fields by their new names.

## Debugging
- Each transformation card has a **Debug** action showing input and output frames (title `Debug transformation`).
- Panel inspector -> **Data** tab: "Apply panel transformations" on/off (label in the locale file) and a data frame selector; download CSV.
- Inspector -> **Query** tab shows raw responses before transformations.
- Use *Disable transformation* on individual steps to bisect a broken chain.

## Verify
- [ ] Debug view of the final step shows the frame structure the visualization expects.
- [ ] Removing any one step changes the output (no dead steps left in the chain).

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 and its shipped locale file and frontend bundle (`transformers.regression.name.trendline`).
- Ran Add field from calculation (binary) and Reduce in a rendered panel; renamed items confirmed in the bundle (Trendline, Group to nested tables).
- Filter and Histogram options were not run: gated markers, so the skill is `gated`.
