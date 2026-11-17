---
id: computing-software.web-development.micronaut.micronaut-health-endpoint
name: micronaut-health-endpoint
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, health-endpoint, liveness, readiness, health-indicator, management, health-status]
level: practitioner
status: docs-checked
description: "Configure the Micronaut /health endpoint: liveness and readiness, details visibility, status code mapping, built-in indicators, custom HealthIndicator beans and logging."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthEndpointConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthEndpointStatusCode.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/diskSpaceHealthIndicator.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthProvidedIndicators/deadlockedThreads.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthEndpointCustomization.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthLogging.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/healthEndpoint/healthMonitoringTask.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure and extend the health endpoint

GET `/health` aggregates "health indicators". It also exposes `/health/liveness` (running and not stuck; failure may mean a restart is needed) and `/health/readiness` (fully initialized, ready to handle requests).

## Configuration

```yaml
endpoints:
  health:
    enabled: Boolean
    sensitive: Boolean
    details-visible: String     # a DetailsVisibility value
    status:
      http-mapping: Map<String, HttpStatus>
```

- `details-visible: ANONYMOUS` exposes indicator detail to unauthenticated users. Combined with `sensitive: true` the outcome is 401 Unauthorized.
- Default status mapping: UP -> 200, UNKNOWN -> 200, DOWN -> 503. To return 200 even when DOWN:

```yaml
endpoints:
  health:
    status:
      http-mapping:
        DOWN: 200
```

## Built-in indicators

All appear on `/health` and `/health/readiness`, except `DeadlockedThreadsHealthIndicator`, which is a liveness indicator (`/health/liveness`).

| Indicator | Toggle | Default |
|---|---|---|
| DeadlockedThreadsHealthIndicator | `endpoints.health.deadlocked-threads.enabled` | true |
| DiscoveryClientHealthIndicator | `endpoints.health.discovery-client-health.enabled` | true |
| DiskSpaceIndicator | `endpoints.health.disk-space.enabled` | true |
| JdbcIndicator | `endpoints.health.jdbc.enabled` | true |
| ServiceHttpClientHealthIndicator | `endpoints.health.service-http-client.enabled` | false |
| ServiceReadyHealthIndicator | `endpoints.health.service-ready-indicator-enabled` | true |

Disk space also takes `endpoints.health.disk-space.path` and `.threshold` (minimum free space, a string such as "10MB" or "200KB", or a byte count). The deadlocked-threads indicator uses `ThreadMXBean` (not supported in GraalVM Native Image) and reports DOWN with thread info and stack traces in the details.

## Custom indicator

Create a bean implementing `HealthIndicator` (subclass `AbstractHealthIndicator` to make it easier). Add the `@Liveness` or `@Readiness` qualifier; with no qualifier the indicator is part of `/health` and `/health/readiness`.

To replace the aggregator, register a `HealthAggregator` bean annotated `@Replaces(DefaultHealthAggregator.class)`. The overall status is the "worst" one: non-operational beats operational, higher severity beats lower (a `HealthStatus` has name, description, operational flag and severity).

## Logging and background monitor

```xml
<logger name="io.micronaut.management.health.aggregator.DefaultHealthAggregator" level="trace" />
```

`debug` logs indicator status; `trace` adds details.

A background thread that updates `CurrentHealthStatus` can be enabled (with `EmbeddedServer`):

```yaml
micronaut:
  application:
    name: foo
  health:
    monitor:
      enabled: true
```

Both properties are required. Its logger is `io.micronaut.management.health.monitor.HealthMonitorTask`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against all nine cited pages: endpoints, configuration keys, the ANONYMOUS and sensitive 401 note, default status mapping and the DOWN override, the indicator toggle table, disk-space and deadlocked-threads details, custom indicator and aggregator rules, and both logger names. Nothing removed.
