---
id: computing-software.software-engineering.java.micrometer-tracing-and-opentelemetry
name: micrometer-tracing-and-opentelemetry
category: computing-software
field: software-engineering
product: java
tags: [java, java-observability, micrometer-tracing, opentelemetry, otlp, distributed-tracing, trace-propagation]
level: practitioner
status: docs-checked
description: "Add distributed tracing to Spring Boot with Micrometer Tracing: tracer choices, OTLP, sampling, W3C propagation, custom spans, baggage and log correlation."
sources: ["https://docs.spring.io/spring-boot/reference/actuator/tracing.html", "https://www.w3.org/TR/trace-context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Micrometer Tracing and OpenTelemetry

Spring Boot Actuator provides dependency management and auto-configuration for Micrometer Tracing, a facade over tracer libraries. Boot ships auto-configuration for OpenTelemetry with OTLP, and OpenZipkin Brave with Zipkin.

## Dependencies and properties
- OpenTelemetry with OTLP: `org.springframework.boot:spring-boot-starter-opentelemetry`; configure the exporter with `management.opentelemetry.tracing.export.otlp.*`. Register `OtlpHttpSpanExporterBuilderCustomizer` or `OtlpGrpcSpanExporterBuilderCustomizer` beans for advanced exporter tweaks.
- Brave with Zipkin: `org.springframework.boot:spring-boot-starter-zipkin`; configure with `management.tracing.export.zipkin.*`.
- OpenTelemetry reporting to Zipkin is deprecated upstream; Boot's page says its auto-configuration will be removed in Spring Boot 4.2. Prefer Brave, or send OTLP to Zipkin directly.
- Tracing components that report data are not auto-configured under `@SpringBootTest`.

## Sampling
Boot samples only 10% of requests by default. Set `management.tracing.sampling.probability` (1.0 samples everything, as in a local trial). With OpenTelemetry, `management.opentelemetry.tracing.sampler` selects `always-on`, `always-off`, `trace-id-ratio`, `parent-based-always-on`, `parent-based-always-off` or `parent-based-trace-id-ratio` (the default: follow a sampled parent, otherwise sample by the probability). Span limits for OpenTelemetry live under `management.opentelemetry.tracing.limits.*` (for example `max-attributes`, `max-attribute-value-length`).

## Log correlation
With Micrometer Tracing, Boot adds a correlation ID built from the `traceId` and `spanId` MDC values to log lines by default. Customise with `logging.pattern.correlation`, for example `[${spring.application.name:},%X{traceId:-},%X{spanId:-}] ` (keep the trailing space; set `logging.include-application-name=false` to avoid duplicating the name).

## Propagation
Build clients from the auto-configured `RestTemplateBuilder`, `RestClient.Builder` or `WebClient.Builder`; clients created any other way do not propagate traces automatically. W3C Trace Context uses the `traceparent` header (position of the request in its trace, fixed format, for example `00-<trace-id>-<parent-id>-01`) and the optional vendor `tracestate`. A participant must at least forward both headers so traces are not broken.

## Custom spans and baggage
A `TracingAwareMeterObservationHandler` is registered on the `ObservationRegistry` and creates a span for every completed observation. Inject `ObservationRegistry` and:
```java
Observation observation = Observation.createNotStarted("some-operation", observationRegistry);
observation.lowCardinalityKeyValue("some-tag", "some-value");
observation.observe(() -> { /* business logic */ });
```
This also records a metric; for a span without a metric use the lower-level Micrometer `Tracer` API. Create baggage with `tracer.createBaggageInScope("baggage1", "value1")` in a try-with-resources block. Baggage propagates automatically with W3C propagation, not with B3. List fields in `management.tracing.baggage.remote-fields` to send them as headers, and `management.tracing.baggage.correlation.fields` to copy them into the MDC.

## Verify
Run a trace backend (the Boot page uses Zipkin), call an endpoint that calls another service, and confirm one trace with parent and child spans and the same trace ID in the logs.

## Checked
Read the Spring Boot tracing page in full and the W3C Trace Context spec (header sections grepped). The micrometer.io tracing page returned 404 and was dropped from sources. Removed as unconfirmed: dependency coordinates for Boot 3, the OTLP endpoint property and port, the list of auto-instrumented components (JDBC, Kafka, @Scheduled), `@Observed` and its aspect requirement, high-cardinality guidance, and PII advice.
Method: docs-checked 2026-11-09 against the Spring Boot Actuator tracing page and the W3C Trace Context recommendation.
