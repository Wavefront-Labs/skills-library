---
id: computing-software.data-engineering.druid.druid-logging-configuration
name: druid-logging-configuration
category: computing-software
field: data-engineering
product: druid
tags: [logging, log4j2, rolling-file, druid-log-dir, metrics-logging]
level: intro
status: docs-checked
description: "Configure Druid's log4j2 logging and log retention."
sources:
  - https://github.com/apache/druid/blob/master/docs/configuration/logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid services emit logs for debugging and also emit periodic metrics about their state. To stop metric info logs set `-Ddruid.emitter.logging.logLevel=debug`.

Druid uses log4j2. The default `log4j2.xml` ships at `conf/druid/{config}/_common/log4j2.xml`. By default it uses `RollingRandomAccessFile`, rolling over daily and keeping log files up to 7 days. If that does not suit you, edit `log4j2.xml`.

The example based on the micro quickstart defines a log path property `druid.log.path` with value `log`; to change the directory set the `DRUID_LOG_DIR` environment variable before launching Druid. It has a Console appender, and a rolling file appender writing `${sys:druid.log.path}/${sys:druid.node.type}.log`, rolled into `${sys:druid.node.type}.%d{yyyyMMdd}.log`.

The example's Console appender uses a pattern layout with an ISO8601 timestamp, level, thread and logger name. Its file appender deletes `*.log` files older than 7 days. The example also sets individual loggers to `info`, with comments saying to set `debug` on `org.apache.druid.server.QueryResource` and `QueryLifecycle` for query-error stack traces, on `org.apache.druid.server.coordinator` (or `trace`) for balancing and load/drop rule details, on `org.apache.druid.segment` for segment and ingestion detail, and on `org.apache.druid.initialization` for extension initialization.

Peons always write logs to standard output; Middle Managers redirect task logs from standard output to long-term storage. All services, including peon processes, share the log4j configuration file, and you must define a console appender in the logger for peons: otherwise Druid creates a new console appender that keeps only the log level and none of the other appender configuration.

With an all-in-one start command such as `bin/start-micro-quickstart` there are two log files per service: the rotated log4j2 file (for example `log/historical.log`) and a secondary file for output written straight to stdout or stderr (for example `log/historical.stdout.log`), mostly Java runtime messages. The secondary file is not rotated but is generally small; it can be truncated with `truncate --size 0 log/historical.stdout.log`.

## Checked

Confirmed against the Druid docs page "Logging": the metric-log property, default file path, default rolling and 7-day retention, `DRUID_LOG_DIR`, example appenders and loggers, peon behaviour and the all-in-one log files. Removed the unsourced advice to plan separate log shipping.

Method: docs-only read of cited pages, 2026-11-08
