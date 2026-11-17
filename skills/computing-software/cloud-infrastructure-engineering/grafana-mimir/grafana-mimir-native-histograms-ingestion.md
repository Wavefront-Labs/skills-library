---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-native-histograms-ingestion
name: grafana-mimir-native-histograms-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [native-histograms, remote-write, ingestion, bucket-limit, otel]
level: practitioner
status: docs-checked
description: "Shows how to enable Prometheus native histogram ingestion in Mimir globally or per tenant and limit buckets per sample."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-native-histograms-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native histogram ingestion

Native histograms arrive over the Prometheus remote write endpoint.

## Global

- Ingesters: `-ingester.native-histograms-ingestion-enabled=true`.
- Distributors: `-validation.max-native-histogram-buckets` to cap buckets per sample. The recommended value is `160`, which is the OpenTelemetry SDK default for exponential histograms (a similar concept).

Samples exceeding the limit are scaled down at ingestion: resolution is reduced and buckets merged until under the limit or at minimum resolution. Set `-validation.reduce-native-histogram-over-max-buckets=false` to drop such samples instead.

## Per tenant

Runtime overrides:

```yaml
overrides:
  tenant1:
    native_histograms_ingestion_enabled: true
    max_native_histogram_buckets: 160
```

## Querying with query sharding

To query native histograms together with query sharding, keep `-query-frontend.query-result-response-format` at its default, `protobuf`.

Sending from Grafana Alloy or Prometheus is covered in the Mimir send docs for native histograms.

## Checked

Confirmed the remote write ingestion path, the global flags, the 160 bucket recommendation and its OpenTelemetry basis, the scale-down behaviour, the per-tenant runtime values, and the query sharding note on protobuf. Added the drop-instead option from the page.

Method: docs-checked 2026-11-09 against the raw grafana/mimir docs page configure-native-histograms-ingestion.md, read in full.
