---
id: computing-software.software-engineering.spring-boot.custom-log-configuration
name: custom-log-configuration
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, logging, logback-spring-xml, log4j2-spring-xml, logging-config, loggingsystem, shutdown-hook, mdc]
level: practitioner
status: docs-checked
description: "Supply logback-spring.xml or log4j2-spring.xml, point logging.config at a file, force a LoggingSystem, disable the shutdown hook and use transferred system properties."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Logging systems activate when their libraries are on the classpath, and are customised by a config file in the classpath root or at the `logging.config` location.

Files by system:
- Logback: `logback-spring.xml`, `logback-spring.groovy`, `logback.xml`, or `logback.groovy`
- Log4j2: `log4j2-spring.xml` or `log4j2.xml`
- Java Util Logging: `logging.properties` (known classloading issues from an executable jar; avoid it there)

Prefer the `-spring` variants. With standard locations Spring cannot fully control log initialization.

Logging initializes before the ApplicationContext exists, so `@PropertySource` on `@Configuration` classes cannot control it. To force a system, set the `org.springframework.boot.logging.LoggingSystem` system property to a `LoggingSystem` implementation's class name; the value `none` disables Boot's logging configuration. The page says the logging system can only be changed or disabled through System properties.

Shutdown hook: registered automatically (except for war deployments) to clean up logging when the JVM exits. Disable with `logging.register-shutdown-hook: false` if you have complex context hierarchies and want to use the logging system's own options (for example Logback context selectors).

Environment values are transferred to System properties so config files can read them: `logging.file.name` -> `LOG_FILE`, `logging.file.path` -> `LOG_PATH`, `logging.pattern.console` -> `CONSOLE_LOG_PATTERN`, `logging.pattern.file` -> `FILE_LOG_PATTERN`, `logging.pattern.dateformat` -> `LOG_DATEFORMAT_PATTERN`, `logging.pattern.level` -> `LOG_LEVEL_PATTERN` (default `%5p`), `logging.charset.console` -> `CONSOLE_LOG_CHARSET`, `logging.threshold.console` -> `CONSOLE_LOG_THRESHOLD`, `logging.exception-conversion-word` -> `LOG_EXCEPTION_CONVERSION_WORD`, plus `PID` and the Logback `LOGBACK_ROLLINGPOLICY_*` values.

Placeholders in logging properties use Spring Boot syntax, not the framework's. For Logback, use `:` between property name and default, never `:-`.

MDC trick: override only `logging.pattern.level`, for example `user:%X{user} %5p`, to add an MDC entry to every line.

## Checked

2026-11-07

Read logging.adoc (docs-repo source of the cited Logging page) in full (935 lines). The sample-format partial (logging-format.txt) and the structured-logging MyCustomFormat include were not opened; neither is used by this skill.
Confirmed: logging.config and classpath-root config file; the LoggingSystem system property with a fully qualified class name and none; the NOTE that logging initializes before the ApplicationContext so @PropertySources cannot control it; the file table for Logback, Log4j2 and JDK; the -spring recommendation; the Java Util Logging executable-jar WARNING; the Environment-to-System-property transfer table entries listed (LOG_FILE, LOG_PATH, CONSOLE_LOG_PATTERN, FILE_LOG_PATTERN, LOG_DATEFORMAT_PATTERN, LOG_LEVEL_PATTERN default %5p, CONSOLE_LOG_CHARSET, CONSOLE_LOG_THRESHOLD, LOG_EXCEPTION_CONVERSION_WORD, PID, LOGBACK_ROLLINGPOLICY_*); Spring Boot placeholder syntax and Logback ":" not ":-"; the MDC logging.pattern.level user:%X{user} %5p tip; shutdown hook behaviour, war exception and logging.register-shutdown-hook false with Logback context selectors.
Trimmed: ambiguous "These can only be changed with System properties" reworded to match the page sentence about changing or disabling the logging system.

Method: documentation only; no commands were run.
