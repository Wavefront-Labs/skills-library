---
id: computing-software.cloud-infrastructure-engineering.observability.otel-metrics-instruments-views-and-temporality
name: otel-metrics-instruments-views-and-temporality
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otel-metrics, instrument-selection, counter-vs-updowncounter, view-configuration, drop-attributes-view, histogram-buckets-view, temporality-selection, delta-vs-cumulative, metric-reader, periodic-reader, prometheus-metric-reader, metric-cardinality-limit, overflow-attribute, exponential-histogram-config, base2-histogram, otel-exemplars, exemplar-filter]
level: advanced
status: docs-checked
description: "Choose OTel metric instruments, shape output with views (attributes, buckets, exponential), pick delta vs cumulative, readers, cardinality limits, exemplars."
sources: ["https://opentelemetry.io/docs/specs/otel/metrics/sdk/", "https://opentelemetry.io/docs/specs/otel/metrics/supplementary-guidelines/", "https://opentelemetry.io/docs/specs/otel/metrics/data-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTel metrics: instruments, views, temporality

## Instrument choice
| Measures | Instrument |
|---|---|
| Monotonic count you add to (requests, bytes) | Counter |
| Value that goes up and down by deltas (queue items, active requests) | UpDownCounter |
| Value you observe from elsewhere at collection time | Observable Counter / UpDownCounter / Gauge (callbacks) |
| Current value you set synchronously (temperature, config value) | Gauge (sync, newer SDKs) |
| Distribution (latency, payload size) | Histogram |
Per the API spec, a Gauge records non-additive values; for additive values (such as heap size summed across processes) use an UpDownCounter.

## Views (Java shown)
```java
SdkMeterProvider.builder()
  .registerView(InstrumentSelector.builder().setName("http.server.request.duration").build(),
      View.builder()
        .setAggregation(Aggregation.explicitBucketHistogram(List.of(0.05, 0.1, 0.3, 0.5, 1.0, 2.5, 5.0)))
        .setAttributeFilter(Set.of("http.request.method", "http.route", "http.response.status_code"))   // drop others
        .build())
  .registerView(InstrumentSelector.builder().setType(InstrumentType.HISTOGRAM).build(),
      View.builder().setAggregation(Aggregation.base2ExponentialBucketHistogram(160, 20)).build())     // max buckets, max scale
  .registerView(InstrumentSelector.builder().setMeterName("io.noisy.lib").build(),
      View.builder().setAggregation(Aggregation.drop()).build())
```
`base2ExponentialBucketHistogram(maxBuckets, maxScale)` takes the SDK defaults 160 and 20 (spec `MaxSize` 160, `MaxScale` 20).

## Temporality
- **Cumulative**: the OTLP exporter default for all instrument kinds.
- **Delta**: Delta for Counter, Asynchronous Counter and Histogram, Cumulative for UpDownCounter kinds.
- **LowMemory**: Delta for synchronous Counter and Histogram, Cumulative for synchronous UpDownCounter and the asynchronous kinds.
`OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=cumulative|delta|lowmemory` (case-insensitive). Check your backend's documentation
for the temporality it accepts. Converting in the collector is stateful, so keep each series on one collector.

## Readers and exporters
- Periodic exporting reader + OTLP exporter (`OTEL_METRIC_EXPORT_INTERVAL`, default 60000 ms).
- The Prometheus exporter is configured with `OTEL_EXPORTER_PROMETHEUS_HOST` (default `localhost`) and `_PORT` (default 9464).

## Cardinality limit and exemplars
- The spec's default aggregation cardinality limit is 2000 (a view can set `aggregation_cardinality_limit`); measurements beyond
  it are reported in an overflow attribute set containing `otel.metric.overflow=true`. Query that attribute to find leaks.
- Exemplars: `OTEL_METRICS_EXEMPLAR_FILTER` accepts `trace_based` (default), `always_on`, `always_off`.

## Verify
- [ ] No `otel.metric.overflow` series in steady state.
- [ ] Backend receives the temporality it expects (no negative rates / sawtooths).

## Checked

2026-10-24. OpenTelemetry specification metrics API and SDK, SDK environment variables, OTLP metrics exporter spec (temporality preference), and the opentelemetry-java SDK metrics source (View, ViewBuilder, InstrumentSelectorBuilder, Aggregation, SdkMeterProviderBuilder; main branch). Confirmed: instrument semantics for Gauge and UpDownCounter, the Java view API calls used, base2 exponential defaults (160, 20), temporality preference values and meanings, cardinality limit default and overflow attribute, exemplar filter variable and default, export interval default. Removed vendor and Prometheus mapping claims that no spec covers.

Method: documentation only; no commands were run.
