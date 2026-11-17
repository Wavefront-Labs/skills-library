---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-components-and-reliability
name: otel-collector-components-and-reliability
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-config, prometheus-receiver-config, hostmetrics-receiver, kafka-receiver, batch-processor-tuning, memory-limiter-tuning, spanmetrics-connector-config, servicegraph-connector, routing-connector, count-connector, sending-queue-config, persistent-queue, file-storage-extension, basicauth-extension, oauth2client-extension, bearertokenauth]
level: advanced
status: docs-checked
description: "Assemble a reliable OTel Collector pipeline: prometheus/hostmetrics/kafka receivers, memory_limiter and batch tuning, connectors, auth extensions, and persistent sending queues."
sources: ["https://opentelemetry.io/docs/collector/configuration/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Collector components and reliability

```yaml
extensions:
  file_storage: {directory: /var/lib/otelcol/queue}
  oauth2client: {client_id: otel, client_secret: "${env:OAUTH_SECRET}", token_url: https://idp/oauth2/token}
  bearertokenauth/in: {token: "${env:INBOUND_TOKEN}"}     # auth for incoming OTLP
receivers:
  otlp: {protocols: {grpc: {endpoint: 0.0.0.0:4317, auth: {authenticator: bearertokenauth/in}}, http: {endpoint: 0.0.0.0:4318}}}
  prometheus:
    config:
      scrape_configs:
        - job_name: app
          scrape_interval: 30s
          kubernetes_sd_configs: [{role: pod}]
          relabel_configs: [{source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape], regex: "true", action: keep}]
  hostmetrics: {collection_interval: 30s, scrapers: {cpu: {}, memory: {}, filesystem: {}, network: {}, load: {}}}
  kafka: {brokers: [kafka:9092], topics: [otlp_spans], encoding: otlp_proto, group_id: otel-gateway}
processors:
  memory_limiter: {check_interval: 1s, limit_percentage: 80, spike_limit_percentage: 20}   # FIRST in every pipeline
  batch: {send_batch_size: 8192, send_batch_max_size: 10000, timeout: 5s}                 # LAST before exporters
connectors:
  spanmetrics: {histogram: {explicit: {buckets: [50ms, 100ms, 300ms, 1s, 3s]}}, dimensions: [{name: http.route}]}
  servicegraph: {latency_histogram_buckets: [100ms, 1s], store: {ttl: 2s, max_items: 10000}}
  count: {}                                                  # counts spans/logs as metrics
  routing: {table: [{condition: 'resource.attributes["tenant"] == "a"', pipelines: [traces/a]}], default_pipelines: [traces/default]}
exporters:
  otlp/tempo:
    endpoint: tempo-distributor:4317
    sending_queue: {enabled: true, num_consumers: 10, queue_size: 5000, storage: file_storage}   # survives restarts
    retry_on_failure: {enabled: true, initial_interval: 5s, max_interval: 30s, max_elapsed_time: 300s}
  otlphttp/vendor: {endpoint: https://otlp.vendor.example, auth: {authenticator: oauth2client}}
service:
  extensions: [file_storage, oauth2client, bearertokenauth/in]
  pipelines:
    traces: {receivers: [otlp, kafka], processors: [memory_limiter, batch], exporters: [otlp/tempo, spanmetrics, servicegraph]}
    metrics: {receivers: [prometheus, hostmetrics, spanmetrics, servicegraph], processors: [memory_limiter, batch], exporters: [otlphttp/vendor]}
```

## Reliability rules
- `memory_limiter` first: refuses data (receivers return retryable errors) before OOM. Set GOMEMLIMIT ~80 % too.
- Persistent queue (`storage: file_storage`) needs a directory that survives restarts (a persistent volume); the in-memory queue is lost on restart.
- `max_elapsed_time` bounds retries; after that data is dropped (`otelcol_exporter_send_failed_*`).
- Prometheus receiver in multiple replicas scrapes everything N times: use the target allocator or one replica.
- Connectors are both exporter (in one pipeline) and receiver (in another).

## Verify
- [ ] `otelcol validate --config=config.yaml` passes.
- [ ] `otelcol_exporter_queue_size` well below capacity; `otelcol_processor_refused_*` zero at normal load.

## Checked
- 2026-10-28. Checked against the collector-contrib READMEs for kafkareceiver, routingconnector, servicegraphconnector, spanmetricsconnector, countconnector, bearertokenauthextension, hostmetricsreceiver and filestorage, the collector exporterhelper and memorylimiterprocessor READMEs, and the Collector scaling and internal-telemetry pages (main branch, 2026-10).
- Confirmed: `topics`, `group_id`, `encoding` (default otlp_proto), routing `table.condition/pipelines`, `default_pipelines`, servicegraph `store.ttl/max_items` and `latency_histogram_buckets`, `spike_limit_percentage`, `check_interval`, `num_consumers`, `queue_size`, `max_elapsed_time`, persistent-queue `storage`, `otelcol_processor_refused_*`, Target Allocator for Prometheus receiver scaling.
- Fixed: Kafka receiver `topic` replaced by `topics` list; routing `statement: route() where` replaced by `condition` (the README prefers it); bearertokenauth `filename` replaced by `token` (the only option in the fetched README).
Method: documentation only; no commands were run.
