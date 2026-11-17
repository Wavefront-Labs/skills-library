---
id: computing-software.software-engineering.quarkus.quarkus-logging-categories-handlers
name: quarkus-logging-categories-handlers
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, logging, log-levels, handlers, jboss-logging, console, file]
level: practitioner
status: docs-checked
description: "Configure Quarkus logging: logger APIs, levels, min-level, per-category settings, console/file/syslog/socket handlers, named handlers and filters."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/logging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus logging: levels, categories and handlers

Quarkus logs through the JBoss Log Manager. JBoss Logging and `java.util.logging` work out of the box; SLF4J, Commons Logging and Log4j 2 need an adapter (`org.jboss.slf4j:slf4j-jboss-logmanager`, `org.jboss.logging:commons-logging-jboss-logging`, `org.jboss.logmanager:log4j2-jboss-logmanager`). Without adapters a native build can fail with `ClassNotFoundException: org.apache.commons.logging.impl.LogFactoryImpl`.

## Getting a logger

- `private static final Logger LOG = Logger.getLogger(MyService.class);` (`org.jboss.logging.Logger`)
- `io.quarkus.logging.Log.info("...")`: static calls that Quarkus rewrites at build time. Use only in application classes, not in extensions or dependencies.
- In CDI beans: `@Inject Logger log;` (named after the class) or `@LoggerName("foo") Logger fooLog;`.
- Do not create loggers with unbounded dynamic names; their metadata is kept for the life of the app.

## Levels and categories

```properties
quarkus.log.level=INFO
quarkus.log.category."org.hibernate".level=DEBUG
quarkus.log.category."org.hibernate".min-level=TRACE
```

- Category names in properties need quotes. On the command line escape them: `-Dquarkus.log.category.\"org.hibernate\".level=TRACE`.
- A category applies recursively to subcategories; unconfigured categories fall back to the parent, then the root.
- `min-level` is build-time. To log below DEBUG (for example TRACE) you must also lower `quarkus.log.min-level` (or the per-category `min-level`).

## Handlers

- Console: on by default; `quarkus.log.console.format=%d{yyyy-MM-dd HH:mm:ss} %-5p [%c] (%t) %s%e%n`.
- File: disabled by default; `quarkus.log.file.enabled=true`, `quarkus.log.file.path=application.log` (supports rotation).
- Syslog (RFC 5424): `quarkus.log.syslog.enabled=true`, `quarkus.log.syslog.app-name=my-application`.
- Socket: `quarkus.log.socket.enabled=true`, `quarkus.log.socket.endpoint=localhost:4560`.

## Named handlers per category

```properties
quarkus.log.handler.file.my-file-handler.enabled=true
quarkus.log.handler.file.my-file-handler.path=application.log
quarkus.log.category."com.example".handlers=my-file-handler
quarkus.log.category."com.example".use-parent-handlers=false
```

Handlers can also attach to the root logger with `quarkus.log.handlers=<names>`.

## Filters

Annotate a `final` class implementing `java.util.logging.Filter` with `@LoggingFilter(name = "my-filter")`, then set `quarkus.log.console.filter=my-filter`.

## Gotcha

For `@QuarkusTest`, set `java.util.logging.manager` to `org.jboss.logmanager.LogManager` (Surefire `systemPropertyVariables` or Gradle `systemProperty`), or logging will not work as expected.

## Checked

2026-11-07. Read in full: logging.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
