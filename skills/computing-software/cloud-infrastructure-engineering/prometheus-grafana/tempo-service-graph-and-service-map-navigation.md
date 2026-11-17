---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tempo-service-graph-and-service-map-navigation
name: tempo-service-graph-and-service-map-navigation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [service-map-navigation, tempo-service-graph-view, service-graph-metrics, tempo, grafana, red-method]
level: practitioner
status: docs-checked
description: "Enable and read the Tempo service graph (node graph) in Grafana and navigate from a service node to RED metrics, traces and logs."
sources: ["https://grafana.com/docs/tempo/latest/metrics-generator/service_graphs/", "https://grafana.com/docs/grafana/latest/datasources/tempo/service-graph/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/node-graph/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tempo service graph and service map navigation

## Prerequisites
- Service graph metrics: Tempo metrics-generator `service-graphs` processor (or the collector `servicegraph` connector) remote-writing `traces_service_graph_request_total`, `traces_service_graph_request_failed_total`, and the `traces_service_graph_request_server_seconds` and `_client_seconds` histograms to Prometheus/Mimir.
- Tempo data source settings > Service graph: select that Prometheus data source.
- Span metrics (for the Service Graph view table): `traces_spanmetrics_calls_total` and `traces_spanmetrics_duration_seconds_bucket`, from the `span-metrics` processor.

## Reading the map (Explore > Tempo > Service Graph)
- Node = service; numbers inside show response time and requests per second; colour shows the mix of green (success), red (fault), yellow (errors) and purple (throttled).
- Clicking a node opens a context menu with links to traces, metrics and related views.
- Investigate a node with TraceQL such as `{ resource.service.name = "<SERVICE_NAME>" && status = error }`.
- The Service Graph view adds a table of rate, error rate and duration; clicking a row opens Prometheus (rate columns) or Tempo (links column) with the span name set.

## Tuning
- The generator inspects spans for parent-child request relationships using OpenTelemetry semantic conventions; edges need both sides to be present.
- For virtual nodes, labels and the full metrics list, see the Tempo service graphs page.
- `dimensions` adds extra labels to the metrics; keep them low-cardinality (the Grafana troubleshooting guide covers high cardinality warnings).

## Gotchas
- Sampling before Tempo thins edges and rates; the graph shows sampled traffic unless metrics are generated before sampling (collector connector).
- Missing edges are usually broken context propagation, not a Tempo issue: check traces for orphan roots.

## Verify
- [ ] Every service in the call path appears with edges; no unexpected "unknown" nodes.
- [ ] Node click opens rate and error panels that match the RED dashboard.

## Checked
- 2026-10-28. Confirmed against the Grafana Tempo data source "Service Graph and Service Graph view" page (metric names, colours, TraceQL example, table behaviour, prerequisites) and the Tempo metrics-generator service graphs page (`dimensions`).
- Removed: the node click menu item names, the `wait` default, `messaging_system`, `virtual_node_peer_attributes`, the "Service structure" view and the cluster/namespace dimension advice.
Method: documentation only; no commands were run.
