---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.micrometer-spring-boot-prometheus
name: micrometer-spring-boot-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, micrometer-prometheus, spring-boot-actuator-prometheus, java, jvm-metrics, percentiles-histogram, servicemonitor]
level: practitioner
status: docs-checked
description: "Expose Spring Boot metrics to Prometheus via Micrometer and Actuator: dependencies, endpoint exposure, histogram buckets for SLOs, common tags, and naming translation."
sources: ["https://docs.spring.io/spring-boot/reference/actuator/metrics.html", "https://docs.micrometer.io/micrometer/reference/implementations/prometheus.html", "https://docs.spring.io/spring-boot/reference/actuator/endpoints.html", "https://docs.micrometer.io/micrometer/reference/concepts/histogram-quantiles.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Micrometer + Spring Boot Actuator for Prometheus

## Setup
```xml
<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
<dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
```
```yaml
management:
  endpoints.web.exposure.include: health,prometheus   # by default only /health is exposed over HTTP
  server.port: 8081                         # optional separate management port; keep actuator off the public port
  metrics:
    tags:
      region: us-east-1                     # common tags: management.metrics.tags.<name>
    distribution:
      percentiles-histogram:
        http.server.requests: true          # publish a histogram suitable for aggregable percentile approximations
      slo:
        http.server.requests: 100ms,300ms,1s   # extra buckets at SLO thresholds
      minimum-expected-value:
        http.server.requests: 5ms           # clamp the range to publish fewer buckets
      maximum-expected-value:
        http.server.requests: 10s
```
Prometheus scrapes the actuator endpoint `/actuator/prometheus`. Only expose endpoints that carry nothing sensitive, or
secure them behind a firewall or Spring Security.

## Naming translation
Spring Boot names server request metrics `http.server.requests` (rename with
`management.observations.http.server.requests.name`). A timer is exported to Prometheus as `${name}_seconds_count`,
`${name}_seconds_sum` and `${name}_seconds_max`; enabling percentile histograms adds `${name}_seconds_bucket`.
Look at the actual `/actuator/prometheus` output for the exact series.
Spring documents the tags `exception` (simple class name) and `outcome` (INFORMATIONAL, SUCCESS, REDIRECTION,
CLIENT_ERROR, SERVER_ERROR) among others.

## Custom metrics
```java
Timer.builder("payment.call").publishPercentileHistogram().register(registry).record(() -> callPsp());
```
`serviceLevelObjectives(...)` adds SLO buckets to a histogram; `minimumExpectedValue` and `maximumExpectedValue`
control how many buckets `publishPercentileHistogram` ships (Micrometer clamps timers to 1 ms - 1 minute by default).

## Gotchas
- Without percentile histograms you only get `_count`, `_sum` and `_max`: no latency percentiles in Prometheus.
  Client-side `percentiles` publish computed values that cannot be aggregated across tags, and the Prometheus Java
  client 1.x cannot have both under the same metric name.
- `micrometer-registry-prometheus` uses the "new" Prometheus Java client (1.x); `micrometer-registry-prometheus-simpleclient`
  uses the "legacy" client (0.x).

## Verify
- [ ] `/actuator/prometheus` shows `http_server_requests_seconds_bucket` series once the histogram is enabled.
- [ ] Prometheus `up` is 1 for the application's target.

## Checked
2026-10-31. Confirmed against the Spring Boot Actuator metrics page (`/actuator/prometheus`, `http.server.requests`
rename property, `exception` and `outcome` tags, per-meter `management.metrics.distribution.*` properties,
`management.metrics.tags.*` common tags), the Actuator endpoints page (only `/health` exposed over HTTP by default,
`management.endpoints.web.exposure.include`, `management.server.port`) and the Micrometer Prometheus and
Histograms pages (new 1.x vs legacy 0.x client, `_seconds_count/_sum/_max/_bucket` series, aggregability, default
1 ms to 1 minute clamp, `Timer.builder` calls). Removed: the unverified `uri="UNKNOWN"` note, the ServiceMonitor
snippet, `Counter.builder` example, the literal `le="0.3"` bucket check and the `application` tag expression.
Method: documentation only; no commands were run.
