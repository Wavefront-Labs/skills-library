---
id: computing-software.cloud-infrastructure-engineering.observability.log-level-policy-and-dynamic-levels
name: log-level-policy-and-dynamic-levels
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-level-policy, dynamic-log-level, structured-logging, log-levels, runtime-configuration]
level: practitioner
status: draft
description: "Define what each log level means, the production default, and how to change levels at runtime without restarts (Spring actuator, Logback/Log4j reload, env-driven, OTel severity)."
sources: ["https://docs.spring.io/spring-boot/reference/actuator/loggers.html", "https://logging.apache.org/log4j/2.x/manual/configuration.html", "https://opentelemetry.io/docs/specs/otel/logs/data-model/#field-severitynumber"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log level policy and dynamic level changes

## Policy (write this down for every team)
| Level | Meaning | Who reads it |
|---|---|---|
| ERROR | Operation failed and needs attention; request/job could not complete | alerts via counters, on-call |
| WARN | Unexpected but handled (fallback, retry succeeded, degraded) | dashboards, trend review |
| INFO | Lifecycle and business events (startup, config loaded, job done, one canonical line per request) | investigation |
| DEBUG | Diagnostic detail for developers | off in prod, on on demand |
| TRACE | Very fine-grained, payloads | never in prod by default |

Production default: INFO for your code, WARN for chatty third-party packages. Do not log ERROR for client
mistakes (4xx) - that is INFO/WARN; reserve ERROR for things you would fix.

## Runtime changes without restart
- **Spring Boot**: `POST /actuator/loggers/com.acme.payments` body `{"configuredLevel":"DEBUG"}`; reset with
  `{"configuredLevel":null}`. Protect the endpoint (management port, auth).
- **Logback**: `<configuration scan="true" scanPeriod="30 seconds">` reloads the file (mount via ConfigMap).
- **Log4j2**: `monitorInterval="30"` on `<Configuration>`; or `Configurator.setLevel("com.acme", Level.DEBUG)`.
- **Go zap**: `zap.NewAtomicLevel()` exposes `ServeHTTP` (GET/PUT `{"level":"debug"}`).
- **Python**: expose an admin endpoint calling `logging.getLogger("acme").setLevel(logging.DEBUG)`.
- **.NET**: `appsettings.json` with `reloadOnChange: true` and `Logging:LogLevel` keys.
- Feature-flag driven: level per tenant/request (`X-Debug-Log: 1` header honoured only from internal callers).

## Safe debugging in prod
Time-box: set DEBUG with an automatic revert (a job that resets after 30 min) and narrow the logger name.
Watch ingest volume while it is on.

## Mapping to OTel severity
TRACE 1-4, DEBUG 5-8, INFO 9-12, WARN 13-16, ERROR 17-20, FATAL 21-24 (`severity_number`). Filter downstream on
the number, not the text.
