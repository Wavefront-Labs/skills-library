---
id: computing-software.software-engineering.quarkus.quarkus-logging-json-mdc
name: quarkus-logging-json-mdc
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, logging, json, mdc, ecs, structured-logs, access-log]
level: advanced
status: docs-checked
description: "Emit structured JSON logs in Quarkus with quarkus-logging-json: formats (default, ecs, gcp), MDC fields, access-log fields and custom JsonProvider fields."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/logging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured JSON logging and MDC in Quarkus

Add `io.quarkus:quarkus-logging-json`. It overrides the console format: format strings and color settings are ignored, while level and async settings still apply.

## Dev text, prod JSON

```properties
%dev.quarkus.log.console.json.enabled=false
%test.quarkus.log.console.json.enabled=false
```

## Choose a format

Set `quarkus.log.console.json.log-format` to one of:

- `default`: key/value structured logs; MDC and NDC appear under `mdc` and `ndc`.
- `ecs`: Elastic Common Schema (`@timestamp`, `log.level`, `log.logger`, `service.name`, ...). MDC stays in the non-ECS `mdc` field.
- `gcp`: follows default; `exception-output-type` DETAILED is upgraded to DETAILED_AND_FORMATTED so stack traces land in `stack_trace`. With OpenTelemetry, tracing data is copied to `spanId`, `traceSampled` and `trace`, where `trace` is `projects/<quarkus.application.name>/traces/...`.

## MDC options

- `quarkus.log.console.json.mdc.flat-fields=true` writes MDC entries as root-level fields (useful for OpenSearch/Elasticsearch queries).
- `quarkus.log.console.json.mdc.key-overrides.<mdc-key>=<field-name>` renames entries, e.g. `traceId=TraceId`.
- Add `mdc` to `excluded-keys` to drop it.
- The same options exist for `file`, `syslog`, `socket` and named handlers (`quarkus.log.handler.console.<name>.json...`).

## Set MDC values

Use `org.jboss.logmanager.MDC.put("request.id", id)` (Log4j 2: `ThreadContext.put`; SLF4J: `org.slf4j.MDC.put`). Print in text logs with `%X{request.id}`. Quarkus propagates MDC after async calls such as a REST client returning a `Uni`, in `ManagedExecutor` code and in `vertx.executeBlocking()`.

## Structured access log

`quarkus.log.console.json.access-log.structured=true` adds an `accessLog` object (`method`, `uri`, `status`, `responseTimeMs`, `bytesSent`, `remoteIp`, `protocol`) to records from the `io.quarkus.http.access-log` logger, active when `quarkus.http.access-log.enabled=true`. With `log-format=ecs` these become top-level ECS fields such as `http.request.method` and `url.path`.

## Custom fields: JsonProvider

Implement `io.quarkus.logging.json.runtime.JsonProvider` and its `writeTo(JsonLogGenerator generator, ExtLogRecord record)`; call `generator.add("environment", "production")` or `startObject(...)...endObject()`. Register it as a CDI bean (preferred) or via `META-INF/services/io.quarkus.logging.json.runtime.JsonProvider`. ServiceLoader providers run first in file order; CDI beans run afterwards in unspecified order. Keys in `excluded-keys` are still filtered.

## Gotchas

- Pretty printing can break some processors and parsers.
- Printing caller details (class, file, method, line) can be expensive.

## Checked

2026-11-07. Read in full: logging.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
