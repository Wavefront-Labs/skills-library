---
id: computing-software.web-development.micronaut.micronaut-builtin-endpoints
name: micronaut-builtin-endpoints
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, builtin-endpoints, management, endpoints, management-port, threaddump, beans, routes]
level: intro
status: docs-checked
description: "Know which built-in Micronaut management endpoints are on or off by default, how to move them to a separate port, and how the beans, routes, threaddump and metrics endpoints work."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/beansEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/routesEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/threadDumpEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/metricsEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/stopEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/loggersEndpoint.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/providedEndpoints/cachesEndpoint.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Built-in management endpoints

Goal: choose and expose the right built-in endpoints once the `management` dependency is on the project.

## Enabled by default

| URI | Purpose |
|---|---|
| `/beans` | loaded bean definitions |
| `/health` | application health (see the health skill) |
| `/info` | static application info |
| `/loggers` | list loggers, change levels (the overview table lists it as enabled, but its own page says it is disabled by default and must be enabled with `endpoints.loggers.enabled=true`) |
| `/metrics` | metrics; needs `micrometer-core` configuration on the classpath |
| `/refresh` | refresh application state |
| `/routes` | URIs the app can serve |
| `/threaddump` | current threads |

## Disabled by default

`/env` (environment and property sources), `/caches` (list/invalidate caches; documented in the micronaut-cache project), `/stop` (shuts the server down).

Enable one with its own key, e.g. `endpoints.stop.enabled: true` (the stop page: disabled by default, must be explicitly enabled). Each endpoint is configured under `endpoints.<id>` with `enabled` and `sensitive` booleans (`beans`, `routes`, `threaddump`, `stop` share exactly that shape).

WARNING from the docs: `endpoints.all.sensitive: false` opens all endpoints to unauthenticated access and exposes private information; use with care.

## Separate management port

By default endpoints share the application port. To serve them only on another port:

```yaml
endpoints:
  all:
    port: 8085
```

## Notes per endpoint

- **beans**: GET `/beans` returns an object keyed by bean definition class name. Customize by replacing `BeanDefinitionDataCollector` / `BeanDefinitionData` (extend `DefaultBeanDefinitionDataCollector` / `DefaultBeanDefinitionData` or implement the interface) with `@Replaces`.
- **routes**: GET `/routes` returns URI, allowed method, produced content types and the method that would execute. Customize via `RouteDataCollector` / `RouteData` the same way.
- **threaddump**: GET `/threaddump`; delegates to a `ThreadInfoMapper` that transforms `java.lang.management.ThreadInfo` objects into whatever is serialized.
- **metrics**: GET `/metrics` lists metric names; `/metrics/[name]` such as `/metrics/jvm.memory.used` returns one. With the CLI, add a micrometer feature: `mn create-app my-app --features micrometer-atlas`.
- **stop**: POST `/stop`.
- Endpoints can also be registered with JMX (see the JMX section of the guide).

## Checked
2026-11-07. Checked against the endpoint overview and per-endpoint pages (stop, loggers, caches). Reworded the /loggers row (overview lists it enabled, its page says disabled by default) and changed the enable example to endpoints.stop.enabled; added the loggers and caches pages to sources.

Method: documentation only; no commands were run.
