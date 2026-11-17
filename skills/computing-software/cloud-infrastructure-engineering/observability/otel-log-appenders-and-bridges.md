---
id: computing-software.cloud-infrastructure-engineering.observability.otel-log-appenders-and-bridges
name: otel-log-appenders-and-bridges
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [logback-otel-appender, log4j-otel-appender, serilog-otel, otel-logs, logs-bridge]
level: practitioner
status: docs-checked
description: "Send existing application logs through OpenTelemetry: Logback and Log4j2 appenders, their capture settings and install step, plus .NET ILogger and Serilog."
sources: ["https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/main/instrumentation/logback/logback-appender-1.0/library", "https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/main/instrumentation/log4j/log4j-appender-2.17/library", "https://github.com/serilog/serilog-sinks-opentelemetry", "https://opentelemetry.io/docs/languages/dotnet/logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTel log appenders (bridges)

OTel does not replace your logging library; an **appender/bridge** forwards records from it into the OTel Logs SDK,
which adds resource attributes and trace context and exports them.

## Java: Logback (library module)
Dependency `io.opentelemetry.instrumentation:opentelemetry-logback-appender-1.0`:
```xml
<appender name="OpenTelemetry" class="io.opentelemetry.instrumentation.logback.appender.v1_0.OpenTelemetryAppender">
  <captureExperimentalAttributes>true</captureExperimentalAttributes>
  <mdcAttributesIncluded>request-*,user-?</mdcAttributesIncluded>
  <mdcAttributesExcluded>*-secret</mdcAttributesExcluded>
</appender>
<root level="INFO"><appender-ref ref="console"/><appender-ref ref="OpenTelemetry"/></root>
```
The appender needs an SDK instance set at startup: `OpenTelemetryAppender.install(openTelemetrySdk);`. Logs emitted before
install are cached and replayed; the cache size is `numLogsCapturedBeforeOtelInstall` (default 1000).

Settings (all default off or empty):
- `captureExperimentalAttributes` adds `thread.name` and `thread.id`; `captureCodeAttributes` adds source code attributes (may cost performance); `captureMarkerAttribute`, `captureTemplate` and `captureArguments` capture markers, message template and arguments.
- MDC keys are captured only when you configure `mdcAttributesIncluded` and/or `mdcAttributesExcluded` (case-sensitive globs; excluded wins). The older `captureMdcAttributes` is deprecated.
- Structured attributes (SLF4J key-value pairs, Logstash markers) are captured by default; filter them with `structuredAttributesIncluded` / `structuredAttributesExcluded`.
- Captured MDC and structured attributes can hold sensitive data, so list patterns explicitly.

Do not put the OpenTelemetry appender behind Logback's `AsyncAppender`: trace and span correlation is lost. Keep it on the logger directly, make the console or file appender async instead, and use the SDK's `BatchLogRecordProcessor` for asynchronous export.

## Java: Log4j2
Dependency `io.opentelemetry.instrumentation:opentelemetry-log4j-appender-2.17`; configure `<OpenTelemetry name="OpenTelemetryAppender"/>` in `<Appenders>` and reference it from the root logger. Install the SDK with the `OpenTelemetryAppender.install(openTelemetrySdk)` call from package `io.opentelemetry.instrumentation.log4j.appender.v2_17`. If a layout needs trace or span IDs, also add `opentelemetry-log4j-context-data-2.17-autoconfigure` and use `%X{trace_id}`, `%X{span_id}`, `%X{trace_flags}`.

## .NET
ILogger: `builder.AddOpenTelemetry(options => { /* add an exporter */ });` on the logging builder (the OTel docs show `options.AddConsoleExporter()`).

Serilog (package serilog-sinks-opentelemetry): `Log.Logger = new LoggerConfiguration().WriteTo.OpenTelemetry(options => { options.Endpoint = "http://127.0.0.1:4317"; options.ResourceAttributes = new Dictionary<string, object> { ["service.name"] = "checkout" }; }).CreateLogger();`. Defaults are endpoint `http://localhost:4317` and `OtlpProtocol.Grpc`.

## Gotchas
- Keep a console appender during rollout; if the exporter fails you still have logs.
- Do not also scrape the same logs from stdout with a file reader, or you ingest everything twice.

## Checked
Date: 2026-11-09. Confirmed in the Logback and Log4j2 appender READMEs (dependency names, class names, install call, settings table, MDC and structured attribute rules, async warning, replay cache), the Serilog sink README (WriteTo.OpenTelemetry, Endpoint, ResourceAttributes, defaults) and the OpenTelemetry .NET console logs getting-started page (AddOpenTelemetry on the logging builder). Removed as unconfirmed from the cited pages: Java agent -D flags, the Log4j packages attribute, .NET option names (IncludeFormattedMessage, IncludeScopes, ParseStateValues, AddOtlpExporter), and the Python, Node and Go bridge sections.
Method: docs-checked 2026-11-09 against the Logback and Log4j2 appender READMEs, the Serilog OpenTelemetry sink README and the OpenTelemetry .NET logs getting-started pages.
