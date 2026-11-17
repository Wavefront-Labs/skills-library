---
id: computing-software.cloud-infrastructure-engineering.garage.prometheus-cluster-health-metrics
name: prometheus-cluster-health-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [cluster-healthy, cluster-available, cluster-connected-nodes, prometheus]
level: practitioner
status: docs-checked
description: "Read the cluster_* and storage Prometheus metrics Garage exports to alert on node loss and quorum."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/monitoring/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage exports Prometheus metrics at the `/metrics` endpoint of its admin API. The configuration page says a `metrics_token` can protect it, and `metrics_require_token = true` (since v2.0.0) makes a token always required.

System metrics: `garage_build_info{version=...}` shows the version running on a node (useful during upgrades), `garage_replication_factor`, and `garage_local_disk_avail` / `garage_local_disk_total`, each reported with `volume="data"` and `volume="metadata"`.

Cluster health gauges:

- `cluster_healthy`: 1 when all storage nodes are connected.
- `cluster_available`: 1 when all requests can be served even if some storage nodes are disconnected.
- `cluster_connected_nodes` and `cluster_known_nodes`.
- `cluster_layout_node_connected` per node, with labels for id, role_capacity, role_gateway and role_zone.
- `cluster_layout_node_disconnected_time`: seconds since the last connection to each node.
- `cluster_storage_nodes` and `cluster_storage_nodes_ok`.
- `cluster_partitions` (always 256), `cluster_partitions_all_ok` and `cluster_partitions_quorum`.

A sensible reading: `cluster_healthy` of 0 with `cluster_available` of 1 means nodes are down but service continues; `cluster_available` of 0 means some requests cannot be served. The `cluster_partitions_quorum` value shows how many partitions still have a quorum.

In the sample output `garage_local_disk_total{volume="data"}` is 763063566336 (the page does not state the unit) and `garage_build_info` is exposed as a counter with value 1.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Monitoring. Confirmed on the monitoring page: every metric name, type and description listed, the labels of `cluster_layout_node_connected`, and `cluster_partitions` always 256. Confirmed on the configuration page: the `/metrics` endpoint, `metrics_token` and `metrics_require_token`. Removed: the claim that disk gauges are in bytes and the 763 GB figure (the page gives no unit), and reworded the `cluster_available` 0 reading to match the metric description.

Method: documentation only; no commands were run.
