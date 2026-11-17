---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-exporters-prw-kafka-elasticsearch
name: otel-collector-exporters-prw-kafka-elasticsearch
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [prometheusremotewrite-exporter-config, kafka-exporter, elasticsearch-exporter, collector-config, otel-collector]
level: advanced
status: docs-checked
description: "Configure key OTel Collector exporters: prometheusremotewrite (labels, target_info, WAL), kafka (encodings, partitioning) and elasticsearch (mapping modes, routing)."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/prometheusremotewriteexporter", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/kafkaexporter", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Collector exporters: prometheusremotewrite, kafka, elasticsearch

## prometheusremotewrite
```yaml
exporters:
  prometheus_remote_write:
    http:
      endpoint: https://mimir.example.com/api/v1/push
      headers: {X-Scope-OrgID: team-a}
    translation_strategy: UnderscoreEscapingWithSuffixes   # default; replaces add_metric_suffixes
    resource_constant_labels:
      included: ["service*", "k8s.namespace.name"]          # replaces resource_to_telemetry_conversion
    target_info: {enabled: true}
    send_metadata: false
    remote_write_queue: {enabled: true, queue_size: 10000, num_consumers: 5}
    wal: {directory: ./prom_rw}                              # queue contents survive restarts
    max_batch_size_bytes: 3000000
```
- A top-level `endpoint` is still accepted for backward compatibility, but the README prefers the `http` block. The type name `prometheusremotewrite` (no underscores) is a deprecated alias.
- TLS is on by default (`insecure: false`). The exporter supports only `snappy` compression.
- Non-cumulative monotonic, histogram and summary metrics are dropped, so convert delta sources to cumulative before this exporter.
- Resource attributes go to a `target_info` metric by default (`target_info.enabled` defaults to true). Copying all resource attributes onto every series (`resource_to_telemetry_conversion`, now deprecated) adds label cardinality; select only the ones you need with `resource_constant_labels.included`, or copy a few with the transform processor.
- It has no `sending_queue`; use `remote_write_queue`. Retries use `retry_on_failure`; the data in the queue is lost on restart unless `wal` is set.
- More than one consumer (the `EnableMultipleWorkers` feature gate) needs a backend that accepts out-of-order samples; for Prometheus that is `tsdb.out_of_order_time_window`.

## kafka
```yaml
exporters:
  kafka:
    brokers: [kafka-0:9092, kafka-1:9092]
    protocol_version: 2.1.0
    traces: {topic: otlp_spans, encoding: otlp_proto}
    logs:   {topic: otlp_logs,  encoding: otlp_proto}
    partition_traces_by_id: true
    producer: {compression: zstd, max_message_bytes: 1000000, required_acks: 1}
    tls: {insecure: false}
    auth: {sasl: {username: otel, password: "${env:KAFKA_PASSWORD}", mechanism: SCRAM-SHA-512}}
```
- Defaults: `brokers` is localhost:9092, `protocol_version` 2.1.0, topics `otlp_logs`, `otlp_metrics`, `otlp_spans`, encoding `otlp_proto`, producer `compression` none, `required_acks` 1, `max_message_bytes` 1000000.
- `partition_traces_by_id` (default false) uses the trace ID as the message key. `partition_logs_by_trace_id` and `partition_logs_by_resource_attributes` are mutually exclusive.
- SASL mechanisms: SCRAM-SHA-256, SCRAM-SHA-512, AWS_MSK_IAM_OAUTHBEARER, OAUTHBEARER, PLAIN. Compression options: none, gzip, snappy, lz4, zstd.
- `raw` encoding sends a byte-array log body as is (otherwise JSON) and discards resource and record attributes.
- To put several signals on one topic, enable `signal_header` first (it adds an `otelcol.signal` header).

## elasticsearch
```yaml
exporters:
  elasticsearch:
    endpoint: https://es.example.com:9200
    auth: {authenticator: basicauth}
    sending_queue:
      batch: {flush_timeout: 10s, max_size: 5000000, sizer: bytes}
    retry: {enabled: true, max_retries: 2}
```
- Mapping modes: `otel`, `ecs`, `raw`, `bodymap`, `none`. `mapping::mode` is deprecated: set the scope attribute `elastic.mapping.mode` (for example with a transform processor) or the client metadata key `X-Elastic-Mapping-Mode`. `otel` is the default and recommended mode; `ecs` suits existing ECS dashboards.
- `otel` and `ecs` need Elasticsearch 8.12 or above; `otel` works best on 8.16 or above.
- Routing order: static `logs_index` / `metrics_index` / `traces_index` if non-empty, then the `elasticsearch.index` attribute, then a data stream built from `data_stream.type`, `data_stream.dataset` and `data_stream.namespace`. `logs_index` should be empty unless all logs go to one index.
- The old `flush` and `num_workers` settings were removed; `flush::interval` is now `sending_queue::batch::flush_timeout`. Retry defaults: enabled, `max_retries` 2, `retry_on_status` [429].

## Gotchas
- Exporter failures show in the Collector's own exporter metrics; keep the queue and retry settings on each exporter.

## Checked
Date: 2026-11-09. Confirmed against the README files of the prometheusremotewrite, kafka and elasticsearch exporters in opentelemetry-collector-contrib: PRW options, deprecations, drop rule, WAL and queue behaviour; Kafka defaults, auth mechanisms, compression options, partition flags and raw encoding; Elasticsearch auth shortcuts, mapping modes, version needs, routing order, removed settings and retry defaults. Removed: sigv4auth and Amazon Managed Prometheus note, deltatocumulative processor and OTLP-direct backend claims, the "400 out of order" explanation, the kafka consumer receiver note, the logs_index data stream name pattern and a metric name in the gotchas.
Method: docs-checked 2026-11-09 against the three exporter README files read in full or by targeted search.
