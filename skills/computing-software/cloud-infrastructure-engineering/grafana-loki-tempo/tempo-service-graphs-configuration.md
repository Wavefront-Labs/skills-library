---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-service-graphs-configuration
name: tempo-service-graphs-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [service-graphs, tempo, servicegraph-metrics, peer-attributes, virtual-nodes, service-map-metrics]
level: practitioner
status: docs-checked
description: "Configure Tempo service graphs: processor options, peer attributes, virtual nodes, filter policies, and the Grafana serviceMap link to the metrics store."
sources: ["https://grafana.com/docs/tempo/latest/metrics-from-traces/service_graphs/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/service_graphs/enable-service-graphs/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/service_graphs/metrics-queries/", "https://grafana.com/docs/tempo/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: correct edges between services, including databases, queues and uninstrumented callers.

Enable in Tempo by running the metrics-generator and adding `service-graphs` to the tenant's overrides processors:
```yaml
overrides:
  defaults:
    metrics_generator:
      processors: [service-graphs]      # optionally add service-graphs-connection-info
metrics_generator:
  processor:
    service_graphs:
      wait: 10s            # default
      max_items: 10000     # default
      workers: 10          # default
      dimensions: [deployment.environment]
      peer_attributes: [peer.service, db.name, db.system, db.system.name]   # default list
      enable_virtual_node_label: true       # default false
```
Subprocessors: `service-graphs-request` (request and failed counters), `service-graphs-latency` (server/client histograms), `service-graphs-connection-info` (off by default, `traces_service_graph_connection_info` presence gauge). Bare `service-graphs` means request and latency; listing request/latency alongside it is redundant and dropped.

How pairing works: client/server spans (`span.kind` client and server), producer/consumer spans for messaging, or client spans with a `db.namespace`, `db.name`, `db.system` or `db.system.name` attribute for databases. Spans wait in memory until their pair arrives or `wait` passes. Metrics carry `client`, `server`, `connection_type` (unset, `virtual_node`, `messaging_system`, `database`). Main series: `traces_service_graph_request_total`, `_failed_total`, `_request_server_seconds`, `_request_client_seconds`; also `_unpaired_spans_total` and `_dropped_spans_total`. Messaging latency histogram needs `enable_messaging_system_latency_histogram: true`.

Virtual nodes: a root server/consumer span with no client span gets its client name from `peer_attributes` on the server span (otherwise `user`); a client span with no server span uses the first matching peer attribute as the server name. Database node naming: `peer.service`, then `server.address`, then `network.peer.address:port`, then the first matching `database_name_attributes` entry.

Other options: `span_multiplier_key` or `enable_tracestate_span_multiplier` scale counts for sampled traffic; `enable_client_server_prefix` gives `client_`/`server_` labels per extra dimension (doubles those labels); `filter_policies` (same format as span metrics) include or exclude spans, with `exclude` winning.

Grafana: Tempo data source links to the metrics store:
```yaml
- name: Tempo
  type: tempo
  uid: tempo
  jsonData:
    serviceMap:
      datasourceUid: 'prometheus'
```
Query example from the docs: `sum(increase(traces_service_graph_request_server_seconds_count{}[7d])) by (server, client) > 0`.

Gotchas
- The processor must see every span of a trace; if spans spread across instances it cannot pair them reliably.
- `histogram_quantile()` on low-traffic service graph histograms can give misleading values; the docs suggest TraceQL `quantile_over_time()` for latency alerts.
- Extra `dimensions` raise cardinality; the docs describe a dry run.
- Alloy's `otelcol.connector.servicegraph` always names an uninstrumented caller `user`.

## Verify
Query `traces_service_graph_request_total` in the metrics store; expected series have `client` and `server` labels. Filtering metrics: `tempo_metrics_generator_processor_service_graphs_dropped_edges_total`.

## Checked
2026-11-03. Confirmed against the Tempo service graphs overview, enable-service-graphs, metrics-queries and configuration reference pages. Removed: the invented `messaging.system` peer attribute and `curl | grep` verification, the claim that missing `span.kind` produces a counter-name error, and the pre-move source URL.
Method: documentation only; no commands were run.
