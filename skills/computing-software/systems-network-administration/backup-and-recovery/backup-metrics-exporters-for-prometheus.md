---
id: computing-software.systems-network-administration.backup-and-recovery.backup-metrics-exporters-for-prometheus
name: backup-metrics-exporters-for-prometheus
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-metrics-exporter, prometheus, backup-monitoring]
level: advanced
status: docs-checked
description: "Export backup job metrics to Prometheus with the node_exporter textfile collector or an exporter, and alert on last-success age, not only failure."
sources:
  - https://prometheus.io/docs/instrumenting/writing_exporters/
  - https://prometheus.io/docs/practices/pushing/
  - https://github.com/prometheus/node_exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup metrics exporters for Prometheus

## The key metric
A last-success timestamp per backup job, for example `backup_last_success_timestamp_seconds{job="..."}` (a name you choose). Alert on its age, which catches failures, disabled jobs and stuck schedulers alike. A job that never runs never fails, so failure-only alerting misses it.

## Patterns
1. **Textfile collector** (simplest): the backup script writes a `.prom` file at the end of a run. Machine-tied batch jobs belong here rather than in the Pushgateway.
   - Start node_exporter with `--collector.textfile.directory`; the collector parses all files in that directory matching `*.prom` in the Prometheus text format. Timestamps are not supported.
   - Write atomically, as the node_exporter README does:
     ```
     echo my_batch_job_completion_time $(date +%s) > /path/to/directory/my_batch_job.prom.$$
     mv /path/to/directory/my_batch_job.prom.$$ /path/to/directory/my_batch_job.prom
     ```
2. **Exporter**: a small service that queries the backup system's API and exposes metrics for Prometheus to scrape. Do not set timestamps on exposed metrics; let Prometheus do it.
3. **Pushgateway**: Prometheus recommends it only in limited cases, for service-level batch jobs. Pitfalls: single point of failure and bottleneck, you lose the automatic `up` health metric, and it never forgets pushed series until you delete them through its API.

## Alerting
Alert when the age of the last-success timestamp exceeds your backup interval plus slack, and also when the metric is missing altogether. Add duration trend and repository free-space alerts.

## Gotchas
- High cardinality causes problems (the node_exporter README lists it as a concern); label by job and target only, not per file or per restore point.
- For success and failure counts, expose a total and a failed counter rather than one metric with a success/failure label (Prometheus exporter guidance).

## Verify
Disable a job's schedule in a test: the staleness alert fires after the threshold.

## Checked

2026-11-09. Confirmed against the Prometheus "Writing exporters" page (no timestamps, total and failed metrics, batch job guidance), "When to use the Pushgateway" (pitfalls, textfile collector for machine-related batch jobs) and the node_exporter README (textfile directory flag, `*.prom` glob, no timestamps, atomic write example, cardinality). Partial reads of the two long pages. Removed: Veeam REST, Bacula and PBS API claims (the Veeam page returned a stub), sample metric names beyond the example, PromQL alert rule YAML (the functions are not on the cited pages), the 26-hour threshold, read-only account advice and community exporter remarks.

Method: documentation only; no commands were run.
