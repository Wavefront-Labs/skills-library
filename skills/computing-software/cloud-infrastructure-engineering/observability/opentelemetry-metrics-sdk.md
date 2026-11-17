---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-metrics-sdk
name: opentelemetry-metrics-sdk
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel, otel-metrics, opentelemetry-metrics, meter, meter-provider, instruments, counter, updowncounter, histogram, gauge, observable-counter, observable-gauge, asynchronous-instruments, views, otel-views, aggregation, explicit-bucket-histogram, exponential-histogram, aggregation-temporality, cumulative, delta, periodic-exporting-metric-reader, otlp-metrics, prometheus-exporter, attributes, cardinality, semantic-conventions-metrics]
level: advanced
status: gated
description: "Use the OpenTelemetry metrics SDK correctly: choosing instruments (counter, updowncounter, histogram, gauge, observables), views to rename/drop attributes/set buckets."
sources: ["https://opentelemetry.io/docs/concepts/signals/metrics/", "https://opentelemetry.io/docs/specs/otel/metrics/sdk/", "https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality", "https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/", "https://opentelemetry.io/docs/specs/semconv/general/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry metrics SDK

**Goal:** instrument metrics once with the OTel API so they export correctly to
Prometheus/Mimir, Datadog, or any OTLP backend, with bounded cardinality and the right
temporality, and know how the SDK knobs (views, readers) shape what comes out.

## 1. API vs SDK, and the pipeline
`MeterProvider` (SDK, configured once at startup) → `Meter` (per library/module, `get_meter("checkout", version)`)
→ **instruments** → measurements with attributes → SDK aggregates per `View` →
`MetricReader` (periodic, e.g. `PeriodicExportingMetricReader`, or a pull reader)
→ `Exporter` (OTLP gRPC/HTTP, Prometheus, console). Libraries use only the API; the
application wires the SDK. Zero-code agents wire a default SDK from env vars
(`OTEL_METRICS_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_METRIC_EXPORT_INTERVAL=60000`).

## 2. Instruments: pick by semantics
| Instrument | Sync/Async | Use for | Prom equivalent |
|---|---|---|---|
| `Counter` | sync `add(+n)` | things that only go up: requests, bytes, errors | counter `_total` |
| `UpDownCounter` | sync `add(±n)` | in-flight requests, queue length changes, connections | gauge |
| `Histogram` | sync `record(v)` | durations, sizes — distributions | histogram (explicit or native) |
| `Gauge` | sync `record(v)` | last value you set yourself (temperature, config value) | gauge |
| `ObservableCounter` / `ObservableUpDownCounter` / `ObservableGauge` | async callback at collection | values you read from elsewhere: CPU time, memory, cache size, thread count | counter / gauge |
Rules: name in `dot.case` per semconv (`http.server.request.duration`), unit in UCUM (`s`,
`By`, `{request}`), description set. Prefer `ObservableGauge` over polling in a thread.
Durations in **seconds** in current semconv; older conventions used milliseconds, and the
`OTEL_SEMCONV_STABILITY_OPT_IN` environment variable controls the migration.

```python
# (gated: unconfirmed, source is paywalled or blocked) Python API names below were not checked
from opentelemetry import metrics
meter = metrics.get_meter("checkout", "1.4.0")
reqs = meter.create_counter("checkout.requests", unit="{request}", description="Checkout requests")
dur  = meter.create_histogram("checkout.duration", unit="s", description="Checkout latency")
inflight = meter.create_up_down_counter("checkout.inflight", unit="{request}")
def cb(options): yield metrics.Observation(cache.size(), {"cache": "prices"})
meter.create_observable_gauge("checkout.cache.size", callbacks=[cb], unit="{entry}")
reqs.add(1, {"http.response.status_code": 200, "http.route": "/checkout"})
```

## 3. Views: fix what you cannot change in code
Express views in your SDK's own API (names differ per language; not covered here).

Per the SDK spec, views select instruments by criteria such as `meter_name` and instrument name, and can set a
new name, description, aggregation (including Drop), an `attribute_keys` allow-list and an
`aggregation_cardinality_limit`. Measurements beyond a cardinality limit are aggregated into a single overflow
data point with attribute `otel.metric.overflow=true`. The declarative config file
(`OTEL_EXPERIMENTAL_CONFIG_FILE`) takes precedence over other SDK configuration.

## 4. Temporality: the thing that bites
- **Cumulative** (value since start): counters monotonic from process start.
- **Delta** (value since last export): a delta data point after a gap can indicate a reset downstream;
  converting delta to cumulative needs state held by the converting component.
- Choose per OTLP exporter with the `temporality_preference` setting: `cumulative` (default), `delta`, or
  `lowmemory` (delta for counters and histograms, cumulative for all other instruments).
  Match the backend: a Prometheus-style pull path expects cumulative.
- Histograms: explicit buckets map to classic histograms. Exponential (native) histograms are not supported by
  the Prometheus text exposition or OpenMetrics formats and SHOULD be dropped or MAY be converted to
  fixed-bucket histograms when unsupported (Prometheus compatibility spec).

## 5. How it appears in Prometheus
Per the OTel Prometheus compatibility spec:
- A `_total` suffix SHOULD be added to monotonic sums that lack it; units are translated to UCUM-style suffixes.
- Resource attributes are carried on a `target_info` gauge (constant value 1) rather than on every series.
- `job` and `instance` labels distinguish scraped targets and must be derivable from the resource.
For exact attribute-to-label promotion options, see the Prometheus and Collector exporter documentation (not covered here).

## 6. Export configuration
```bash
OTEL_SERVICE_NAME=checkout
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=prod,service.version=1.4.0
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc            # or http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_METRIC_EXPORT_INTERVAL=30000
OTEL_METRICS_EXEMPLAR_FILTER=trace_based
```
Pull alternative: a Prometheus metric reader exposing `/metrics` on the app. Push through a Collector is the common default.

## Gotchas
- Creating instruments per request (`create_counter` inside a handler) leaks; create once.
- Attribute values must be bounded: `http.route` (template) not `url.path`; user ids never.
  When a cardinality limit applies, extra combinations merge into `otel.metric.overflow=true`.
- The SDK default explicit boundaries are `0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000`,
  a poor fit for second-valued histograms; set boundaries with an instrument advisory or a view.
- Async callbacks must be fast and must not block; they run at every collection.
- `OTEL_METRIC_EXPORT_INTERVAL` defaults to 60000 ms.

## Verify
- [ ] The Prometheus-format output shows `_total` counters and a `target_info` series.
- [ ] Series count per instrument stays within your estimate and no `otel_metric_overflow` label appears.
- [ ] Backend of choice receives the configured temporality (Datadog shows correct per-interval counts; Prometheus `rate()` works with no resets).

## Checked
Checked 2026-10-28 against the OTel metrics concepts page, Metrics SDK spec, SDK environment variable spec, metrics data-model temporality page and Prometheus/OpenMetrics compatibility spec.
- Confirmed: instrument semantics (counter, UpDownCounter, histogram, synchronous Gauge, asynchronous variants), view criteria (`meter_name`, instrument name), `attribute_keys`, `aggregation_cardinality_limit`, `otel.metric.overflow=true`, `OTEL_EXPERIMENTAL_CONFIG_FILE`, `OTEL_METRICS_EXPORTER` (default otlp), `OTEL_METRIC_EXPORT_INTERVAL` (60000), `OTEL_METRICS_EXEMPLAR_FILTER` (default trace_based), default explicit bucket boundaries, `temporality_preference` values, `_total` suffix rule, `target_info`, native-histogram handling.
- Removed: default cardinality limit of 2000, Prometheus/Mimir flags and settings, `_ratio`, `PrometheusMetricReader`, Collector converter processor names, `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`, the Python advisory keyword, "designed for milliseconds", vendor temporality preferences.
- Removed: the Go view snippet (not checked against the Go SDK).
- Gated: the Python snippet's API names (`create_counter`, `create_histogram`, `create_up_down_counter`, `create_observable_gauge`, `metrics.Observation`) were not on any fetched page (gated: unconfirmed, source is paywalled or blocked) - the Python API docs were not fetched.

Method: documentation only; no commands were run.
