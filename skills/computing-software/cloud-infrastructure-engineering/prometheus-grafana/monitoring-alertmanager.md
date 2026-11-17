---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-alertmanager
name: monitoring-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager-meta-monitoring, notification-failures, alertmanager, meta-monitoring, alertmanager-mixin]
level: practitioner
status: docs-checked
description: "Monitor Alertmanager itself: failed notifications per integration, cluster membership, config reload status and consistency, using the alertmanager-mixin alert set."
sources: ["https://github.com/prometheus/alertmanager/tree/main/doc/alertmanager-mixin", "https://monitoring.mixins.dev/alertmanager/", "https://prometheus.io/docs/alerting/latest/alertmanager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Alertmanager

## Prerequisites
The alertmanager-mixin alerts monitor a cluster of Alertmanager instances. The Prometheus server evaluating them must
scrape every instance of the cluster, even across locations. All instances in one Alertmanager cluster must share the
same `job` label; different clusters need different `job` labels.

## Key metrics (as used by the mixin)
```promql
# failed notifications per integration (slack, pagerduty, email, webhook...)
rate(alertmanager_notifications_failed_total{job="alertmanager"}[15m])
  / ignoring (reason) group_left
rate(alertmanager_notifications_total{job="alertmanager"}[15m])
max_over_time(alertmanager_config_last_reload_successful{job="alertmanager"}[5m]) == 0
alertmanager_cluster_members{job="alertmanager"}        # compare with the replica count of the cluster
count by (job) (count_values by (job) ("config_hash", alertmanager_config_hash{job="alertmanager"})) != 1
```
The mixin wraps gauges in `max_over_time(...[5m])` so failed scrapes do not create false negatives.

## Mixin alerts (alertmanager-mixin)
| Alert | Condition (summary) | Severity |
|---|---|---|
| AlertmanagerFailedReload | last reload unsuccessful, for 10m | critical |
| AlertmanagerMembersInconsistent | an instance sees fewer members than the cluster has, for 15m | critical |
| AlertmanagerFailedToSendAlerts | one instance's failure ratio to an integration above 0.01 over 15m, for 5m | warning |
| AlertmanagerClusterFailedToSendAlerts | minimum failure ratio across instances above 0.01; critical for integrations matching the critical selector, warning for the rest | critical / warning |
| AlertmanagerConfigInconsistent | instances have different `config_hash`, for 20m | critical |
| AlertmanagerClusterDown | half or more instances up less than half of the last 5m, for 5m | critical |
| AlertmanagerClusterCrashlooping | half or more instances restarted at least 5 times in 10m, for 5m | critical |

Build the YAML with `mixtool` and `jsonnetfmt`: edit `config.libsonnet`, then `make build`. The mixin also ships an
`alertmanager-overview` dashboard.

## The catch
If Alertmanager is broken, these alerts cannot reach you through it. Combine with:
- A Watchdog/dead man's switch (external heartbeat).
- A second, independent route for meta-alerts (e.g. a different Alertmanager or a direct webhook from a separate Prometheus).

## Prometheus side
Point Prometheus at the list of all Alertmanagers; do not load balance traffic between Prometheus and its
Alertmanagers. Clustering uses the `--cluster-*` flags. If you set `--alerts.per-alertname-limit`, new alerts beyond
the limit are dropped and counted in `alertmanager_alerts_limited_total`.

## Gotchas
- A receiver with a revoked Slack webhook fails silently from the user's view; the failure ratio metric is the only signal.
- Notification failures for one integration can be partial (rate limits); alert on a ratio over a window (the mixin
  uses 15m with a 1% threshold), not single failures.

## Verify
- [ ] Revoking a test webhook makes `AlertmanagerFailedToSendAlerts` fire and reach you via the independent path.

## Checked
Checked 2026-11-08 against the alertmanager-mixin README, the generated alert list at monitoring.mixins.dev and the
Prometheus Alertmanager overview page. Removed as not on those pages: the notification latency histogram query, the
`alertmanager_alerts{state="active"}` query and the `prometheus_notifications_*` metric names. Thresholds and
durations are taken from the generated mixin alerts and can change with mixin versions.
Method: documentation only; no commands were run.
