---
id: computing-software.software-engineering.java.spring-boot-services
name: spring-boot-services
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, configuration, profiles, actuator, health-probes, kubernetes, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Spring Boot service essentials from the reference docs: configtree imports, actuator exposure, Kubernetes liveness and readiness groups, and graceful shutdown."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
  - https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html
  - https://docs.spring.io/spring-boot/how-to/data-initialization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Boot services

**Goal:** a Spring Boot service with honest health probes, a locked-down actuator, clean shutdown and sane config sources.

## Configuration
- Property sources are layered; command line arguments are the highest-priority source in the documented order. See the "Externalized Configuration" page for the full list before relying on precedence.
- Mounted secret or config directories can be read as properties with a config tree import: `spring.config.import=optional:configtree:/etc/config/` (exposes all the files in the directory as properties). Use the `configtree:` prefix; a plain import is for YAML or properties files.

## Actuator exposure
- Over HTTP only the health endpoint is exposed by default. Choose what to expose with `management.endpoints.web.exposure.include` and make sure exposed endpoints hold nothing sensitive, are behind a firewall or are secured (for example with Spring Security).
- Access to all endpoints except `shutdown` and `heapdump` is unrestricted by default; change access per endpoint with `management.endpoint.<id>.access`.
- `management.endpoint.health.show-details` and `show-components` control how much the health endpoint reveals.
- A separate management port is available through `management.server.port`.

## Kubernetes probes
- Liveness and readiness are health groups, available at `/actuator/health/liveness` and `/actuator/health/readiness`; they are enabled automatically and can be disabled with `management.endpoint.health.probes.enabled`.
- The liveness probe should not depend on health checks of external systems (database, web API, cache): if one fails, Kubernetes could restart every instance and cause cascading failures.
- Add checks to a group with include properties, for example `management.endpoint.health.group.readiness.include=readinessState,customCheck`.

## Graceful shutdown
Enabled by default with Jetty, Reactor Netty and Tomcat (servlet and reactive). It runs while the application context closes, with a timeout giving existing requests a grace period while new requests are refused. Disable it with the `server.shutdown` property. An IDE stop may be immediate if it does not send a proper SIGTERM.

## Schema management
When using Flyway or Liquibase, use them alone to create and initialize the schema; combining the basic `schema.sql` and `data.sql` scripts with them is not recommended.

## Verify
- [ ] Only the intended actuator endpoints are exposed, on the intended port.
- [ ] Liveness has no external dependency checks; readiness includes what the service needs to serve traffic.
- [ ] The pod receives SIGTERM and drains requests.

## Checked
2026-11-01. Confirmed against the Spring Boot reference pages Externalized Configuration, Actuator Endpoints and Graceful Shutdown, and the data-initialization how-to. Removed as unconfirmed by those pages: Java and Boot version claims, ConfigurationProperties code, YAML snippets with specific timeouts, Micrometer and Prometheus setup, test slice and Testcontainers advice, JVM container flags, and the gotchas list.
Method: documentation only; no commands were run.
