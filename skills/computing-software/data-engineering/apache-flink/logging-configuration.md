---
id: computing-software.data-engineering.apache-flink.logging-configuration
name: logging-configuration
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-logging, log4j2, kubernetes-logging, json-logs, log-rotation]
level: practitioner
status: docs-checked
description: "Configure Flink logging: log4j2 files for JobManager/TaskManager/CLI, rolling and JSON output, per-package levels, dynamic changes on Kubernetes, and avoiding log floods."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/advanced/logging/
  - https://github.com/apache/flink-kubernetes-operator/blob/main/docs/content/docs/operations/logging.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Logging configuration

Flink uses Log4j 2 via SLF4J. Files in `conf/`:
- `log4j.properties`: JobManager and TaskManager processes.
- `log4j-console.properties`: processes run in the foreground (Docker/Kubernetes `start-foreground`), logging to stdout and a file.
- `log4j-cli.properties`: the `flink` CLI. `log4j-session.properties`: session CLIs (yarn-session, kubernetes-session).

## Typical production config (Kubernetes)
```properties
monitorInterval=30                       # Log4j re-reads the file every 30 s (the Flink default)
rootLogger.level=INFO
rootLogger.appenderRef.console.ref=ConsoleAppender
appender.console.name=ConsoleAppender
appender.console.type=CONSOLE
appender.console.layout.type=JsonTemplateLayout
appender.console.layout.eventTemplateUri=classpath:<template>.json   # choose one of the Log4j Event Templates
logger.kafka.name=org.apache.kafka
logger.kafka.level=WARN
logger.hadoop.name=org.apache.hadoop
logger.hadoop.level=WARN
logger.app.name=com.acme
logger.app.level=INFO
```
- JSON output suits structured log stores; the required `log4j-layout-template-json` jar is bundled in flink-dist. Flink also adds fields such as `flink-job-id` to the MDC on most relevant messages (experimental), which a JSON layout can include.
- The log files can be accessed via the Job-/TaskManager pages of the Web UI, so keep a file appender if you want logs there; otherwise log to stdout and let the platform collect.

## Rolling files (VM/YARN)
```properties
appender.rolling.type=RollingFile
appender.rolling.fileName=${sys:log.file}
appender.rolling.filePattern=${sys:log.file}.%i
appender.rolling.policies.size.type=SizeBasedTriggeringPolicy
appender.rolling.policies.size.size=100MB
appender.rolling.strategy.type=DefaultRolloverStrategy
appender.rolling.strategy.max=10
```

## Kubernetes operator
The default logging settings can be overridden per deployment by putting the entire log configuration into `spec.logConfiguration` (key `log4j-console.properties`). The operator supports Log4j2 (default) and Logback. Log4j re-reads its files every 30 seconds by default (`monitorInterval`).

## Avoid
- Logging per record at INFO in user functions: very high volume that can saturate disk or I/O and cause backpressure. Use metrics or sampled logging.
- DEBUG on `org.apache.flink` in production: very high log volume.
- Switching to Logback is a documented option, but it needs the logback jars in `lib/` and the Log4j 2 jars removed; follow the Configuring logback section rather than mixing both.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the logging page (properties files and their roles, `monitorInterval` every 30 s by default, `env.log.dir|level|max`, bundled JsonTemplateLayout jar, MDC `flink-job-id`, Web UI log access, logback section) and the Flink Kubernetes Operator logging page (`spec.logConfiguration`, Log4j2 default). Corrected the layout jar location (bundled, not copied to `lib/`) and removed the unconfirmed UI-tab, Logback-exclusion and volume claims.

Method: documentation only; no commands were run.

## Verify
- [ ] Changing a logger level in the mounted configuration takes effect within `monitorInterval` with no restart.
- [ ] Logs from JM and every TM pod arrive in the log store as structured JSON with pod/job labels.
