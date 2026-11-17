---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-ha-cluster-setup
name: alertmanager-ha-cluster-setup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, alertmanager-ha, alertmanager-cluster, cluster-peer-flags, gossip-settings, alertmanagers-config, all-alertmanager-instances, notification-log, nflog, silence-replication, cluster-status, gossip-troubleshooting]
level: advanced
status: docs-checked
description: "Run Alertmanager HA: --cluster.* flags and gossip, pointing every Prometheus at all peers, nflog and silence replication, and diagnosing duplicate notifications."
sources: ["https://github.com/prometheus/alertmanager#high-availability", "https://prometheus.io/docs/alerting/latest/alertmanager/#high-availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager HA cluster

## Peers
```bash
alertmanager --config.file=am.yml --storage.path=/alertmanager \
  --cluster.listen-address=0.0.0.0:9094 \
  --cluster.peer=alertmanager-0.alertmanager-operated:9094 \
  --cluster.peer=alertmanager-1.alertmanager-operated:9094 \
  --cluster.peer=alertmanager-2.alertmanager-operated:9094 \
  --cluster.advertise-address=$(POD_IP):9094 \
  --cluster.peer-timeout=15s --cluster.pushpull-interval=1m --cluster.gossip-interval=200ms
```
- The three timing flags are shown at their defaults. `--cluster.listen-address` defaults to `0.0.0.0:9094`;
  an empty value disables HA mode. The port in it is the one to use in the other peers' `--cluster.peer`.
- Alertmanager 0.15 and higher need **both TCP and UDP** on the cluster port: open it in firewalls and expose it
  in containers for both protocols.
- `--cluster.advertise-address` is required if the instance has no address that is part of RFC 6890 with a
  default route.
- `--cluster.peer-timeout`: time to wait between peers to send notifications. Raise it if duplicates appear.

## Prometheus sends to ALL peers
```yaml
alerting:
  alertmanagers:
    - kubernetes_sd_configs: [{role: pod, namespaces: {names: [monitoring]}}]
      relabel_configs:
        - {source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_name], regex: alertmanager, action: keep}
        - {source_labels: [__meta_kubernetes_pod_container_port_number], regex: "9093", action: keep}
```
Never load balance traffic between Prometheus and its Alertmanagers: point Prometheus at the list of all of them,
because Alertmanager expects every alert to be sent to every peer.

## What replicates
- **Notification log (nflog)**: entries are gossiped between peers (metric
  `alertmanager_nflog_gossip_messages_propagated_total`).
- Not replicated: alerts themselves (that's why Prometheus sends to all) and config (deploy identically).

## Troubleshooting duplicates or gaps
```promql
alertmanager_cluster_failed_peers                # should stay 0
alertmanager_cluster_peer_info                   # constant 1, labelled by peer name
rate(alertmanager_nflog_gossip_messages_propagated_total[5m])
```
- Failed peers: network policy blocking 9094 on UDP or TCP, or a wrong advertise address.
- Duplicates with a healthy cluster: config differs between peers, or `peer-timeout` too low.

## Checked
2026-10-28. Confirmed in the Alertmanager README high availability section (`--cluster.*` flags and defaults, TCP and UDP
requirement since 0.15, advertise-address rule, do not load balance, send to all) and prometheus.io Alertmanager HA text, plus
Alertmanager source (`cmd/alertmanager/main.go` flags and `--storage.path`; metrics `alertmanager_cluster_failed_peers`,
`alertmanager_cluster_peer_info`, `alertmanager_nflog_gossip_messages_propagated_total`). Removed: `alertmanager_cluster_members`
and `alertmanager_peer_position` (not found in the source read), the Operator replicas claim, the silence-gossip and storage
persistence claims, the `/#/status` UI claim.
Method: documentation only; no commands were run.

## Verify
- [ ] `alertmanager_cluster_failed_peers` is 0 on every peer; stopping one peer still notifies exactly once.
- [ ] A silence created on one peer appears on the others.
