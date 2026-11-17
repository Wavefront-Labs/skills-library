---
id: computing-software.data-engineering.apache-spark.history-server-and-event-logs
name: history-server-and-event-logs
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-monitoring, spark-history-server, spark-event-log, eventlog-dir, rolling-event-logs, event-log-compaction, rest-api, post-mortem]
level: practitioner
status: docs-checked
description: "Keep Spark UIs after jobs finish: enable event logs to durable storage, run the history server, rolling/compacted logs, cleaner retention, and the monitoring REST API."
sources:
  - https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact
  - https://spark.apache.org/docs/latest/monitoring.html#rest-api
  - https://spark.apache.org/docs/latest/configuration.html#spark-ui
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# History server and event logs

**Goal:** inspect any finished or failed application's UI and metrics days later, which is where most post-mortems happen.

## Enable event logging (every app)
```properties
spark.eventLog.enabled=true
spark.eventLog.dir=s3a://<BUCKET>/spark-events/       # durable, shared; hdfs:///spark-logs on Hadoop
spark.eventLog.compress=true                           # default true
spark.eventLog.rolling.enabled=true                    # since 3.0.0; default true in the current docs
spark.eventLog.rolling.maxFileSize=128m                    # default
```
The live UI disappears when the application exits; the history server rebuilds it from event logs written to durable storage.

## Run the history server
```properties
# spark-defaults.conf on the history host
spark.history.fs.logDirectory=s3a://<BUCKET>/spark-events/
spark.history.fs.update.interval=30s                   # default 10s
spark.history.retainedApplications=50          # default 50: apps whose UI data stays cached
spark.history.fs.cleaner.enabled=true               # default false
spark.history.fs.cleaner.maxAge=14d
spark.history.fs.eventLog.rolling.maxFilesToRetain=2   # enables compaction of rolled logs (compaction is lossy)
spark.history.store.path=/var/spark/history-store      # local directory; stores app data on disk instead of memory
```
```bash
./sbin/start-history-server.sh     # UI on :18080
```

## REST API (same on live UI :4040 and history :18080)
```bash
curl "http://<HOST>:18080/api/v1/applications?status=completed&minDate=2026-10-15"
curl "http://<HOST>:18080/api/v1/applications/<appId>/stages?status=failed"
curl http://<HOST>:18080/api/v1/applications/<appId>/executors
curl http://<HOST>:18080/api/v1/applications/<appId>/sql
```

## Gotchas
- Very large event logs make the history server slow: use rolling plus compaction, and size the server heap with `SPARK_DAEMON_MEMORY` (default 1g).
- Event logs contain configuration values; restrict access to the log directory and see `spark.redaction.regex` for redaction.

## Verify
- [ ] A just-finished job appears in the history server within the update interval with full SQL and stage tabs.
- [ ] Cleaner removes logs older than the retention period.
- [ ] REST API returns stage data for a completed app.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in monitoring.md and configuration.md: history server UI on :18080, SPARK_DAEMON_MEMORY default 1g, spark.history.fs.update.interval default 10s (skill said 30s as if default), retainedApplications 50, cleaner.enabled false, cleaner.maxAge, store.path semantics, maxFilesToRetain compaction (lossy), eventLog.rolling.enabled (default true, since 3.0.0), rolling.maxFileSize 128m, eventLog.compress true, REST paths and minDate/status query parameters. Removed vendor-service and unsourced operational claims.

Method: documentation only; no commands were run.
