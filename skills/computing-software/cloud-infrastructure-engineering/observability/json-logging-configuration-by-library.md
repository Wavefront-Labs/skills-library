---
id: computing-software.cloud-infrastructure-engineering.observability.json-logging-configuration-by-library
name: json-logging-configuration-by-library
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [json-logging-config, structlog, zap-logger, pino-logger, logback, structured-logging, logging]
level: practitioner
status: draft
description: "Configure JSON structured logging in logback (logstash encoder), Go zap/slog, Python structlog and Node pino with consistent field names and timestamps."
sources: ["https://github.com/logfellow/logstash-logback-encoder", "https://pkg.go.dev/log/slog", "https://www.structlog.org/en/stable/", "https://getpino.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JSON logging configuration by library

Agree field names once: `timestamp` (RFC3339 UTC), `level`, `message`, `logger`, `trace_id`, `span_id`, `service.name`, `error.type`, `error.message`, `error.stack_trace`.

## Java logback (logstash-logback-encoder)
```xml
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
  <encoder class="net.logstash.logback.encoder.LogstashEncoder">
    <fieldNames><timestamp>timestamp</timestamp><version>[ignore]</version></fieldNames>
    <includeMdcKeyName>trace_id</includeMdcKeyName>
    <includeMdcKeyName>span_id</includeMdcKeyName>
  </encoder>
</appender>
```
Spring Boot 3.4+: `logging.structured.format.console=ecs` (or `logstash`, `gelf`) with no extra dependency.

## Go
slog (stdlib): `logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))`.
zap: `zap.NewProduction()` emits JSON with `ts` epoch floats; set `cfg.EncoderConfig.TimeKey = "timestamp"` and `EncodeTime = zapcore.ISO8601TimeEncoder` to match the schema.

## Python structlog
```python
structlog.configure(processors=[
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
    structlog.processors.dict_tracebacks,
    structlog.processors.JSONRenderer(),
])
```
Route stdlib `logging` through structlog's `ProcessorFormatter` so third-party libraries also emit JSON.

## Node pino
```js
const logger = require('pino')({ timestamp: pino.stdTimeFunctions.isoTime, messageKey: 'message',
  formatters: { level: (label) => ({ level: label }) } });
```
pino defaults to numeric levels and `msg`; the options above align it.

## Gotchas
- Multi-line stack traces break line-based shippers; JSON-encode them into one field.
- Logging to files inside containers: log to stdout and let the runtime/agent collect.
- Two libraries in one process (app + framework) with different formats: bridge to one.

## Verify
- [ ] `kubectl logs <pod> | head | jq .` parses every line.
- [ ] Field names match across Java, Go, Python and Node services in a Loki/ES query.
