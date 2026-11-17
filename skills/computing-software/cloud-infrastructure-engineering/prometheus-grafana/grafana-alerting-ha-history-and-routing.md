---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-alerting-ha-history-and-routing
name: grafana-alerting-ha-history-and-routing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-alerting, grafana-alerting-ha, alerting-ha-peers, unified-alerting-ha, state-history-loki, alert-state-history, grafana-managed-recording-rules]
level: advanced
status: docs-checked
description: "Run Grafana Alerting in production: HA peers (memberlist or Redis), single-node evaluation, alert state history in Loki or Prometheus, and recording rule behaviour."
sources: ["https://grafana.com/docs/grafana/latest/alerting/set-up/configure-high-availability/", "https://grafana.com/docs/grafana/latest/alerting/set-up/configure-alert-state-history/", "https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-recording-rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana Alerting: HA, state history, recording rules

## High availability
With multiple Grafana instances, all alert rules are evaluated on all instances by default, so alerts keep firing while at
least one instance works. The embedded Alertmanagers use a gossip protocol to make a best-effort attempt to avoid duplicate
notifications; the design prefers an occasional duplicate or out-of-order notification to a missing one. Silences are gossiped
too. Notifications and silences are persisted to the database periodically and on graceful shut down.

Memberlist (the preferred option); gossip uses both TCP and UDP port 9094. In `[unified_alerting]`:
```ini
[unified_alerting]
enabled = true
ha_listen_address = "${POD_IP}:9094"
ha_advertise_address = "${POD_IP}:9094"
ha_peers = "grafana-alerting.grafana:9094"
ha_peer_timeout = 15s
ha_reconnect_timeout = 2m
```
- `ha_peers`: `host:port` list of the cluster instances, at least one. `ha_listen_address` defaults to all interfaces (0.0.0.0).
- `ha_advertise_address` is optional; use it behind NAT (Docker Swarm, Kubernetes services).
- `ha_peer_timeout` defaults to 15s; raise it for cross-region or high-latency networks.
- On Kubernetes the docs expose the Pod IP as `POD_IP` through `status.podIP`, open 9094 on TCP and UDP, and create a headless
  Service (`clusterIP: 'None'`) so `ha_peers` resolves to Pod IPs.

Redis alternative, for environments where Grafana servers cannot reach each other (for example blocked TCP or UDP ports):
set `ha_redis_address` (comma-separated for Cluster or Sentinel). Standalone, Cluster and Sentinel are supported; Redis needs
pub/sub (also through any proxy). Optional keys on the page: `ha_redis_cluster_mode_enabled`, `ha_redis_sentinel_mode_enabled`,
`ha_redis_sentinel_master_name`, `ha_redis_username`, `ha_redis_password`, `ha_redis_prefix`, `ha_redis_tls_enabled`.
`ha_advertise_address` is required if the instance has no RFC 6890 address with a default route.

Single-node evaluation reduces data source query load from N times to 1; it requires HA to be configured:
```ini
[unified_alerting]
ha_single_node_evaluation = true
```
The primary (position 0, metric `grafana_alertmanager_peer_position`) evaluates all rules and broadcasts fired alerts to the
others; on its failure there is a brief evaluation gap. The broadcast queue holds 200 messages by default
(`ha_single_evaluation_alert_broadcast_queue_size`).

To avoid duplicate notifications entirely, the docs suggest a shared external Alertmanager.

## Alert state history
Grafana-managed rule state changes can be recorded in Loki, Prometheus, or both. Loki enables the Alerting History views:
```ini
[unified_alerting.state_history]
enabled = true
backend = loki
loki_remote_url = http://localhost:3100
```
Add the Loki data source in Grafana. The history view may query up to 30 days of data; the page suggests
`split_queries_by_interval: '24h'` and `max_query_parallelism: 32` in Loki `limits_config` and a separate Loki instance.
Prometheus backend (`backend = prometheus`, `prometheus_target_datasource_uid`; optional `prometheus_metric_name` default
`GRAFANA_ALERTS`, `prometheus_write_timeout` default 10s) needs Prometheus started with `--web.enable-remote-write-receiver`
and does not enable the History views. Both: `backend = multiple` with `primary = loki` and `secondaries = prometheus`.

## Recording rules (behaviour)
A recording rule evaluates on a fixed interval and writes one value as a new data point; the query must return a single
value (instant query, or range query plus a Reduce expression). Recorded metrics may differ from raw data. Alert rules on
recorded metrics should align their evaluation interval with the recording rule's. Grafana-managed recording rules can query
any data source supported by alerting and are the recommended type; data source-managed ones query Prometheus-based
data sources such as Mimir or Loki.

## Verify
- [ ] `grafana_alertmanager_cluster_members` equals the number of Grafana instances.
- [ ] With default HA, state history shows each rule evaluated by every instance.
- [ ] With Loki history, the Alerting History views show state changes.

## Checked
Checked 2026-11-07. Read in full: the Configure high availability page (Memberlist, Redis, Kubernetes, single-node evaluation, metrics,
duplicate notifications), the Configure alert state history page (Loki, Prometheus, multiple) and the Configure recording rules page. Removed
as not on these pages: the `/api/alertmanager/grafana/api/v2/status` peers check, the `[annotations.alerting] max_age` pruning
note, the whole "Simplified routing" section, and the `[recording_rules]` configuration block with the `grafanaManagedRecordingRules` toggle (the recording
rules page documents behaviour only; the Grafana-managed recording rule setup page was not read). Corrected: the headless service
and POD_IP details now follow the page's Kubernetes example. Not opened: the Docker Compose demos and Alerting meta-monitoring page.
Method: documentation only; no commands were run.
