---
id: computing-software.software-engineering.quarkus.quarkus-health-checks
name: quarkus-health-checks
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, health, liveness, readiness, startup, smallrye-health, microprofile]
level: intro
status: docs-checked
description: "Add liveness, readiness and startup health checks to a Quarkus app with smallrye-health, including DOWN states, data and reactive checks."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/smallrye-health.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus health checks with SmallRye Health

Add the `quarkus-smallrye-health` extension (`smallrye-health`; Maven dependency `io.quarkus:quarkus-smallrye-health`). It implements MicroProfile Health and exposes endpoints immediately.

## Endpoints

- `/q/health/live` - application is up and running
- `/q/health/ready` - application is ready to serve requests
- `/q/health/started` - application is started
- `/q/health/well` - checks annotated `@Wellness`
- `/q/health/group` and `/q/health/group/<name>` - checks annotated `@HealthGroup("<name>")`
- `/q/health` - all checks together

Each returns JSON with `status` (logical AND of all checks) and a `checks` array. It is empty until you define checks.

## Define a check

A check is a CDI bean implementing `HealthCheck` and carrying a qualifier: `@Liveness`, `@Readiness` or `@Startup`.

```java
@Liveness
@ApplicationScoped
public class SimpleHealthCheck implements HealthCheck {
    @Override
    public HealthCheckResponse call() {
        return HealthCheckResponse.up("Simple health check");
    }
}
```

Use `@ApplicationScoped` or `@Singleton` so one instance serves all requests; a bean with a health annotation and no scope becomes `@Singleton`.

## DOWN state and data

Use the full builder when the result varies:

```java
HealthCheckResponseBuilder b = HealthCheckResponse.named("Database connection health check");
try { verify(); b.up(); }
catch (IllegalStateException e) { b.down().withData("error", e.getMessage()); }
return b.build();
```

`withData(key, value)` adds a `data` JSON object to that check. `HealthCheckResponse.up(String)` / `down(String)` are shortcuts.

## Semantics

- Liveness decides whether the app should be restarted; readiness decides whether it should get requests. A DOWN readiness check does not change `/q/health/live`.
- Startup checks delay liveness probes for slow-starting containers (the page says it should not be needed in Quarkus).

## Gotchas

- Import `org.eclipse.microprofile.health.Startup`, not `io.quarkus.runtime.Startup`; the names clash.
- Reactive checks: implement `io.smallrye.health.api.AsyncHealthCheck` returning `Uni<HealthCheckResponse>`.
- Extensions may register their own checks (for example the datasource readiness check); disable them with `quarkus.smallrye-health.extensions.enabled`.
- To serve health on a separate port, set the build-time property `quarkus.management.enabled=true`; the default is then `http://0.0.0.0:9000/q/health`, with the path set by `quarkus.smallrye-health.root-path`.

Verify: after adding a `@Liveness` check in dev mode, `curl http://localhost:8080/q/health/live` lists it in the `checks` array.

## Checked

2026-11-07. Read in full: smallrye-health.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the `quarkus extension add smallrye-health` command form (shown only through an include).

Method: documentation only; no commands were run.
