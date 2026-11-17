---
id: computing-software.software-engineering.spring-boot.test-observability-metrics-and-tracing
name: test-observability-metrics-and-tracing
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, testing, autoconfiguremetrics, autoconfiguretracing, observationregistry, traceparent, meterregistry]
level: practitioner
status: docs-checked
description: "Metrics, tracing and observations in Spring Boot tests: @AutoConfigureMetrics, @AutoConfigureTracing, the global registry, test clients not instrumented and traceparent."
sources:
  - https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
  - https://docs.spring.io/spring-boot/4.2-SNAPSHOT/reference/testing/spring-boot-applications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metrics: with `@SpringBootTest`, meter registries other than the in-memory one are not auto-configured regardless of classpath. To export to another backend in an integration test, annotate with `@AutoConfigureMetrics` (from `spring-boot-micrometer-metrics-test`). On a sliced test it auto-configures an in-memory `MeterRegistry` and exporting is not supported. Registries are not added to the global registry in tests; use `@AutoConfigureMetrics(useGlobalRegistry = true)` or set `management.metrics.use-global-registry` to `true`.

Tracing: with `@SpringBootTest`, tracing components that report data are not auto-configured regardless of classpath. Use `@AutoConfigureTracing` (from `spring-boot-micrometer-tracing-test`) to get them. On a sliced test it auto-configures a no-op `Tracer`; exporting is not supported. For your own reporting components (such as a custom `SpanExporter` or `brave.handler.SpanHandler`) that must be inactive in tests, annotate them with `@ConditionalOnEnabledTracingExport`.

Observations: `@AutoConfigureTracing` or `@AutoConfigureMetrics` on a sliced test auto-configures an `ObservationRegistry`. The auto-configured `RestTestClient` and `WebTestClient` are part of the harness and are not instrumented: only the application's own observations are recorded, so test requests do not appear in client metrics or become a trace root. To test handling of an incoming trace, send a known trace context such as a W3C `traceparent` header; accepted propagation formats come from `management.tracing.propagation.consume`.

Version note: the global-registry paragraph and the note about the test clients not being instrumented (with the `traceparent` advice) are on the 4.2-SNAPSHOT version of the page and were not on the 4.1.2 version when checked; the other points are on both.

## Checked

2026-11-07. Read testing/spring-boot-applications.html (4.1.2 and 4.2-SNAPSHOT) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Added the 4.2-SNAPSHOT page as a source and a version note: the global-registry paragraph and the not-instrumented test clients / traceparent note appear on the 4.2-SNAPSHOT page, not on 4.1.2. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
