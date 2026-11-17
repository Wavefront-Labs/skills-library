---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-specialty-panels
name: grafana-specialty-panels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, geomap-layers, canvas-panel, flame-graph-panel, node-graph-panel, xy-chart, trend-panel, candlestick, logs-panel-options, traces-panel-options]
level: practitioner
status: draft
description: "Use Grafana's specialty visualizations: geomap layers, canvas, flame graph, node graph data frames, XY chart, trend, candlestick, and logs/traces panel options."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Specialty panels

## Geomap
Layers: Markers (lat/long fields, or lookup by country/US state code or geohash), Heatmap, GeoJSON, Route,
Photos, plus base layers (OpenStreetMap, CARTO, ArcGIS, XYZ tiles). Location mode "Auto" detects `latitude`/
`longitude` fields. Size/colour markers by a field (e.g. requests per region from `sum by (region)` joined with
a region-to-coordinates CSV via a second query + Join by field).

## Canvas
Free-form layout of elements (metric value, text, icon, rectangle, server, button) bound to fields, with
connections between elements whose colour/width can be data-driven. Use for system diagrams with live status;
keep it small and maintained, as it's hand-placed.

## Flame graph
Expects profile data frames (`level`, `value`, `self`, `label`) from Pyroscope/Grafana profiles or Tempo
traces-to-profiles. Options: top table + flame graph, search, sandwich view, colour by package.

## Node graph
Two frames: **nodes** (`id`, `title`, `subtitle`, `mainstat`, `secondarystat`, `arc__*` fields summing to 1
for the ring) and **edges** (`id`, `source`, `target`, `mainstat`). Tempo service graphs and the Prometheus
service-graph metrics produce these; you can build them from SQL/Infinity too.

## XY chart, Trend, Candlestick
- XY chart: any numeric X vs Y (latency vs throughput per instance, from instant queries joined by instance);
  series mapping Auto or Manual.
- Trend: like time series but X is any increasing numeric field (e.g. load-test RPS on X).
- Candlestick: open/high/low/close (+ volume) fields; maps automatically when named so; also useful for
  min/max/first/last of any metric per interval.

## Logs and traces panels
- Logs: show time, unique labels, common labels, wrap lines, prettify JSON, dedup (exact/numbers/signature),
  order newest first; data links from derived fields appear on expand.
- Traces: single trace view by trace ID (`${traceId}` variable) for embedding in dashboards; span filters.

## Verify
- [ ] Node graph renders with node and edge frames correctly named (inspect -> Data).
- [ ] Geomap markers land in the right places for a known region.
