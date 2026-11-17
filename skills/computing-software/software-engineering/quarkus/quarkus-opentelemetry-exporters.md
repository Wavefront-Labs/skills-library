---
id: computing-software.software-engineering.quarkus.quarkus-opentelemetry-exporters
name: quarkus-opentelemetry-exporters
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, opentelemetry, otlp, exporter, tracing, metrics, observability]
level: advanced
status: docs-checked
description: "Configure the Quarkus OpenTelemetry extension: signal on/off properties, OTLP protocol, timeout and retry behaviour, resource attributes, test and logging exporters."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/opentelemetry.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus OpenTelemetry: switches, exporters and resources

Add `io.quarkus:quarkus-opentelemetry`. Tracing, metrics and logs are all on by default. The OpenTelemetry Java agent is neither needed nor recommended (it does not work in native mode); Quarkus extensions are instrumented directly. Properties use the `quarkus.otel.*` prefix.

## Turning things off

- `quarkus.otel.enabled=false`: disable everything at build time.
- `quarkus.otel.sdk.disabled=true`: disable the SDK at runtime.
- `quarkus.otel.exporter.otlp.enabled=false`: build-time; telemetry is generated and context propagated but nothing is sent.
- Per signal (build time): `quarkus.otel.traces.enabled`, `quarkus.otel.metrics.enabled`, `quarkus.otel.logs.enabled`; output via `quarkus.otel.<signal>.exporter` (`otlp`, `cdi`, `none`; default `cdi`).
- `quarkus.otel.logs.handler.enabled=false` removes the JBoss LogManager bridge at runtime.

## OTLP protocol

Built-in exporters speak OTLP using Vert.x senders. `quarkus.otel.exporter.otlp.protocol` defaults to `http/protobuf`; `grpc` is the alternative. When you change the protocol, change the endpoint port: `4317` for grpc, `4318` for http/protobuf. The `cdi` default describes how exporters are wired, not the protocol. `quarkus.otel.exporter.otlp.memory-mode=reusable-data` pools objects to cut GC pressure (default `immutable-data`).

## Timeout and retries

`quarkus.otel.exporter.otlp.timeout` defaults to `10s` and applies per attempt; override per signal with `quarkus.otel.exporter.otlp.metrics.timeout` (also `traces`, `logs`). A timed-out attempt is cancelled and retried, as are failed connections and `5xx` responses with http/protobuf; an export is sent at most 4 times. Retries after a timeout have no back-off, so a retry can deliver a batch twice (the OTLP spec accepts duplicates). Set the timeout above your collector or proxy's slowest answer. A slow export also delays the next: the metric reader logs `Exporter busy. Dropping metrics.`

## Resource attributes

```properties
quarkus.otel.resource.attributes=deployment.environment=dev,service.name=cart,service.namespace=shopping
```

`service.name` otherwise comes from the artifactId or `quarkus.application.name`. Custom `Resource` CDI producer beans are merged. On Kubernetes, `quarkus-kubernetes` adds env vars such as `QUARKUS_OTEL_K8S_RESOURCE_POD_NAME`; without it set them yourself. `k8s.cluster.name` is never automatic.

## Test and debug exporters

- Tests: keep `cdi` and produce an `InMemorySpanExporter` bean (from `io.opentelemetry:opentelemetry-sdk-testing`, test scope). In integration tests read it from inside the app, for example through a REST method.
- Debug: add `io.opentelemetry:opentelemetry-exporter-logging`, then `quarkus.otel.traces.exporter=logging`, `quarkus.otel.metrics.exporter=logging`, `quarkus.otel.metric.export.interval=10000ms`. Not for production.
- The standard OpenTelemetry OTLP exporter is not supported; the Quarkus defaults already use OTLP.

Dev mode starts a Grafana OTel LGTM Dev Service; disable it with `quarkus.observability.lgtm.enabled=false` or `quarkus.observability.dev-resources=false`.

## Checked

2026-11-07. Matched against the text (with includes) of: opentelemetry.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
