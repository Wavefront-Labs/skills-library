---
id: computing-software.data-engineering.apache-spark.log4j2-logging-configuration
name: log4j2-logging-configuration
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, log4j2-config, logging, setloglevel, structured-logging, executor-logs, rolling-logs]
level: practitioner
status: docs-checked
description: "Configure Spark log4j2 logging for driver and executors: custom log4j2.properties, per-package levels, rolling executor logs and JSON structured logs."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#configuring-logging
  - https://logging.apache.org/log4j/2.x/manual/configuration.html
  - https://spark.apache.org/docs/latest/configuration.html#spark-ui
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Spark logging with log4j2

**Goal:** readable driver/executor logs at the right verbosity, that do not fill disks, and that your log platform can parse.

Spark's logging is configured with a `log4j2.properties` file, started from `conf/log4j2.properties.template` (plain text) or `conf/log4j2-json-layout.properties.template` (structured).

## Custom config file
```properties
# log4j2.properties
rootLogger.level = warn
rootLogger.appenderRef.stdout.ref = console
appender.console.type = Console
appender.console.name = console
appender.console.target = SYSTEM_ERR
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n%ex

logger.myapp.name = com.acme.etl
logger.myapp.level = info
logger.parquet.name = org.apache.parquet
logger.parquet.level = error
```
Point driver and executors at the file with the `log4j2.configurationFile` system property (the file must exist at that path on every node):
```bash
spark-submit \
  --conf spark.driver.extraJavaOptions=-Dlog4j2.configurationFile=<PATH>/log4j2.properties \
  --conf spark.executor.extraJavaOptions=-Dlog4j2.configurationFile=<PATH>/log4j2.properties ...
```

## Runtime level change
```python
spark.sparkContext.setLogLevel("WARN")   # valid levels: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
```

## Executor log rolling
```properties
spark.executor.logs.rolling.strategy=size
spark.executor.logs.rolling.maxSize=134217728
spark.executor.logs.rolling.maxRetainedFiles=5
```
See your cluster manager's documentation for where executor logs are collected.

## Structured JSON logs
```properties
spark.log.structuredLogging.enabled=true
```
Load the JSON logs for analysis with `from pyspark.logger import SPARK_LOG_SCHEMA` and `spark.read.schema(SPARK_LOG_SCHEMA).json("<LOG_PATH>")`.

## Application logging from PySpark
```python
import logging; logging.getLogger("etl").info("rows=%d", n)                          # Python logger
```
Avoid per-row logging inside UDFs.

## Gotchas
- Scope DEBUG logging to one package rather than all of `org.apache.spark`.
- Secrets in confs: Spark redacts keys matching `spark.redaction.regex` in UI/logs; extend it for custom secret keys.

## Verify
- [ ] Executor stderr shows the custom pattern (config was picked up on executors, not just driver).
- [ ] Log volume per job within budget; no secret values in logs.

## Checked
2026-10-28. Confirmed on the Spark configuration page (Configuring Logging, executor log rolling settings, `spark.redaction.regex`), the SparkContext.setLogLevel API page and the Log4j configuration manual: `log4j2.properties` in `conf` copied from `log4j2.properties.template` or `log4j2-json-layout.properties.template`; `spark.log.structuredLogging.enabled` and `SPARK_LOG_SCHEMA`; `log4j2.configurationFile` system property; `spark.executor.logs.rolling.strategy` (`time` or `size`), `maxSize`, `maxRetainedFiles`; setLogLevel valid levels ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN.
Removed as unconfirmed: the Spark 3.3+ and Spark 4 version claims, the `--files` flag, the wrong driver property name `log4j.configurationFile` (the documented property is `log4j2.configurationFile`), and the standalone / k8s scope of rolling.
Method: documentation only; no commands were run.
