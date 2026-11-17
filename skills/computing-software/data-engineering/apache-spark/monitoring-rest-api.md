---
id: computing-software.data-engineering.apache-spark.monitoring-rest-api
name: monitoring-rest-api
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-rest-api, monitoring, history-server, spark-ui, automation, spark-monitoring]
level: practitioner
status: docs-checked
description: "Pull Spark job, stage, executor and SQL metrics from the monitoring REST API (/api/v1) on the live UI or History Server for alerting and automated tuning reports."
sources:
  - https://spark.apache.org/docs/latest/monitoring.html#rest-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark monitoring REST API

Every Spark UI (driver on :4040, History Server on :18080) serves JSON under `/api/v1`. Use it to script checks that the UI only shows visually.

```bash
H=http://history:18080/api/v1
curl -s "$H/applications?status=completed&minDate=2026-10-17"
APP=<app-id>
curl -s "$H/applications/$APP/jobs"
curl -s "$H/applications/$APP/stages?status=complete"
curl -s "$H/applications/$APP/stages/<stage-id>/<stage-attempt-id>/taskSummary?quantiles=0.5,0.95,1.0"
curl -s "$H/applications/$APP/allexecutors"                # active and dead executors
curl -s "$H/applications/$APP/sql"
curl -s "$H/applications/$APP/environment"
curl -s -o logs.zip "$H/applications/$APP/logs"            # event logs as a zip
```
- On a running app the base is `http://<driver>:4040/api/v1/applications/<app-id>/...`.
- Applications with several attempts use `/applications/<base-app-id>/<attempt-id>/...` (for example `/logs`).
- The `/streaming/*` endpoints describe a streaming context (DStreams); for Structured Streaming use `StreamingQueryListener` or the Structured Streaming tab in the web UI.
- `executors` lists active executors only; `allexecutors` lists active and dead ones.
- `stages?details=true` includes task data; `taskSummary?quantiles=` summarises task metrics.

## Useful automated checks
- Skew: compare the max with the median `executorRunTime` from `taskSummary`.
- Spill: stage `memoryBytesSpilled` / `diskBytesSpilled`.
- GC: executor `totalGCTime` against `totalDuration`.
- Config drift: diff `environment` between a fast run and a slow run.

## Gotchas
- The History Server serves only applications whose event logs it has loaded; see `spark.history.fs.update.interval` and `spark.history.store.path`.
- The environment endpoint exposes configuration; see `spark.redaction.regex` and the security section of the docs.

## Verify
- [ ] Script output matches the numbers shown in the UI for one sample stage.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in monitoring.md: /api/v1 paths (applications, jobs, stages, stages/[id]/[attempt]/taskSummary with ?quantiles, allexecutors vs executors, sql, environment, logs, [base-app-id]/[attempt-id]/logs, streaming/* for the streaming context), minDate and status query parameters, field names executorRunTime, memoryBytesSpilled, diskBytesSpilled, totalGCTime, totalDuration. Removed jq filters, field names not in the docs (shuffleReadBytes, numFailedTasks) and numeric alert thresholds.

Method: documentation only; no commands were run.
