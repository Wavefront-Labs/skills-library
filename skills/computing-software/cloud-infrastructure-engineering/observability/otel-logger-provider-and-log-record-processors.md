---
id: computing-software.cloud-infrastructure-engineering.observability.otel-logger-provider-and-log-record-processors
name: otel-logger-provider-and-log-record-processors
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [logger-provider, log-record-processor, otel-logs, otel-sdk, batch-processor]
level: advanced
status: docs-checked
description: "Configure the OTel Logs SDK: LoggerProvider setup, batch vs simple LogRecordProcessor, OTEL_BLRP_* tuning, custom processors for enrichment and filtering, limits and shutdown."
sources: ["https://opentelemetry.io/docs/specs/otel/logs/sdk/", "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-logrecord-processor", "https://opentelemetry.io/docs/languages/java/sdk/#sdkloggerprovider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoggerProvider and LogRecordProcessor

## Pipeline
`LoggerProvider` (resource + processors + limits) -> `LogRecordProcessor` (`onEmit`) -> `LogRecordExporter`.
Processors run in registration order; a batch processor ends the chain by exporting.

## Java
```java
SdkLoggerProvider lp = SdkLoggerProvider.builder()
    .setResource(resource)
    .addLogRecordProcessor(new AddTenantProcessor())                 // enrich first
    .addLogRecordProcessor(BatchLogRecordProcessor.builder(
        OtlpGrpcLogRecordExporter.builder().setEndpoint("http://collector:4317").build())
        .setScheduleDelay(Duration.ofSeconds(1)).setMaxQueueSize(4096).setMaxExportBatchSize(512).build())
    .setLogLimits(() -> LogLimits.builder().setMaxNumberOfAttributes(64).setMaxAttributeValueLength(4096).build())
    .build();
```
## Python
```python
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
lp = LoggerProvider(resource=resource); set_logger_provider(lp)
lp.add_log_record_processor(BatchLogRecordProcessor(exporter))   # exporter: your OTLP log exporter
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=lp))
```

## Env tuning (batch processor)
| Var | Default |
|---|---|
| `OTEL_BLRP_SCHEDULE_DELAY` | 1000 ms |
| `OTEL_BLRP_MAX_QUEUE_SIZE` | 2048 |
| `OTEL_BLRP_MAX_EXPORT_BATCH_SIZE` | 512 |
| `OTEL_BLRP_EXPORT_TIMEOUT` | 30000 ms |
| `OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT` / `_VALUE_LENGTH_LIMIT` | 128 / unlimited |

Queue full = records are dropped. Raise queue size for bursty error storms rather than shortening delay.

## Custom processors
- Enrichment: copy baggage or tenant from context into attributes in `onEmit` (records are mutable there).
- Filtering: wrap the batch processor and only forward records with `severity >= WARN` for a noisy logger.
- Simple processor (`SimpleLogRecordProcessor`) exports synchronously - use only for tests/console.

## Shutdown
Shut down (or flush) the provider on exit, or buffered records are lost. Manual setups must wire this themselves.

## Checked
- 2026-10-28. Checked against the SDK environment variables spec page and the OpenTelemetry Java and Python logs SDK pages.
- Confirmed: `OTEL_BLRP_SCHEDULE_DELAY` 1000, `OTEL_BLRP_MAX_QUEUE_SIZE` 2048, `OTEL_BLRP_EXPORT_TIMEOUT` 30000, `OTEL_LOGRECORD_ATTRIBUTE_VALUE_LENGTH_LIMIT` no limit, Java builder methods, Python `LoggerProvider`, `LoggingHandler`, `add_log_record_processor`.
- Removed (unconfirmed): `OTLPLogExporter` import path, `OTEL_LOGS_EXPORTER` default row, Java warn-once claim, shutdown-hook claims.
Method: documentation only; no commands were run.
