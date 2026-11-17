---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-monitoring-and-metrics
name: dataproc-monitoring-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, dataproc-monitoring, dataproc-metrics, yarn-metrics, alerting]
level: practitioner
status: docs-checked
description: "Monitor Dataproc clusters and jobs: enabling custom metric sources (YARN, Spark, HDFS) with overrides, and where job driver, YARN container and agent logs appear in Cloud Logging."
sources: ["https://cloud.google.com/dataproc/docs/guides/dataproc-metrics", "https://cloud.google.com/dataproc/docs/guides/logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc monitoring and metrics

## 1. Custom metric collection
Enable collection from one or more metric sources when you create the cluster. Sources:
`spark`, `flink`, `hdfs`, `yarn`, `spark-history-server`, `hiveserver2`, `hivemetastore`,
`monitoring-agent-defaults` (names are case insensitive). A standard set is collected per
source unless you specify overrides.
```bash
gcloud dataproc clusters create etl --region=<R> \
  --metric-sources=yarn,spark,hdfs \
  --metric-overrides=yarn:ResourceManager:QueueMetrics:PendingMB
```
- `--metric-overrides` takes a list of metrics (case sensitive, CamelCase); only the overridden metrics are collected from that source, and other sources keep their standard set.
- The source of an override must be enabled (a `spark:driver` override needs `--metric-sources=spark`).
- `--metric-overrides-file` (local or `gs://` file) is the alternative; the two flags cannot be combined.
- On 2.2 and later images, `monitoring-agent-defaults` is not available unless the Ops Agent is installed.
- View them in Metrics Explorer under the VM Instance resource, Custom metrics. Look up exact metric names in the custom metrics tables on the Dataproc metrics page.

## 2. Logs
- Job driver output: Logging log name `dataproc.job.driver`.
- YARN container logs: `dataproc.job.yarn.container`. Both are listed under the Dataproc Job resource.
- System logs include `google.dataproc.agent` and `google.dataproc.startup` (startup script plus initialization action log), and the autoscaler log.
- Extended logs can be turned off with `dataproc:dataproc.logging.extended.enabled=false`, VM syslogs with `dataproc:dataproc.logging.syslog.enabled=false`.

## 3. Alerts
Build alerts from the custom metrics you enabled (for example pending YARN memory staying above zero) and from log-based metrics on the job logs above. Check the metric names on the Dataproc and Cloud Monitoring metrics pages before writing policies.

## Gotchas
- Collecting many per-node metrics from large clusters is more data; pick overrides rather than whole sources.

## Verify
- [ ] Metrics Explorer shows the enabled custom metrics; a deliberately failing job leaves entries in the driver log.

## Checked
2026-10-31. Confirmed against the Dataproc metrics guide (metric sources list, `--metric-sources`, `--metric-overrides`, `--metric-overrides-file`, override rules, 2.2 Ops Agent note, Metrics Explorer path) and the Dataproc logging guide (log names, system logs, the two property switches). Corrected the flag: the old `--dataproc-metric-source` does not exist. Removed unconfirmed built-in metric names (`yarn/memory_size`, hdfs and job metrics), the billing claim, `gcloud dataproc jobs wait`, the `...stackdriver.job...enable` properties, `--max-idle`, the 20-minute alert threshold and the Persistent History Server note.
Method: documentation only; no commands were run.
