---
id: computing-software.software-engineering.java.micrometer-metrics-in-spring-boot
name: micrometer-metrics-in-spring-boot
category: computing-software
field: software-engineering
product: java
tags: [java, java-observability, micrometer-metrics, prometheus, meterregistry, timed, cardinality, histogram-buckets]
level: practitioner
status: docs-checked
description: "Add custom Micrometer meters in Spring Boot, name and tag them safely, bind gauges with MeterBinder, and configure histograms and percentiles."
sources: ["https://docs.micrometer.io/micrometer/reference/concepts/gauges.html", "https://docs.micrometer.io/micrometer/reference/concepts/naming.html", "https://docs.micrometer.io/micrometer/reference/concepts/histogram-quantiles.html", "https://docs.spring.io/spring-boot/reference/actuator/metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Micrometer metrics in Spring Boot

## Setup
Spring Boot provides an actuator endpoint at `/actuator/prometheus` that presents metrics in the format a Prometheus scrape expects. Common tags and per-meter distribution settings are plain properties:
```yaml
management:
  metrics:
    tags: { region: us-east-1, stack: prod }      # added to all meters
    distribution:
      percentiles-histogram: { http.server.requests: true }
      slo: { http.server.requests: 100ms,300ms,1s }
```
Per-meter properties apply to any meter ID that starts with the given name. Available: `management.metrics.enable`, `distribution.percentiles-histogram`, `distribution.percentiles`, `distribution.slo`, `distribution.minimum-expected-value` / `maximum-expected-value` (fewer buckets), and `distribution.expiry` / `buffer-length` (weight recent samples).

## Instruments
Builder style on a `MeterRegistry`, for example:
```java
Timer.builder("orders.processing").publishPercentileHistogram().register(registry);
```
Register gauges that depend on other beans through a `MeterBinder` bean, which sets up the right dependency order and is bound to the Spring-managed registry automatically:
```java
@Bean
public MeterBinder queueSize(Queue queue) {
    return registry -> Gauge.builder("queueSize", queue::size).register(registry);
}
```
- Spring Data repository calls are timed automatically as `spring.data.repository.invocations`; `@Timed` is supported on repository interfaces and methods, and `longTask = true` enables a long task timer.
- `MeterFilter` beans customise individual meters, for example `MeterFilter.renameTag("com.example", "mytag.region", "mytag.area")`.

## Naming and cardinality
Use lowercase dot notation for meter and tag names; it translates best to each backend (Prometheus renders `http.server.requests` as `http_server_requests_duration_seconds`). Tag values from user-supplied input can blow up cardinality: normalise and bound them. The docs' example is the URI tag on HTTP requests, where unbounded 404 paths should collapse to a value like NOT_FOUND.

## Histograms and percentiles
- `publishPercentiles` publishes percentiles computed in your application; they cannot be aggregated across dimensions.
- `publishPercentileHistogram` publishes buckets so the backend can approximate aggregable percentiles. Where it is supported, client-side percentiles are usually redundant.
- `serviceLevelObjectives` publishes a cumulative histogram with buckets from your SLOs (adds buckets, or is the only buckets where aggregable percentiles are unsupported).
- `minimumExpectedValue` / `maximumExpectedValue` bound bucket count and memory.
- The Prometheus Java client 1.x does not allow both histogram and client-side percentiles under the same metric name.

## Gotchas
- A gauge keeps only a weak reference to the observed object. If nothing else holds it, it is garbage collected and the gauge reports NaN or disappears (registry-dependent). Hold a strong reference yourself.
- Graphite users: common-tag order matters, so define a custom `MeterFilter` instead of the property.

## Verify
`curl localhost:8080/actuator/prometheus` shows the meter with its tags; if a gauge vanishes after a few minutes, suspect garbage collection of its source object.

## Checked

Method: docs-checked 2026-11-09 against the Micrometer reference pages Gauges, Naming Meters and Histograms and Percentiles, and the Spring Boot Actuator Metrics page (Boot 4.1.x docs). Dropped unconfirmed claims (TimedAspect for bean-level @Timed, MeterFilter.maximumAllowableTags, counter and timer definitions, SimpleMeterRegistry test advice, YAML snippet details such as the application and env tags, series-count check).
