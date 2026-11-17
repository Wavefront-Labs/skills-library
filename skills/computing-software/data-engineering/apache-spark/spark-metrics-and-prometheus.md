---
id: computing-software.data-engineering.apache-spark.spark-metrics-and-prometheus
name: spark-metrics-and-prometheus
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-monitoring, spark-metrics, spark-prometheus, metrics-properties, prometheusservlet, jmx-sink, executor-metrics, grafana, observability]
level: advanced
status: docs-checked
description: "Export Spark metrics: metrics.properties sinks, the built-in PrometheusServlet and executor metrics endpoint, JMX exporter alternative, namespaces, and what to alert on."
sources:
  - https://spark.apache.org/docs/latest/monitoring.html#metrics
  - https://spark.apache.org/docs/latest/monitoring.html#executor-metrics
  - https://spark.apache.org/docs/latest/configuration.html#spark-ui
  - https://github.com/apache/spark/blob/master/conf/metrics.properties.template
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark metrics and Prometheus

**Goal:** get driver and executor metrics into Prometheus/Grafana (or another TSDB) for dashboards and alerts across many applications.

## Built-in Prometheus endpoints (since 3.0)
```properties
# spark-defaults / --conf
spark.ui.prometheus.enabled=true                         # default true; executor metrics at /metrics/executors/prometheus on the driver page
spark.metrics.conf.*.sink.prometheusServlet.class=org.apache.spark.metrics.sink.PrometheusServlet
spark.metrics.conf.*.sink.prometheusServlet.path=/metrics/prometheus
spark.metrics.conf.master.sink.prometheusServlet.path=/metrics/master/prometheus
spark.metrics.appStatusSource.enabled=true               # default true; job/stage/task counters
spark.metrics.namespace=${spark.app.name}                # stable names instead of app ids
```
Scrape `http://<driver>:4040/metrics/prometheus` and `/metrics/executors/prometheus`. `PrometheusServlet` is marked experimental in the docs. The master serves `/metrics/master/prometheus` and `/metrics/applications/prometheus` on port 8080.

## Alternative sinks
`metrics.properties` (or `spark.metrics.conf.*` confs) supports `ConsoleSink`, `CSVSink`, `JmxSink`, `MetricsServlet` (JSON), `PrometheusServlet`, `GraphiteSink`, `StatsdSink` and `Slf4jSink`.

## Useful metrics
| Metric | Why |
|---|---|
| executor peak `JVMHeapMemory`, `OnHeapExecutionMemory`, `ProcessTreeJVMRSSMemory` | memory pressure (process tree metrics need `spark.executor.processTreeMetrics.enabled=true`, default false) |
| `totalGCTime` / `MinorGCTime`/`MajorGCTime` | GC-bound executors |
| `failedTasks`, `activeTasks`, executor count | job health, dynamic allocation behaviour |
| Streaming: `inputRate-total`, `processingRate-total`, `latency` (with `spark.sql.streaming.metricsEnabled=true`) | lag |
| appStatus `jobs.failedJobs`, `stages.failedStages` | failures |

## Gotchas
- By default the root namespace for driver and executor metrics is `spark.app.id`, so each run creates new series; set `spark.metrics.namespace` (for example `${spark.app.name}`).
- Metrics need the UI to be on (`spark.ui.enabled=true`) for servlet sinks.

## Verify
- [ ] The driver's `/metrics/prometheus` and `/metrics/executors/prometheus` URLs return data.
- [ ] Series are named by `spark.metrics.namespace`, not by app id.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in monitoring.md, configuration.md and conf/metrics.properties.template: PrometheusServlet (experimental) class and path keys, master/applications prometheus paths, spark.ui.prometheus.enabled default true, appStatusSource.enabled default true, spark.metrics.namespace behaviour, sink list, processTreeMetrics.enabled default false, executor peak metric names, Structured Streaming metrics (need spark.sql.streaming.metricsEnabled=true, default false), failedStages/failedJobs counters. Removed Kubernetes annotation, JMX-exporter and shuffle-metric names that are not in the docs.

Method: documentation only; no commands were run.
