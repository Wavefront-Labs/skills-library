---
id: computing-software.data-engineering.apache-airflow.metrics-statsd-and-opentelemetry
name: metrics-statsd-and-opentelemetry
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-metrics, statsd, opentelemetry, otel, statsd-exporter, prometheus, scheduler-heartbeat, dag-processing-metrics, observability]
level: advanced
status: gated
description: "Emit and use Airflow metrics: StatsD or OpenTelemetry config, Prometheus via statsd-exporter, the scheduler/executor/pool/task metrics worth alerting on, and allow-lists."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/metrics.html
  - https://github.com/prometheus/statsd_exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Airflow metrics: StatsD and OpenTelemetry

**Goal:** dashboards and alerts on Airflow's own health (scheduler, executor, pools, parsing, task outcomes).

## StatsD
```ini
[metrics]
statsd_on = True
statsd_host = statsd-exporter.monitoring.svc
statsd_port = 9125
statsd_prefix = airflow
metrics_allow_list = scheduler,executor,dagrun,dag_processing,pool,ti,triggerer   # prefixes; limits cardinality
statsd_datadog_enabled = False        # True + statsd_datadog_tags for tagged DogStatsD
```
For Prometheus, run `statsd_exporter` with a mapping file that turns dotted names (`airflow.dagrun.duration.success.load_orders`) into labelled metrics (`airflow_dagrun_duration_success{dag_id="load_orders"}`). The official Helm chart deploys one with mappings.

## OpenTelemetry (2.7+)
```ini
[metrics]
otel_on = True
otel_host = otel-collector.monitoring.svc
otel_port = 4318
otel_interval_milliseconds = 30000
otel_ssl_active = False
```
Metrics go via OTLP/HTTP to a collector that exports to Prometheus, Datadog, etc. Tracing is configured separately; see the Airflow traces documentation for the current settings. (gated: unconfirmed, source is paywalled or blocked)

## What to alert on
| Metric | Meaning |
|---|---|
| `scheduler_heartbeat` (counter stops increasing) | Scheduler dead/hung |
| `scheduler.tasks.starving` > 0 sustained | Pools/limits blocking work |
| `executor.queued_tasks` high + `executor.open_slots` 0 | Not enough workers |
| `dag_processing.import_errors` > 0 | Broken DAG files |
| `dag_processing.total_parse_time` near `min_file_process_interval` | Parsing too slow |
| `dagrun.duration.success.<dag>` vs history | Pipeline slowdowns |
| `ti_failures`, `ti.finish.<dag>.<task>.failed` | Failure spikes |
| `pool.open_slots.<pool>` 0 for long | Pool exhaustion |
| `triggerer.capacity_left` / `triggers.blocked_main_thread` | Triggerer saturation |

## Cardinality
Per-DAG/per-task metrics multiply with DAG count. Use `metrics_allow_list`/`metrics_block_list` (and for StatsD, a `stat_name_handler` to sanitise names).

## Verify
- [ ] `airflow_scheduler_heartbeat` visible in Prometheus and increasing.
- [ ] Stopping the scheduler fires the heartbeat alert within minutes.
- [ ] Per-DAG duration panel exists for critical DAGs.

## Checked

2026-11-02

- Confirmed: The Airflow metrics page and the statsd_exporter README were fetched. Confirmed: [metrics] otel_on, statsd_on, statsd_datadog_enabled, metric names ti.finish.{dag_id}.{task_id}.{state}, pool.open_slots.{pool_name}, scheduler_heartbeat, dag_processing.import_errors.
- Removed or gated: Removed the unconfirmed claim about when tracing support arrived. Gated: the OTLP/HTTP port 4318, otel_interval_milliseconds and the 2.7+ version gate were not seen on the fetched page (its example uses port 8889).

Method: documentation only; no commands were run.
