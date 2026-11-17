---
id: computing-software.software-engineering.quarkus.quarkus-micrometer-custom-meters
name: quarkus-micrometer-custom-meters
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, micrometer, metrics, counter, gauge, timer, prometheus]
level: practitioner
status: docs-checked
description: "Create counters, gauges, timers and distribution summaries in Quarkus with Micrometer, including registry injection, naming, tags and @Counted/@Timed."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/telemetry-micrometer.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Micrometer meters in Quarkus

Add a registry extension, e.g. `quarkus-micrometer-registry-prometheus`; `quarkus-micrometer` is the core Micrometer extension. Metrics are served on the main HTTP server at `/q/metrics` unless the management interface is enabled.

## Get a MeterRegistry

Use constructor injection, `@Inject MeterRegistry registry;`, or the global `Metrics.globalRegistry`.

## Naming and tags

Use dotted names (`a.name.like.this`); Micrometer converts per backend (`registry.timer("http.server.requests")` becomes `http_server_requests_seconds` on Prometheus). Tags are the dimensions. Every unique name plus tag combination is a separate time series, so unbounded tag values cause a "cardinality explosion". Never use end-user data as tag values.

## Meter types

- Counter (only increases): `registry.counter("example.prime.number", "type", "prime")`, or `Counter.builder("count.me").baseUnit("beans").description("...").tags("region","test").register(registry)`, or annotate a method with `@Counted(value = "counted.method", extraTags = {"extra","annotated"})`.
- Gauge (sampled value that can go up or down): `registry.gaugeCollectionSize("fantastic.list", Tags.of("key","value"), new ArrayList<>())` or `Gauge.builder("jvm.threads.peak", threadBean, ThreadMXBean::getPeakThreadCount).register(registry)`. Gauge tags are fixed at construction. Micrometer holds no strong reference to the observed object; after GC the gauge is omitted or reports `NaN`. Prefer a counter when the value only increments.
- Distribution summary (records a value, not time): `registry.summary("bytes.written", "protocol", "http")`.
- Timer: `registry.timer("fabric.selection", "primary", "blue")` or `@Timed(value = "call", extraTags = {"region","test"})`. Record with `timer.record(Runnable)`, `timer.recordCallable(...)`, `timer.wrap(...)`, or `Timer.Sample sample = Timer.start(registry); ... sample.stop(registry.timer("my.timer", "response", status))` when the tag is known only at the end.

## Annotation tags

`@Timed` adds `class`, `method` and `exception` tags. Annotate parameters with `@MeterTag` (optionally `key=`, `resolver=` a `ValueResolver` bean, or `expression=` backed by a `ValueExpressionResolver` bean) to derive tag values. Values must be low-cardinality.

## Gotchas

- Meters are created lazily: nothing shows until the code path runs (for example, call the endpoint once).
- Percentiles are not re-aggregable across instances; count, sum and histogram data are.
- Timers reject negative values.
- To skip HTTP paths use `quarkus.micrometer.binder.http-server.ignore-patterns`; to fix templated URIs use `quarkus.micrometer.binder.http-server.match-patterns=/example/prime/[0-9]+=/example/{jellybeans}`.

## Checked

2026-11-07. Matched against the text (with includes) of: telemetry-micrometer.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that the core extension is itself the registry setup; the opening line now says a registry extension (for example `quarkus-micrometer-registry-prometheus`) is added and `quarkus-micrometer` is the core extension.

Method: documentation only; no commands were run.
