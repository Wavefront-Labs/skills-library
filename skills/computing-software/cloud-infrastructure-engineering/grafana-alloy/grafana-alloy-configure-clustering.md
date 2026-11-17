---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-configure-clustering
name: grafana-alloy-configure-clustering
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [clustering-helm, controllertype, statefulset, clusterjoin-addresses, clustername, clusterrejoin-interval, clustermax-join-peers]
level: practitioner
status: docs-checked
description: "Enable Alloy clustering via Helm (statefulset) or flags, with peer discovery, advertise address, TLS, rejoin and wait-for-size settings."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/configure/clustering/configure-alloy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure Alloy for clustering

Cluster mode lets instances find each other; to share work you must also enable clustering per component.

## Helm
For multiple replicas set `controller.type` to `statefulset` (stable pod identity for peer discovery); use a DaemonSet only for node-local data. Then:

```yaml
alloy:
  clustering:
    enabled: true
```
Run `helm upgrade --namespace NAMESPACE RELEASE grafana/alloy -f values.yaml` and check the UI **Clustering** page lists all nodes.

## Flags
Pass `--cluster.enabled` plus `--cluster.join-addresses` or `--cluster.discover-peers`:

```bash
alloy run config.alloy --cluster.enabled \
  --cluster.join-addresses=alloy-1:7946,alloy-2:7946,alloy-3:7946 \
  --cluster.wait-for-size=3 --cluster.wait-timeout=5m
```
The first node may omit discovery or join itself. Peers speak HTTP/2 on the built-in server, so each node must accept connections on `--server.http.listen-addr` and the advertised address. If `--cluster.advertise-address` is unset, Alloy infers one from `--cluster.advertise-interfaces` (default `eth0,en0`); on Windows set one explicitly. Startup fails if no address can be determined.

## Tuning
- `--cluster.rejoin-interval` (default `60s`) rediscovers peers and heals split brain; `0s` discovers only at startup.
- `--cluster.max-join-peers` (default `5`; `0` removes the limit).
- `--cluster.name` stops clusters merging; a wrong name yields `failed to join memberlist`.
- TLS uses `--cluster.enable-tls` and `--cluster.tls-*`.
- With `--cluster.wait-for-size` left at `0`, nodes may scrape before peers join, causing duplicate series and out-of-order errors at remote write.

## Checked
2026-11-04: confirmed against the Configure Alloy for clustering and alloy run CLI reference. Removed: nothing.
Method: documentation only; no commands were run.
