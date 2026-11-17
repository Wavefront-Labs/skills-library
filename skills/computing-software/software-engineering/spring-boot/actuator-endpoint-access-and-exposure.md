---
id: computing-software.software-engineering.spring-boot.actuator-endpoint-access-and-exposure
name: actuator-endpoint-access-and-exposure
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, endpoints, exposure, access, management-endpoints-web-exposure-include]
level: practitioner
status: docs-checked
description: "Control which Actuator endpoints are accessible and which are exposed over HTTP or JMX with management.endpoint.<id>.access and exposure include/exclude."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An endpoint is available when access is permitted and it is exposed. Built-in endpoints are auto-configured only when available. Over HTTP the URL is `/actuator/<id>`; by default only `health` is exposed over HTTP and JMX.

Access: all endpoints except `shutdown` and `heapdump` are unrestricted by default. Set `management.endpoint.<id>.access` (for example `unrestricted`, `read-only`, `none`):
```yaml
management:
  endpoint:
    shutdown:
      access: unrestricted
```
Opt-in style: `management.endpoints.access.default: none`, then per-endpoint access, for example `loggers: access: read-only`. Inaccessible endpoints are removed from the application context. `management.endpoints.access.max-permitted` limits application-wide and takes precedence over default and per-endpoint access (`none` = all inaccessible, `read-only` = read only). Read access means `@ReadOperation` methods (or `GET`/`HEAD` mappings for controller and servlet endpoints).

Exposure properties (defaults: `health` for both include properties, empty exclude):
- `management.endpoints.web.exposure.include` / `.exclude`
- `management.endpoints.jmx.exposure.include` / `.exclude`

`exclude` wins over `include`. `*` selects all; quote it in YAML.
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
        exclude: "env,beans"
```
Register an `EndpointFilter` bean for a custom exposure strategy. Expose publicly only if also secured (see actuator-endpoint-security).

Endpoint IDs include: `auditevents`, `beans`, `caches`, `conditions`, `configprops`, `env`, `flyway`, `health`, `httpexchanges`, `info`, `integrationgraph`, `loggers`, `liquibase`, `metrics`, `mappings`, `quartz`, `scheduledtasks`, `sessions`, `shutdown` (jar packaging only, disabled by default), `startup` (needs `BufferingApplicationStartup`), `threaddump`. Web apps add `heapdump`, `logfile` (needs `logging.file.name` or `logging.file.path`), `prometheus` (needs `micrometer-registry-prometheus`).

A discovery page lists endpoint links at `/actuator`; disable with `management.endpoints.web.discovery.enabled: false`. With a custom management context path it moves to that root; with path `/` it is disabled.

## Checked

2026-11-07

Read endpoints.adoc in full (cited Actuator endpoints page); used the endpoint tables, Controlling Access, Limiting Access, Exposing Endpoints, Hypermedia and Security-intro sections.
Confirmed: available = access permitted and exposed; /actuator/<id>; only health exposed by default over HTTP and JMX (include default `health`, exclude empty); all endpoints except shutdown and heapdump unrestricted by default; management.endpoint.<id>.access with unrestricted / read-only; management.endpoints.access.default=none opt-in example; inaccessible endpoints removed from the context; management.endpoints.access.max-permitted semantics; read-access definition per endpoint type; exclude beats include; `*` and YAML quoting; EndpointFilter tip; every endpoint ID listed, with shutdown (jar packaging, disabled by default), startup (BufferingApplicationStartup), logfile (logging.file.name or logging.file.path), prometheus (micrometer-registry-prometheus) prerequisites; discovery page behaviour on /actuator and under a custom management path.
Nothing trimmed.

Method: documentation only; no commands were run.
