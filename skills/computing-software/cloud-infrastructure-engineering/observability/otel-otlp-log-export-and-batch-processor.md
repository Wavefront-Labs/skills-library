---
id: computing-software.cloud-infrastructure-engineering.observability.otel-otlp-log-export-and-batch-processor
name: otel-otlp-log-export-and-batch-processor
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otlp-log-exporter, batch-log-processor, otel-logs, logger-provider, opentelemetry-logs]
level: practitioner
status: docs-checked
description: "Export application logs over OTLP with the OpenTelemetry logs SDK: LoggerProvider, batch log record processor tuning (OTEL_BLRP_*), handlers and shutdown."
sources: ["https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor", "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-logrecord-processor", "https://opentelemetry.io/docs/languages/python/instrumentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTLP log export and the batch log record processor

## Python (stdlib logging bridged to OTel)
```python
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
provider = LoggerProvider(resource=resource)
provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
set_logger_provider(provider)
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=provider))
```
The `LoggingHandler` in `opentelemetry-sdk` is deprecated (it emits a DeprecationWarning pointing to the handler in
`opentelemetry-instrumentation-logging`), so the example imports the instrumentation package's handler. Zero-code: install
`opentelemetry-instrumentation-logging`; it installs the handler unless `OTEL_PYTHON_LOG_AUTO_INSTRUMENTATION` is `false`
(default true), and it skips installation if the deprecated `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true` is set. Java:
the agent's supported libraries include Logback and Log4j appender instrumentation, and the log exporter is chosen with
`otel.logs.exporter`.

## Batch processor settings (env)
| Variable | Default | Meaning |
|---|---|---|
| `OTEL_BLRP_SCHEDULE_DELAY` | 1000 ms | export interval |
| `OTEL_BLRP_MAX_QUEUE_SIZE` | 2048 | maximum queue size; after it is reached logs are dropped (spec) |
| `OTEL_BLRP_MAX_EXPORT_BATCH_SIZE` | 512 | records per export |
| `OTEL_BLRP_EXPORT_TIMEOUT` | 30000 ms | how long an export may run before it is cancelled |
The batch size must be less than or equal to the queue size. Raise the queue size for bursty logging, since logs beyond it are dropped.

## Shutdown
Call `provider.shutdown()` (or `force_flush()`) on exit, otherwise the last batch is lost; short-lived jobs especially.

## Design choice
OTLP logs from the SDK vs writing to stdout and collecting with filelog: SDK export carries trace context and structured attributes without parsing, while stdout collection needs parsing operators in the collector (see the filelog receiver skills). Choose per service; do not run both on the same output without deduplication.

## Gotchas
- Both a console handler and an OTLP handler produce duplicate records if a collector also tails stdout.

## Verify
- [ ] Logs arrive in the backend with `trace_id`/`span_id` and the service resource attributes.

## Checked

2026-10-24. OpenTelemetry specification logs SDK (batching processor, Shutdown/ForceFlush) and SDK environment variables, opentelemetry-python SDK source (`LoggingHandler` deprecation, `BatchLogRecordProcessor`, `LoggerProvider.add_log_record_processor`, OTLP log exporter module), opentelemetry-python-contrib logging instrumentation, and the Java agent supported-libraries list (main branch). Confirmed: BLRP defaults (1000 ms, 30000 ms, 2048, 512), drop-on-full-queue semantics, shutdown and force flush, the Python handler deprecation and the new handler import path, `OTEL_PYTHON_LOG_AUTO_INSTRUMENTATION` default, and the deprecated env variable. Removed unconfirmed claims about recursion guards, crash survival and Java default export behaviour.

Method: documentation only; no commands were run.
