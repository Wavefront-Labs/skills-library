---
id: computing-software.software-engineering.spring-boot.actuator-health-endpoint
name: actuator-health-endpoint
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, health, healthindicator, statusaggregator, show-details, http-mapping, reactive-health]
level: practitioner
status: docs-checked
description: "Configure the Actuator health endpoint: show-details, auto-configured indicators, writing HealthIndicators, custom statuses, HTTP mapping, reactive indicators, DataSource health."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Detail level: `management.endpoint.health.show-details` and `show-components` take `never` (default), `when-authorized` (roles via `management.endpoint.health.roles`; any authenticated user if none set) or `always`. With `always` and a secured app, permit the health endpoint for authenticated and unauthenticated users.

Health is collected from the `HealthContributorRegistry` (all `HealthContributor` beans). A contributor is a `HealthIndicator` (has a `Status`) or a `CompositeHealthContributor`. The `StatusAggregator` sorts statuses by an ordered list and takes the first; `UNKNOWN` if none is known. Register or unregister at runtime via the registry.

Auto-configured indicators are toggled by `management.health.<key>.enabled` (all off with `management.health.defaults.enabled`). Keys: `amqprabbit`, `cassandra`, `couchbase`, `db`, `diskspace`, `elasticsearch`, `hazelcast`, `jms`, `ldap`, `mail`, `mongodb`, `neo4j`, `ping`, `rabbit`, `redis`, `ssl`. The `ssl` indicator has `management.health.ssl.certificate-validity-warning-threshold`; a soon-expiring certificate shows `WILL_EXPIRE_SOON`. `livenessstate` and `readinessstate` indicators are on by default; disable with `management.endpoint.health.probes.enabled`.

Custom indicator: register a bean implementing `HealthIndicator` and return a `Health` with a status and optional details. The ID is the bean name minus a `HealthIndicator` suffix (`MyHealthIndicator` appears as `my`). A warning is logged for indicators slower than 10 seconds; change with `management.endpoint.health.logging.slow-indicator-threshold`.

Custom status (for example `FATAL`): provide a `StatusAggregator` or set the order:
```yaml
management:
  endpoint:
    health:
      status:
        order: "fatal,down,out-of-service,unknown,up"
```
HTTP code: `DOWN` and `OUT_OF_SERVICE` map to 503; `UP` and `UNKNOWN` to 200. Configuring any custom mapping disables those defaults, so restate them:
```yaml
management:
  endpoint:
    health:
      status:
        http-mapping:
          down: 503
          fatal: 503
          out-of-service: 503
```
For more control define an `HttpCodeStatusMapper` bean.

Reactive: `ReactiveHealthContributor` / `ReactiveHealthIndicator` (consider extending `AbstractReactiveHealthIndicator`); regular contributors run on the elastic scheduler; use `ReactiveHealthContributorRegistry` and wrap regular ones with `ReactiveHealthContributor#adapt`. Auto-configured reactive indicators: `cassandra`, `couchbase`, `elasticsearch`, `mongodb`, `neo4j`, `r2dbc`, `redis`; they replace regular ones, and unhandled `HealthIndicator`s are wrapped.

DataSource: the `db` indicator covers routing data sources, naming each target by routing key; set `management.health.db.ignore-routing-data-sources` to `true` to omit them.

## Checked

2026-11-07

Read endpoints.adoc in full (cited Actuator endpoints page); used Health Information through DataSource Health, including the HealthIndicator, reactive and status-mapping sections. The MyHealthIndicator and MyReactiveHealthIndicator include examples were not opened.
Confirmed: show-details and show-components values with default never, roles, the secured-app NOTE for always; HealthContributorRegistry, HealthIndicator vs CompositeHealthContributor, StatusAggregator ordering and the UNKNOWN fallback; every indicator key in the auto-configured table (amqprabbit ... ssl) and management.health.defaults.enabled; ssl warning threshold and WILL_EXPIRE_SOON; livenessstate/readinessstate indicators and management.endpoint.health.probes.enabled; bean-name-minus-suffix identifier (`my`); the 10-second slow-indicator warning and its property; status.order example; http-mapping defaults (503 for DOWN and OUT_OF_SERVICE, 200 otherwise) and the "custom mapping disables defaults" rule; HttpCodeStatusMapper; reactive contributors, elastic scheduler, adapt, AbstractReactiveHealthIndicator and the reactive indicator keys; ignore-routing-data-sources.
Nothing trimmed.

Method: documentation only; no commands were run.
