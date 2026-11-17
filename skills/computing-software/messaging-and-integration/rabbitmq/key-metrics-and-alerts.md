---
id: computing-software.messaging-and-integration.rabbitmq.key-metrics-and-alerts
name: key-metrics-and-alerts
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, key-metrics-and-alerts]
level: practitioner
status: docs-checked
description: "Alert on memory and disk alarms, queue depth growth, unacked messages, file descriptors and node down."
sources:
  - https://www.rabbitmq.com/docs/monitoring
  - https://www.rabbitmq.com/docs/prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key metrics and alerts

**Goal:** Detect trouble early.

## Steps
1. Alert on resource alarms (`mem_alarm`, `disk_free_alarm`), `messages_ready` growth, `messages_unacknowledged`, and consumer count (`object_totals.consumers`).
2. Compare `fd_used` with `fd_total`, and `proc_used` with `proc_total`.
3. Watch connection and channel counts and connection churn; the guide warns that excessive checks opening TCP connections cause churn.
4. Prometheus metrics for connection, channel and queue churn are grouped under `connection_churn_metrics`.

## Failure modes
- Monitoring only node liveness misses resource alarms and growing backlogs.

## Verify
- Induce a backlog and see the alert fire.

## Checked

Date: 2026-11-02. Confirmed on the Monitoring and Prometheus guides: metric names above. Removed: `rabbitmq_alarms_*` (not in these pages), confirm-rate comparison, socket-versus-limit wording.

Method: documentation only; no commands were run.
