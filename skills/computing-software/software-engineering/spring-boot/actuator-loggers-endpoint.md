---
id: computing-software.software-engineering.spring-boot.actuator-loggers-endpoint
name: actuator-loggers-endpoint
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, loggers, log-levels, opentelemetry, otlp, runtime-configuration]
level: practitioner
status: docs-checked
description: "View and change log levels at runtime through the Actuator loggers endpoint, reset a level with null, and export logs through OpenTelemetry."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/loggers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `loggers` endpoint views and configures log levels at runtime, for the whole list or one logger. Each entry shows the explicitly configured level and the effective level from the logging framework. Levels: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, `OFF`, `null` (no explicit configuration).

Configure a logger by `POST`ing a partial entity to its URI:
```json
{
	"configuredLevel": "DEBUG"
}
```
Pass `null` as `configuredLevel` to reset to the default configuration.

Note: `POST` to loggers needs CSRF handling under default Spring Security (see actuator-endpoint-security), and the endpoint must be exposed (see actuator-endpoint-access-and-exposure).

OpenTelemetry logging is not configured by default. Provide the OTLP logs endpoint:
```yaml
management:
  opentelemetry:
    logging:
      export:
        otlp:
          endpoint: "https://otlp.example.com:4318/v1/logs"
```
- `management.opentelemetry.logging.export.*` configures the `BatchLogRecordProcessor`, for example `schedule-delay: "15s"`.
- `management.opentelemetry.logging.limits.*` sets record limits, for example `max-attributes: 64`, `max-attribute-value-length: 256`; register a `LogLimits` bean for full control.
- The OpenTelemetry Logback and Log4j appenders are not part of Spring Boot. Configure the appender in `logback-spring.xml` or `log4j2-spring.xml`; `OpenTelemetryAppender` needs an `OpenTelemetry` instance set programmatically at startup.

## Checked

2026-11-07

Read loggers.adoc (docs-repo source of the cited Loggers page) in full, and endpoints.adoc for the CSRF/POST and exposure cross-references in the Note. The OpenTelemetryAppenderInitializer include example was not opened; the "set programmatically at startup" claim rests on the page prose.
Confirmed: view all or one logger with configured and effective level; level list TRACE, DEBUG, INFO, WARN, ERROR, FATAL, OFF, null (null = no explicit configuration); POST of a partial entity with configuredLevel and null to reset; OpenTelemetry logging not configured by default and the management.opentelemetry.logging.export.otlp.endpoint example; export.* configuring BatchLogRecordProcessor with schedule-delay "15s"; limits.* with max-attributes 64 and max-attribute-value-length 256; custom LogLimits bean; Logback/Log4j appenders not part of Spring Boot, configured in logback-spring.xml or log4j2-spring.xml; OpenTelemetryAppender needing an OpenTelemetry instance set programmatically.
Nothing trimmed.

Method: documentation only; no commands were run.
