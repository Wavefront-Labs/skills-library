---
id: computing-software.cloud-infrastructure-engineering.observability.injecting-trace-context-into-logs
name: injecting-trace-context-into-logs
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-trace-context-injection, log-correlation-config, otel-logs, signal-correlation, mdc]
level: practitioner
status: docs-checked
description: "Get trace_id and span_id into every log line: Java agent MDC injection, Python log correlation, Node pino/winston, .NET scopes, Go slog, and log patterns."
sources: ["https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/logger-mdc-instrumentation.md", "https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html", "https://opentelemetry.io/docs/specs/otel/compatibility/logging_trace_context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injecting trace context into logs

Logs only correlate with traces if each line carries `trace_id` and `span_id` (and ideally `trace_flags`). With an
OTel log bridge this is automatic in OTLP; for stdout/file logs you must put them into the text.

## Java (agent)
The agent injects `trace_id`, `span_id` and `trace_flags` into the MDC of Log4j 1 (1.2+), Log4j 2 (2.7+) and Logback (1.0+) events. Add to the pattern:
```xml
<pattern>%d{ISO8601} %-5level [%thread] %logger{36} trace_id=%X{trace_id} span_id=%X{span_id} - %msg%n</pattern>
```
Spring Boot with logback: override only `logging.pattern.level = trace_id=%mdc{trace_id} span_id=%mdc{span_id} trace_flags=%mdc{trace_flags} %5p`.
Without the agent use the standalone `opentelemetry-logback-mdc-1.0` (Logback) or `opentelemetry-log4j-context-data-2.17-autoconfigure` (Log4j 2) libraries. If the current span is invalid nothing is injected.

## Python
`OTEL_PYTHON_LOG_CORRELATION=true` (with `opentelemetry-instrument`) adds `otelTraceID`, `otelSpanID`,
`otelServiceName`, `otelTraceSampled` to every `LogRecord` and sets a default format; custom format:
`OTEL_PYTHON_LOG_FORMAT="%(asctime)s %(levelname)s trace_id=%(otelTraceID)s span_id=%(otelSpanID)s %(message)s"`.

## Other languages
Node (pino, winston), .NET (`ILogger` scopes) and Go (slog handlers) need their own instrumentation or bridge; use the field names below and check each SDK's documentation (not covered here).

## Format rules
- Use `trace_id`, `span_id`, `trace_flags` as field names, lowercase hex-encoded IDs, flags in W3C traceflags format.
- Field names consistent with your Loki derived field / Grafana correlation regex.
- All three fields are optional; lines outside any span can omit them, do not fabricate.

## Verify
Hit an endpoint, copy the trace ID from the log line, search it in Tempo; the trace exists (if sampled - check
`trace_flags=01`).

## Checked
Checked 2026-10-28 against the Java instrumentation MDC doc, the Python logging instrumentation docs and the OTel spec page "Trace Context in non-OTLP Log Formats" (Stable).
- Confirmed: MDC keys and supported libraries/versions, Spring Boot pattern, Python `OTEL_PYTHON_LOG_CORRELATION`, `OTEL_PYTHON_LOG_FORMAT`, `otelTraceID`/`otelSpanID`/`otelServiceName`/`otelTraceSampled`, field names and encoding rules.
- Removed: logstash default behaviour, the `-Dotel...logging.trace-id` rename flag, `OpenTelemetryAppender` class path, structlog snippet, Node, .NET and Go specifics, hex length figures.

Method: documentation only; no commands were run.
