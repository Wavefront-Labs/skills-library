---
id: computing-software.software-engineering.ktor.ktor-opentelemetry-tracing
name: ktor-opentelemetry-tracing
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, opentelemetry, tracing, observability, otlp, grafana, spans]
level: advanced
status: docs-checked
description: "Trace Ktor server requests with the KtorServerTelemetry plugin: SDK setup, install, span kind and attribute extractors, header capture, and Grafana LGTM export."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-opentelemetry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor server tracing with OpenTelemetry

The `KtorServerTelemetry` plugin (package `io.opentelemetry.instrumentation`, artifact `io.opentelemetry.instrumentation:opentelemetry-ktor-3.0`) creates spans for incoming requests with route, HTTP method and status, extracts trace context from request headers, and lets you customize span names, attributes and kinds. The client counterpart is `KtorClientTelemetry`.

## 1. Build an OpenTelemetry instance

- Automatic: `AutoConfiguredOpenTelemetrySdk` configures exporters/resources from system properties and environment variables; you can still add e.g. a `service.name` resource attribute.
- Programmatic: build `OpenTelemetrySdk` with an `OtlpGrpcSpanExporter` (e.g. endpoint `http://localhost:4317`), `SdkTracerProvider` with `BatchSpanProcessor`, and `ContextPropagators.create(W3CTraceContextPropagator.getInstance())`, finishing with `buildAndRegisterGlobal()`.

## 2. Install

```kotlin
install(KtorServerTelemetry) {
    setOpenTelemetry(openTelemetry)
}
```

Gotcha: install it before any other logging or telemetry plugins.

## 3. Tune tracing

```kotlin
install(KtorServerTelemetry) {
    knownMethods(HttpMethod.DefaultMethods + CUSTOM_METHOD)   // trace extra methods
    capturedRequestHeaders(HttpHeaders.UserAgent)             // headers as attributes
    spanKindExtractor {
        if (httpMethod == HttpMethod.Post) SpanKind.PRODUCER else SpanKind.CLIENT
    }
    attributesExtractor {
        onStart { attributes.put("start-time", System.currentTimeMillis()) }
        onEnd { attributes.put("end-time", Instant.now().toEpochMilli()) }
    }
}
```

By default only standard methods (`GET`, `POST`, `PUT`, ...) are traced.

## 4. Check with Grafana LGTM

Run the `grafana/otel-lgtm` image (Grafana, Tempo, Loki, Mimir), publishing ports 4317 (OTLP gRPC), 4318 (OTLP HTTP) and 3000 (Grafana UI), with `GF_SECURITY_ADMIN_USER=admin` and `GF_SECURITY_ADMIN_PASSWORD=admin`. Point the app at it:

```shell
export OTEL_TRACES_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

or JVM flags `-Dotel.traces.exporter=otlp -Dotel.exporter.otlp.protocol=grpc -Dotel.exporter.otlp.endpoint=http://localhost:4317`.

Verify: open http://localhost:3000/, log in with admin/admin, then go to Drilldown, then Traces to filter spans and inspect timelines.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-opentelemetry.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
