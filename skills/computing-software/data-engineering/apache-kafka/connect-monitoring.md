---
id: computing-software.data-engineering.apache-kafka.connect-monitoring
name: connect-monitoring
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, connect-monitoring, jmx-metrics, task-failures, connect-rest-api, alerting]
level: practitioner
status: docs-checked
description: "Monitor Kafka Connect: REST status polling for failed tasks, key JMX metrics (task status, errors, offset commit, source/sink lag), and alert rules."
sources:
  - https://kafka.apache.org/documentation/#connect_monitoring
  - https://kafka.apache.org/documentation/#connect_rest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Connect monitoring and task failure alerting

Errors are retried only as configured by `errors.retry.*`; a FAILED task needs a restart. Without monitoring, a connector can stay FAILED unnoticed.

## REST status
```bash
curl -s :8083/connectors/orders-cdc/status | jq -r '.tasks[] | select(.state=="FAILED") | .trace' | head -30
curl -s -X POST ":8083/connectors/orders-cdc/restart?includeTasks=true&onlyFailed=true"
```
States: `UNASSIGNED` (not yet assigned to a worker), `RUNNING`, `PAUSED`, `STOPPED` (connectors only; their tasks are not shown), `FAILED` (the exception is reported in the status output). Status changes can lag briefly because workers read them from `status.storage.topic`.

## JMX metrics (kafka.connect)
| MBean | Metric | Alert |
|---|---|---|
| `connector-metrics,connector=*` | `status` | != running |
| `connector-task-metrics,connector=*,task=*` | `status`, `offset-commit-failure-percentage`, `batch-size-avg` | failed; commit failures > 0 |
| `task-error-metrics,connector=*,task=*` | `total-record-errors`, `total-records-skipped`, `deadletterqueue-produce-requests`, `total-retries` | errors/skips rising (data being dropped to DLQ or skipped) |
| `source-task-metrics` | `source-record-poll-rate`, `source-record-write-rate`, `poll-batch-avg-time-ms` | rate 0 while source active |
| `sink-task-metrics` | `sink-record-read-rate`, `put-batch-avg-time-ms`, `offset-commit-completion-rate` | put time climbing (slow sink) |
| `connect-worker-metrics` | `connector-count`, `task-count`, `connector-startup-failure-total`, `task-startup-failure-total` | startup failures |
| `connect-worker-rebalance-metrics` | `rebalancing`, `time-since-last-rebalance-ms` | constant rebalancing |

## Lag
- Sink connectors consume through a consumer group, so alert on consumer lag like any group.
- Source connectors: compare source position with connector offsets, using the connector's own metrics.

## Verify
- [ ] Deliberately break a connector config in staging (bad credentials): alert fires within minutes.
- [ ] DLQ topic has its own lag/size alert.

## Checked
2026-11-01. Confirmed against the Kafka 3.9 docs: Connect metrics reference (every metric name in the table and the `connector-metrics`, `task-error-metrics`, `connect-worker-rebalance-metrics` groups), Connect administration page (task states, `status.storage.topic`), user guide (restart `includeTasks`/`onlyFailed`, `errors.retry.*`). Removed: `RESTARTING` state, version tags, `expand=status` listing, Prometheus exporter, consumer-group naming and Debezium metric claims.
Method: documentation only; no commands were run.
