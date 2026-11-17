---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-state-timeline-and-status-history
name: grafana-state-timeline-and-status-history
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [status-history-panel, state-timeline-config, state-timeline, grafana-visualizations, value-mapping-rules]
level: practitioner
status: docs-checked
description: "Show discrete states over time with Grafana state timeline and status history panels: data format, value mappings, thresholds, merging, null handling and legends."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/state-timeline/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/status-history/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-value-mappings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State timeline and status history

- **State timeline**: shows state changes over time as bars or bands called state regions, whose length shows how long a state lasted. Each state ends when the next begins or at a null value.
- **Status history**: shows periodic states over time; each field or series is a horizontal row of boxes. Unlike a state timeline, a status history does not merge consecutive values.

## Data
Both work best with table-shaped data containing timestamps (a state-change time, optionally plus an end time), an entity name or identifier, and a state value, which can be string, numerical or boolean. Null or empty values are drawn as gaps. If query results are not in that shape, especially time series data, apply transformations. A state timeline can also take time series data: add thresholds, which turn the series into discrete coloured state regions.

## Configuration
- Value mappings (supported by both panels): Value (specific values), Range (numerical ranges), Regex (regular expressions) and Special (Null, NaN, true/false), each to display text and an optional colour. For example, map 0 to Down in red and 1 to Up in green. Value mappings bypass unit formatting. In Regex mappings `.` does not match newlines by default; use `[\s\S]` for multiline strings.
- Thresholds (Absolute or Percentage mode) with Color scheme set to From thresholds for numeric levels.
- The legend shows value mappings when Color scheme is Single color or Classic palette, and threshold brackets when it is From thresholds.
- State timeline options: Merge equal consecutive values, Show values (Auto, Always, Never; Auto renders values when there is space), Align values, Row height (1 fills the row, lower values leave more space), Page size, Line width, Fill opacity, Connect null values (Never, Always or Threshold) and Disconnect values (Never or Threshold).
- Status history options: Show values (Auto, Always, Never), Row height (1 makes the largest boxes), Column width (1 makes the widest boxes), Page size, Line width, Fill opacity.

## Gotchas
- With many series, use Page size to limit how many are visible at once.
- Use Connect null values with a Threshold to bridge gaps up to a known size and leave larger gaps open.
- Panels with value mappings display a summary in the Value mappings section of the editor.

## Checked
Date: 2026-11-07.
Read in full: the State timeline page, the Configure value mappings page, and the Status history page through its tooltip options (its remaining legend, tooltip and standard-options sections repeat the State timeline page's wording).
Removed because no cited page confirms them: the four PromQL examples (`up`, `probe_success`, `kube_pod_status_phase`, `ALERTS`), the "Row height ~0.8" setting, the "Insert nulls threshold" option (the panel calls it Disconnect values), column width being driven by Max data points, the aligned-timestamps requirement, the heavy-rendering and Min interval advice, the claim that Prometheus values always need mappings, and the invented Verify checklist.
Method: documentation only; no commands were run.
