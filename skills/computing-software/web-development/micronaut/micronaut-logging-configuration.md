---
id: computing-software.web-development.micronaut.micronaut-logging-configuration
name: micronaut-logging-configuration
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, logging-config, logback, logger-levels, slf4j, logging-system, log4j2]
level: intro
status: docs-checked
description: "Set up Micronaut logging with Slf4j and Logback, change log levels via logger.levels, use a custom Logback file with logger.config and understand LoggingSystem."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/logging/loggingMessages.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/logging/logback.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/logging/loggingConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/logging/loggingSystem.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: log from your code and control levels and Logback configuration.

## Log messages

Use Slf4j: `private static Logger logger = LoggerFactory.getLogger(LoggerExample.class);` then `logger.debug(...)`, `logger.info(...)`, `logger.error(...)`.

## Logback

Add `ch.qos.logback:logback-classic` (Gradle `implementation`). Note from the docs: Logback 1.3.x+ has a breaking binary change that may not work with Micronaut 3.8.x; downgrade to 1.2.x if affected.

Put a `logback.xml` in `src/main/resources`:

```xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%cyan(%d{HH:mm:ss.SSS}) %gray([%thread]) %highlight(%-5level) %magenta(%logger{36}) - %msg%n</pattern>
        </encoder>
    </appender>
    <root level="info">
        <appender-ref ref="STDOUT"/>
    </root>
</configuration>
```

Add a per-package level with `<logger name="io.micronaut.context" level="TRACE"/>`.

## Levels via configuration

```yaml
logger:
  levels:
    foo.bar: ERROR
```

Equivalent environment variable: `LOGGER_LEVELS_FOO_BAR`. There is currently no way to set levels for unconventional prefixes such as `foo.barBaz`. To disable a logger, set its level to `OFF` (e.g. `io.verbose.logger.who.CriedWolf: OFF` turns off all logging for that class).

## Custom Logback file

```yaml
logger:
  config: /foo/custom-logback.xml
```

Checked on the classpath first, then the file system. When any `logger.*` property is set, Micronaut resets and reconfigures Logback at startup and on every refresh event, before applying levels.

- A file named by Micronaut configuration wins: `logback.configurationFile` (unless its value equals the JVM system property of that name), or `logger.config` when `logback.configurationFile` is not set. It is used even if a custom Logback `Configurator` service is registered; startup fails if the file is missing or unparseable.
- Otherwise Logback is configured as it does itself (Configurator services, then the `logback.configurationFile` system property, `logback-test.xml`, `logback.xml`, then basic console). In that case `logger.config` is not used, and a parse error is reported but the app still starts.
- Micronaut adds one step: a `logback.xml` in the working directory is used when there is no Configurator service, no `logback.configurationFile` system property, and no `logback-test.xml` or `logback.xml` on the classpath. Until the context starts, such an app logs with the basic console configuration.

## LoggingSystem

`LoggingSystem` is the API that sets levels at runtime; implementations are provided for Logback and Log4j2. Supply your own bean implementing it with `@Replaces` to change behaviour (the config-driven level setting only works through this interface).

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
