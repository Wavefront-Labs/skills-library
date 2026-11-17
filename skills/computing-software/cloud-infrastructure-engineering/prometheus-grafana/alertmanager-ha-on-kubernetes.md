---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-ha-on-kubernetes
name: alertmanager-ha-on-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager-statefulset, alertmanager-peers-kubernetes, alertmanager-ha, alertmanager-cluster, prometheus-operator]
level: practitioner
status: docs-checked
description: "Run a multi-replica Alertmanager cluster on Kubernetes: --cluster.* flags, port 9094 over TCP and UDP, the Operator's replicas setting, and pointing Prometheus at every replica."
sources: ["https://prometheus.io/docs/alerting/latest/alertmanager/#high-availability", "https://prometheus-operator.dev/docs/developer/alerting/", "https://prometheus-operator.dev/docs/platform/high-availability/", "https://github.com/prometheus/alertmanager#high-availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager HA on Kubernetes

## With the Prometheus Operator
The Operator builds a highly available Alertmanager cluster when `replicas` is greater than 1 (Operator HA page):
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Alertmanager
metadata:
  name: example
spec:
  replicas: 3
```
Prometheus instances send alerts to all configured Alertmanagers, and the Alertmanagers form a gossip-based cluster that replicates silences and the notification log. The Operator also manages Alertmanager discovery via the Kubernetes API for Prometheus. In the Prometheus CR, the Alertmanagers are listed under `spec.alerting.alertmanagers` (entries with `namespace`, `name`, `port: web`, as in the Operator alerting guide).

## Without the Operator (key flags)
Clustering is enabled by default and configured with `--cluster.*` flags (Alertmanager README):
- `--cluster.listen-address` default `0.0.0.0:9094`; an empty string disables HA mode.
- `--cluster.peer` is the initial peers; repeat the flag for each additional peer. The port in `--cluster.listen-address` is the port to use in the other peers' `--cluster.peer`.
- `--cluster.advertise-address` is required if the instance has no IP address that is part of RFC 6890 with a default route.
```
--cluster.listen-address=0.0.0.0:9094
--cluster.peer=<alertmanager-0-host>:9094
--cluster.peer=<alertmanager-1-host>:9094
--cluster.peer=<alertmanager-2-host>:9094
```
On Alertmanager 0.15 and higher both UDP and TCP are needed for the cluster to work: allow the clustering port for both protocols in any firewall, and expose it for both protocols in a container.

## Prometheus side
Do not load balance between Prometheus and its Alertmanagers; point Prometheus at a list of all of them, because Alertmanager expects every alert to be sent to every instance:
```yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets: [alertmanager1:9093, alertmanager2:9093, alertmanager3:9093]
```

## Verify
- [ ] Prometheus lists every Alertmanager replica individually (not one load-balanced address).
- [ ] The cluster port is reachable between replicas on both TCP and UDP.

## Checked
Date: 2026-11-07. Read in full: the Alertmanager concepts page (High Availability section), the Alertmanager GitHub README (High Availability section with the `--cluster.*` flag list, default `0.0.0.0:9094`, TCP and UDP note, static_configs example), the Operator "Alerting Routes" guide and the Operator High Availability page (replicas > 1 gives an HA cluster; gossip replicates silences and notification log). Removed as unconfirmed by those pages: the StatefulSet/`alertmanager-operated` service/auto-generated peer flags claim, storage and anti-affinity YAML, `publishNotReadyAddresses`, the kubernetes_sd relabel recipe, the PodDisruptionBudget, NetworkPolicy and ClusterIP gotchas, the `alertmanager_cluster_members` metric and the delete-a-pod verify step. Not opened: the Operator API reference.
Method: documentation only; no commands were run.
