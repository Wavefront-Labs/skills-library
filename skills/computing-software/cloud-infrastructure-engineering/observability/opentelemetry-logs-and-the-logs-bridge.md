---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-logs-and-the-logs-bridge
name: opentelemetry-logs-and-the-logs-bridge
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel, otel-logs, opentelemetry-logs, logs-bridge, logs-bridge-api, log-appender, logback-appender, log4j-appender, python-logging-handler, otelslog, winston-transport, ilogger, log-record, severity-number, body, attributes, resource, otlp-logs, filelog-receiver, log-data-model, trace-context-in-logs, batch-log-record-processor, collector-logs-pipeline, loki-exporter, otlphttp-loki]
level: advanced
status: gated
description: "Get logs into OpenTelemetry the two sanctioned ways: the Logs Bridge (SDK appenders for logback/log4j/python logging/slog/winston/ILogger) with trace context."
sources: ["https://opentelemetry.io/docs/concepts/signals/logs/", "https://opentelemetry.io/docs/specs/otel/logs/data-model/", "https://opentelemetry.io/docs/specs/otel/logs/bridge-api/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver", "https://grafana.com/docs/loki/latest/send-data/otel/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenTelemetry logs and the Logs Bridge

**Goal:** application logs arrive as OTLP log records that carry resource attributes,
severity, structured attributes and the active trace/span ids, through the same Collector
pipeline as traces and metrics, to whatever backend you run.

## 1. The design: no new logging API
OTel deliberately does not ask developers to call a new logger. Two paths:
1. **Logs Bridge** (in-process): an appender/handler for the language's existing logging
   framework converts each record to an OTel `LogRecord` and hands it to the SDK's
   `LoggerProvider` → `BatchLogRecordProcessor` → OTLP exporter. Trace context is attached
   automatically from the current span.
2. **Collector-side** (out of process): the app writes files/stdout as before; the
   Collector's `filelog` receiver (or `journald`, `syslog` and similar receivers)
   parses them into log records. No trace ids unless the app already prints them and a
   parser extracts them.
Use 1 for your services, 2 for third-party/legacy; both can coexist.

## 2. The log data model (what a record is)
`Timestamp`, `ObservedTimestamp`, `TraceId`, `SpanId`, `TraceFlags`, `SeverityText` (`WARN`),
`SeverityNumber` (1–24; `INFO`=9, `WARN`=13, `ERROR`=17, `FATAL`=21), `Body` (string or
structured any-value), `Attributes` (key/values; semconv `exception.type`, `exception.message`,
`exception.stacktrace`, `log.file.path`), `Resource` (shared with traces:
`service.name`, `k8s.pod.name`…), `InstrumentationScope` (logger name). Backends map these:
Loki → labels from resource attrs (allow-listed), structured metadata from the rest;
Elastic → its own mapping modes (see section 5); other vendors map to their own fields.

## 3. Bridge setup per language
**Java (logback)**
```xml
<appender name="OTEL" class="io.opentelemetry.instrumentation.logback.appender.v1_0.OpenTelemetryAppender">
  <captureExperimentalAttributes>true</captureExperimentalAttributes>
  <captureMdcAttributes>*</captureMdcAttributes>
  <captureCodeAttributes>true</captureCodeAttributes>
</appender>
<root level="INFO"><appender-ref ref="OTEL"/><appender-ref ref="CONSOLE"/></root>
```
`OpenTelemetryAppender.install(openTelemetry)` at startup (the Java agent does this when
`-Dotel.logs.exporter=otlp`; also `otel.instrumentation.logback-appender.experimental-log-attributes=true`).
Keep a console appender during rollout.

**Python**
```python
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
provider = LoggerProvider(resource=resource); set_logger_provider(provider)
provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=provider))
```
Or zero-code: `opentelemetry-instrument` with `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true`, `OTEL_LOGS_EXPORTER=otlp`.

**Go** `otelslog`: `logger := otelslog.NewLogger("checkout")` (bridge for `log/slog`), or `otelzap`, `otellogrus`.
**Node** `@opentelemetry/winston-transport` / `pino` via `@opentelemetry/instrumentation-pino` (adds trace ids and, optionally, sends records).
**.NET** `builder.Logging.AddOpenTelemetry(o => { o.IncludeScopes = true; o.ParseStateValues = true; o.AddOtlpExporter(); })`.

Env: `OTEL_LOGS_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`, `OTEL_BLRP_SCHEDULE_DELAY=1000`,
`OTEL_BLRP_MAX_QUEUE_SIZE=2048`, `OTEL_BLRP_MAX_EXPORT_BATCH_SIZE=512`.

## 4. Collector-side parsing (filelog)
```yaml
receivers:
  filelog:
    include: [/var/log/pods/*/*/*.log]
    exclude: [/var/log/pods/*/otel-collector/*.log]
    start_at: end
    include_file_path: true
    storage: file_storage           # checkpoints; add extensions.file_storage
    operators:
      - type: container             # parses CRI/docker formats + k8s attrs from path (newer contrib)
      - type: recombine             # multiline stack traces
        combine_field: body
        is_first_entry: body matches "^\\d{4}-\\d{2}-\\d{2}"
      - type: json_parser
        if: body matches "^\\{"
        parse_from: body
        timestamp: { parse_from: attributes.ts, layout: "%Y-%m-%dT%H:%M:%S.%fZ" }
        severity: { parse_from: attributes.level }
        trace: { trace_id: { parse_from: attributes.trace_id }, span_id: { parse_from: attributes.span_id } }
      - type: move
        from: attributes.message
        to: body
processors:
  k8sattributes: { extract: { metadata: [k8s.namespace.name, k8s.pod.name, k8s.deployment.name], labels: [{ tag_name: app, key: app.kubernetes.io/name, from: pod }] } }
  resource/service: { attributes: [{ key: service.name, from_attribute: app, action: insert }] }
  batch: {}
exporters:
  otlphttp/loki: { endpoint: http://loki-gateway/otlp, headers: { X-Scope-OrgID: team-payments } }
service:
  pipelines:
    logs: { receivers: [filelog, otlp], processors: [k8sattributes, resource/service, batch], exporters: [otlphttp/loki] }
```
Operators run in order; `regex_parser`, `syslog_parser`, `severity_parser`, `time_parser`,
`add`, `remove`, `copy`, `filter`, `router` cover most formats. The deprecated `loki` exporter
is replaced by Loki's native OTLP endpoint (`/otlp`).

## 5. Backend mapping notes
- **Loki OTLP**: resource attributes in `default_resource_attributes_as_index_labels`
  (a default list that includes service.name, service.namespace and deployment.environment.name) become index labels;
  the remaining attributes are stored as structured metadata (default limits per line: 64KB and 128 entries);
  `Body` is the line. Override the list with `default_resource_attributes_as_index_labels` under the distributor's
  `otlp_config` to keep stream counts low.
- **Elastic**: the `elasticsearch` exporter defaults to the `otel` mapping mode, which keeps the OTel model; the config-file `mapping::mode` setting is deprecated in favour of the `X-Elastic-Mapping-Mode` client metadata key or the `elastic.mapping.mode` scope attribute.
- **Cloud vendors** have native OTLP log endpoints; check severity mapping (`SeverityNumber` → vendor status).

## Gotchas
- Logging frameworks' own formatters do not apply to the bridge: the `Body` is the raw
  message (plus structured args), not your `%d [%t] %-5level` line. That is a feature.
- Double shipping during rollout (bridge + filelog on stdout) doubles volume; disable one
  per service deliberately.
- `BatchLogRecordProcessor` drops records when its queue is full (default `OTEL_BLRP_MAX_QUEUE_SIZE` is 2048) — raise the queue or export more often for chatty services.
- Exceptions: ensure `exception.stacktrace` is an attribute (Java appender does; Python needs
  `exc_info=True`), otherwise traces of errors lose the stack.
- Severity text varies (`WARNING` vs `WARN`); map it to `SeverityNumber` in the Collector (stanza `severity` parsing) so backends filter consistently.

## Verify
- [ ] A log line emitted inside a traced request shows `trace_id`/`span_id` in the backend and the trace view's "logs for this span" finds it.
- [ ] `debug` exporter (`verbosity: detailed`) on the logs pipeline prints `SeverityNumber`, `Body`, resource `service.name` for a sample record.
- [ ] Stack traces arrive as single records; multiline recombine shows no split fragments.
- [ ] Loki stream count for the tenant is unchanged after enabling OTLP logs (labels allow-listed).

## Checked

- Date: 2026-11-02.
- Confirmed against: LoggerProvider and the Logs Bridge API concepts, BatchLogRecordProcessor, filelog receiver options include_file_path, start_at, json_parser, parse_from (OpenTelemetry signals/logs, bridge-api, SDK environment variable and filelogreceiver pages).
- Not confirmed: language-specific appender and handler class and option names (logback appender, captureMdcAttributes, Python LoggingHandler) and the exact filelog operator chains, which the fetched pages do not state (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
