---
id: computing-software.software-engineering.spring-boot.structured-logging
name: structured-logging
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, structured-logging, json-logging, ecs, gelf, logstash, logging-structured-format]
level: practitioner
status: docs-checked
description: "Enable ECS, GELF or Logstash JSON logs with logging.structured.format.console or file, adjust fields and stack traces, and plug in a custom formatter."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot has built-in JSON structured logging formats: Elastic Common Schema (`ecs`), Graylog Extended Log Format (`gelf`) and `logstash`. Set the format id for console and/or file:
```yaml
logging:
  structured:
    format:
      console: ecs
      file: ecs
```
Every MDC key-value pair is added to the JSON. SLF4J fluent API `addKeyValue` also adds pairs. With Logstash, markers appear in a `tags` array.

If you use a custom log configuration, update it to respect the `CONSOLE_LOG_STRUCTURED_FORMAT` and `FILE_LOG_STRUCTURED_FORMAT` system properties (the page shows the console one). Logback: replace your encoder with `org.springframework.boot.logging.logback.StructuredLogEncoder` (using `${CONSOLE_LOG_STRUCTURED_FORMAT}` and `${CONSOLE_LOG_CHARSET}`). Log4j2: replace `PatternLayout` with `StructuredLogLayout`.

Format-specific fields:
- ECS: `logging.structured.ecs.service.name` (defaults to `spring.application.name`), `.version` (defaults to `spring.application.version`), `.environment`, `.node-name`.
- GELF: `logging.structured.gelf.host` (defaults to `spring.application.name`), `logging.structured.gelf.service.version`.

JSON customization: `logging.structured.json.include` / `exclude` filter paths, `rename` renames a member, `add` adds members. Example: `exclude: log.level`, `rename: {process.id: procid}`, `add: {corpname: mycorp}`. Advanced: `StructuredLoggingJsonMembersCustomizer` referenced by `logging.structured.json.customizer` or `META-INF/spring.factories`.

Stack traces: `logging.structured.json.stacktrace.root` (`last` or `first`), `max-length`, `max-throwable-depth`, `include-common-frames`, `include-hashes`, and `printer` (a `StackTracePrinter` class name, or `logging-system`).

Custom format: implement `StructuredLogFormatter` (generic type `ILoggingEvent` for Logback, `LogEvent` for Log4j2), return any String, and set `logging.structured.format.console` or `.file` to its fully qualified class name.

## Checked

2026-11-07. Read features/logging.html (Structured Logging section, through Supporting Other Structured Logging Formats) in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Changed 'must honor' to the page's softer 'update your configuration to respect' for the CONSOLE/FILE_LOG_STRUCTURED_FORMAT properties. The default-configuration files the page links were not opened. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
