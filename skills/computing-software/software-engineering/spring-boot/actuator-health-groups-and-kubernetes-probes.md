---
id: computing-software.software-engineering.spring-boot.actuator-health-groups-and-kubernetes-probes
name: actuator-health-groups-and-kubernetes-probes
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, health-groups, kubernetes, liveness, readiness, probes, additional-path]
level: practitioner
status: docs-checked
description: "Define health groups, extra paths such as /healthz, and Kubernetes liveness and readiness probes with their lifecycle states and external-system guidance."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Groups: `management.endpoint.health.group.<name>.include` / `.exclude` list indicator IDs.
```yaml
management:
  endpoint:
    health:
      group:
        custom:
          include: "db"
```
Check `http://localhost:8080/actuator/health/custom`. Startup fails if a group names a nonexistent indicator unless `management.endpoint.health.validate-group-membership` is `false`. Groups inherit the system `StatusAggregator` and `HttpCodeStatusMapper`; override per group with `status.order`, `status.http-mapping`, `show-details`, `roles`. Use `@Qualifier("groupname")` for per-group custom beans. Include a composite component by qualified name: `management.endpoint.health.group.custom.include="test/primary"`, `exclude="test/primary/b"`.

Extra path: `management.endpoint.health.group.live.additional-path="server:/healthz"` exposes the group on the main port. Prefix is mandatory: `server:` (main port) or `management:` (management port).

Kubernetes probes: Boot manages Application Availability; `LivenessStateHealthIndicator` and `ReadinessStateHealthIndicator` appear on `/actuator/health`, and as groups at `/actuator/health/liveness` and `/actuator/health/readiness` (automatic; disable with `management.endpoint.health.probes.enabled`).
```yaml
livenessProbe:
  httpGet:
    path: "/actuator/health/liveness"
    port: <actuator-port>
readinessProbe:
  httpGet:
    path: "/actuator/health/readiness"
    port: <actuator-port>
```
`<actuator-port>` is the main port, or the management port if `management.server.port` is set. With a separate management context, probes could pass while the main app is broken; set `management.endpoint.health.probes.add-additional-paths=true` to expose `/livez` and `/readyz` on the main port. If startup outlasts the liveness period consider a `startupProbe` using the liveness HTTP probe (readiness already fails until startup completes).

External state: add indicators to a probe group, for example `readiness: include: "readinessState,customCheck"`; Boot adds none by default. Liveness should not depend on external systems (a failure could make Kubernetes restart all instances in a cascade). For readiness it is a judgement call: shared external systems you include take instances out of service when they fail. If all instances are unready, `ClusterIP`/`NodePort` services accept no connections (no 503); load balancer and ingress behaviour depends on implementation (503 likely).

Lifecycle: starting = Liveness `BROKEN`, Readiness `REFUSING_TRAFFIC`, HTTP server not started; started (context refreshed, running startup tasks) = `CORRECT` / `REFUSING_TRAFFIC`, refuses requests; ready = `CORRECT` / `ACCEPTING_TRAFFIC`. On shutdown: running = `CORRECT` / `ACCEPTING_TRAFFIC`; graceful shutdown = `CORRECT` / `REFUSING_TRAFFIC`, new requests rejected, and HTTP probes stop accepting traffic too; then the server is shut down. See the Kubernetes container-lifecycle how-to for the `preStop` hook.

## Checked

2026-11-07

Read endpoints.adoc in full (cited Actuator endpoints page); used Health Groups, Kubernetes Probes, Checking External State With Kubernetes Probes and Application Lifecycle and Probe States.
Confirmed: group include/exclude and the /actuator/health/custom URL; validate-group-membership; per-group StatusAggregator/HttpCodeStatusMapper, show-details, roles, status overrides; @Qualifier("groupname"); composite component include/exclude by qualified name; additional-path with mandatory `server:` or `management:` prefix; liveness/readiness indicators and /actuator/health/liveness and /readiness groups, probes.enabled; the probe YAML and the <actuator-port> note; add-additional-paths giving /livez and /readyz; startupProbe advice; readiness include example and "no other indicators by default"; liveness-must-not-check-external-systems; ClusterIP/NodePort/LoadBalancer/ingress behaviour when all instances are unready; both lifecycle tables (BROKEN/CORRECT, REFUSING_TRAFFIC/ACCEPTING_TRAFFIC); preStop hook pointer.
Nothing trimmed.

Method: documentation only; no commands were run.
