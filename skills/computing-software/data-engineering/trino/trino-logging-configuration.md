---
id: computing-software.data-engineering.trino.trino-logging-configuration
name: trino-logging-configuration
category: computing-software
field: data-engineering
product: trino
tags: [logging, log-properties, log-levels, gc-logging, jvm-config]
level: practitioner
status: docs-checked
description: "Set per-package log levels for Trino in etc/log.properties, and enable JVM GC logging for tuning investigations."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/logging.md", "https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/tuning.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino logging configuration

Application logging is optional and configured in `log.properties` inside the installation's `etc` directory. Each logger is named after its class, and levels follow the dotted hierarchy like Java packages. The four levels, from most to least verbose, are `DEBUG`, `INFO`, `WARN`, `ERROR`.

```properties
io.trino=WARN
io.trino.plugin.iceberg=DEBUG
io.trino.parquet=DEBUG
```

This lowers everything under `io.trino` from the default `INFO` to `WARN`, while raising the Iceberg connector and the Parquet reader/writer to `DEBUG` for troubleshooting.

Other useful logger namespaces from the docs:
- `io.airlift` for the Airlift application framework.
- `org.eclipse.jetty` for the Jetty web server.
- `org.postgresql` for the PostgreSQL JDBC driver used by that connector.
- `javax.net.ssl` for Java runtime TLS.
- `java.io` for I/O operations.

Further logging properties are documented in the logging properties page (`properties-logging`). By default output is file-based with rotated files in `var/log`: `launcher.log` (only when the launcher starts Trino in the background), `http-request.log` and `server.log`. `log.format=json` writes JSON output; `node.annotations-file` can add fields with environment variable substitution; `log.path=tcp://<server_ip>:<server_port>` logs to a TCP socket whose endpoint is assumed to be stable. The page's fluentbit example consumes this stream.

For garbage-collection problems the tuning page suggests adding this line to `jvm.config`: `-Xlog:gc*,safepoint::time,level,tags,tid`. It states the default Trino settings work well for most workloads, so tune only when the cluster has a specific performance problem.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Replaced a vague pointer with the page's log output and JSON/TCP logging details; rest unchanged.
