---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-java-client-1x
name: prometheus-java-client-1x
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [client-java, prometheus-java-client, client-libraries, jvm-metrics, instrumentation, java]
level: practitioner
status: docs-checked
description: "Instrument JVM code with Prometheus client_java 1.x: counter, gauge and histogram builders, the _total suffix, classic and native histograms, and the simpleclient bridge."
sources:
  - https://prometheus.github.io/client_java/
  - https://github.com/prometheus/client_java
  - https://prometheus.github.io/client_java/getting-started/metric-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus Java client (client_java 1.x)

Version 1.0.0 and higher is a breaking change from 0.16.0 and older (simpleclient); the pre-1.0.0 code lives on the simpleclient branch. New in 1.0.0: native histograms, an OpenTelemetry (OTLP push) exporter, and runtime configuration through a properties file or system properties. The modules are published as separate artifacts such as `prometheus-metrics-core`, `prometheus-metrics-exporter-httpserver`, `prometheus-metrics-instrumentation-jvm`, `prometheus-metrics-exporter-servlet-jakarta` and `prometheus-metrics-simpleclient-bridge`.

## Metric builders
```java
Counter serviceTimeSeconds = Counter.builder()
    .name("service_time_seconds_total")
    .help("total time spent serving requests")
    .unit(Unit.SECONDS)
    .register();
serviceTimeSeconds.inc(Unit.millisToSeconds(200));      // value 0.2

Gauge temperature = Gauge.builder()
    .name("temperature_celsius").help("current temperature")
    .labelNames("location").unit(Unit.CELSIUS).register();
temperature.labelValues("Berlin").set(22.3);

Histogram duration = Histogram.builder()
    .name("http_request_duration_seconds")
    .help("HTTP request service time in seconds")
    .unit(Unit.SECONDS)
    .labelNames("method", "path", "status_code")
    .register();
duration.labelValues("GET", "/", "200").observe(Unit.nanosToSeconds(System.nanoTime() - start));
```
- Counters only increase and need not be integers (a counter can hold total time spent).
- In the default OpenMetrics 1.0 and Prometheus text formats counters are exposed with the `_total` suffix. Naming the counter with or without `_total` gives the same exposed name, so do not add it twice by hand.
- The `Unit` class converts other time units to seconds (`millisToSeconds`, `nanosToSeconds`). Histograms implement `TimerApi`, which provides convenience methods for timing durations.
- If `JvmMetrics` is registered (module `prometheus-metrics-instrumentation-jvm`), a `jvm_runtime_info` metric is exposed out of the box.

## Histograms: classic and native
- By default a histogram keeps both flavours; which one is used depends on the scrape request. A default Prometheus scrape gets the classic flavour. With `--enable-feature=native-histograms` Prometheus requests the protobuf format and ingests the native histogram. Adding `scrape_classic_histograms: true` to the scrape config ingests both, which suits a migration.
- Builder options include `nativeOnly()` / `classicOnly()`, `classicUpperBounds(...)`, `classicLinearUpperBounds(start, width, count)`, `classicExponentialUpperBounds(start, factor, count)` and `nativeMaxNumberOfBuckets()`.
- Default classic upper bounds are .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5 and 10, designed for request durations in seconds. Pick custom bounds for other units (for example bytes).
- Native bucket limit defaults to 160; when reached, the native histogram reduces its resolution automatically.
- Native histograms with custom buckets (NHCB, schema -53): keep the classic custom bounds, and set `convert_classic_histograms_to_nhcb: true` (with `scrape_protocols: ["PrometheusProto"]`) on the Prometheus scrape job to convert them on ingestion.

## Migrating from simpleclient
The `prometheus-metrics-simpleclient-bridge` module lets existing simpleclient 0.16.0 metrics be used with the new 1.0.0 `PrometheusRegistry` without rewriting instrumentation code. Not every simpleclient module was in the initial 1.0.0 release.

## Verify
- [ ] The scrape target exposes your metric names, with `_total` once on counters.
- [ ] A histogram shows classic buckets on a default scrape; native data appears only after enabling native histograms on the server.

## Checked
Checked 2026-11-08 against the client_java documentation home page, the Metric Types page and the repository module list. Removed because the pages do not state them: Maven snippets and version property, the `HTTPServer` builder and port, `initLabelValues`, the configuration property names, "one HTTPServer per JVM", and the Micrometer advice for Spring Boot.

Method: docs-only read of cited pages, 2026-11-08
