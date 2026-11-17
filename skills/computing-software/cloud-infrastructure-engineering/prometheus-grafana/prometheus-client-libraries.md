---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-client-libraries
name: prometheus-client-libraries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, client-libraries, client-library, prometheus-client, client-golang, prometheus-client-python, micrometer, simpleclient, prom-client, nodejs, java, go, python, counter, gauge, histogram, summary, registry, promhttp, metrics-endpoint, label-cardinality, custom-collector, pca]
level: practitioner
status: docs-checked
description: "Choose and use the official Prometheus client libraries: instrumentation rules, labels and cardinality, registries, default metrics, and the Node.js package rename."
sources: ["https://prometheus.io/docs/instrumenting/clientlibs/", "https://github.com/prometheus/client_golang", "https://github.com/prometheus/client_python", "https://github.com/prometheus/client_java", "https://github.com/prometheus/client_js", "https://prometheus.io/docs/practices/instrumentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus client libraries

**Goal:** expose correct, cheap metrics from application code with the official client libraries, following the
Prometheus instrumentation guidelines.

## 1. Which library
- Official client libraries (Prometheus docs): Go, Java or Scala, Node.js, Python, Ruby, Rust. Others (Bash, C, C++,
  .NET/C#, PHP, Perl and more) are unofficial third-party libraries.
- A client library implements the Prometheus metric types and exposes the current state of all tracked metrics on an
  HTTP endpoint that Prometheus scrapes. With no library for your language you can implement an exposition format
  yourself.
- Go (`client_golang`): supports the two most recent major Go releases; has an instrumentation part and a Prometheus
  HTTP API client (the `api/` client is experimental and alpha). Metrics can also be pushed over OTLP via the
  `go.opentelemetry.io/contrib/bridges/prometheus` bridge, but pull via `promhttp` remains the recommended default.
- Python: `pip install prometheus-client`; documentation at prometheus.github.io/client_python.
- Java: current docs at prometheus.github.io/client_java; source for 0.16.0 and older is on the `simpleclient` branch.
- Node.js: the README now installs `@prometheus-io/client` (previously published as `prom-client`; see its CHANGELOG
  for breaking changes).

## 2. Instrumentation rules (Prometheus guidelines)
- Instrument everything: every library, subsystem and service should have a few metrics. Instantiate the metric
  classes in the same file you use them.
- Online-serving systems: queries, errors, latency, optionally in-progress requests. Count queries when they end, so
  they line up with error and latency stats, and be consistent.
- Offline processing: per stage, items in, in progress, last processed time and items out; consider a heartbeat item.
- Batch jobs: the key metric is the last time the job succeeded; push gauges to a Pushgateway; very frequent jobs
  (more often than every 15 minutes) should become daemons.
- Libraries should provide instrumentation with no extra user configuration. For every log line, have a counter; count
  failures and also expose total attempts so the failure ratio is easy to compute.
- Threadpools: queued requests, threads in use, total threads, tasks processed, time taken, queue wait. Caches: total
  queries, hits, latency.
- Custom collectors: export a gauge for collection duration in seconds and one for errors; durations as gauges are
  acceptable only for collectors and batch jobs.

## 3. Labels, types and cost
- Use one metric with labels (for example `http_responses_total` with a `code` label) instead of metric names built
  from values. Do not procedurally generate metric names.
- Each label set is another time series. Guideline: keep metric cardinality below 10, and for those that exceed it
  limit to a handful across the system; if cardinality is over 100 or could grow that large, investigate alternatives.
  If unsure, start with no labels.
- Counter vs gauge: if the value can go down it is a gauge. Take `rate()` of counters, never of gauges.
- Export a Unix timestamp rather than time since an event, and compute `time() - my_timestamp_metric`.
- Avoid missing metrics: export 0 for series you know may exist. Go, Java and Python clients export 0 automatically for
  metrics with no labels.
- Inner loops (above about 100k calls per second per process): limit metrics updated, avoid labels or cache the label
  lookup (`With()` in Go, `labels()` in Java), and beware time calls that need a syscall.

## 4. Node.js client notes (from its README)
- It does not bundle a web framework: respond to scrape requests with `await registry.metrics()`.
- `collectDefaultMetrics` collects the recommended default metrics plus Node.js ones (event loop lag, active handles,
  GC, version); file descriptor and memory metrics are Linux only. It accepts options such as `prefix` and `labels`.
- Metrics take `labelNames`; labelled metrics are not exported until observed once, and histograms offer `zero()` to
  pre-create expected label values.
- Global registry by default; use `registers: [...]` for others, `Registry.merge` to expose several on one endpoint
  (a duplicate metric name throws). With the Node.js `cluster` module and non-default registries, use
  `AggregatorRegistry.setRegistries`.
- Exemplars (OpenMetrics) need an OpenMetrics-type registry; the default registry type is Prometheus text format 0.0.4.

## Gotchas
- Put the route template, not the raw path, in labels (unbounded labels explode series).
- Do not take `rate()` of a gauge.
- Check each library's own documentation for multiprocess, async and framework-specific behaviour; this skill's
  fetched pages did not cover them.

## Verify
- [ ] The `/metrics` endpoint is scraped and every counter is monotonic.
- [ ] Label sets are bounded and the per-instance series count is known.
- [ ] Failure counters have a matching attempts metric.

## Checked
2026-11-08: confirmed against the Prometheus client libraries page, the instrumentation practices page, and the
README pages of client_golang, client_python, client_java and the Node.js client. Removed: the Go, Python, Java and
Node code samples, Python multiprocess instructions, Micrometer property names, bucket recommendations, series-count
rules of thumb and `promtool` commands, because none of the fetched pages stated them.
Method: documentation only; no commands were run.
