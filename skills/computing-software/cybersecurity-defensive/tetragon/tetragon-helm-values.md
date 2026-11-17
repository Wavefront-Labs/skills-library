---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-helm-values
name: tetragon-helm-values
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [helm-values]
level: advanced
status: docs-checked
description: "Key Tetragon Helm chart values for export, filtering, gRPC, metrics, process cache, rthooks and the operator, with defaults."
sources:
  - "https://tetragon.io/docs/reference/helm-chart/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Helm chart values

Goal: pick the right chart value. Set values with `--set key=value` on `helm install` or `helm upgrade` (chart from `https://helm.cilium.io`, `cilium/tetragon`).

## Agent (`tetragon.*`)

- `tetragon.image.tag` `v1.8.0`; `tetragon.hostProcPath` `/proc` (differs in kind-like environments).
- `tetragon.enableK8sAPI` `true`; `tetragon.clusterName` sets `cluster_name` in `GetEventsResponse`.
- `tetragon.enableProcessCred` / `tetragon.enableProcessNs` default `false`.
- `tetragon.processCacheSize` `65536`; `tetragon.processCacheGCInterval` `30s`; `tetragon.deletedPodCacheSize` `1024`.
- `tetragon.processAncestors.enabled`: comma-separated event types (base, kprobe, tracepoint, loader, uprobe, lsm, usdt); `base` is required by the others; `""` disables.
- `tetragon.cri.enabled` `false` with `cri.socketHostPath`; `tetragon.cgidmap.enabled` `false` (needs cri).

## Export and filters

- `tetragon.exportFilename` `tetragon.log` (empty string disables JSON export); `exportFileMaxSizeMB` `10`; `exportFileMaxBackups` `5`; `exportFileCompress` `false`; `exportFilePerm` `"600"`.
- `tetragon.exportRateLimit` `-1`: -1 off, 0 disables JSON export, positive = events per minute.
- `tetragon.exportAllowList`, `tetragon.exportDenyList` (the denylist is for file sinks only and does not filter gRPC output; its default drops health checks and namespaces "", cilium, kube-system), `tetragon.fieldFilters`, `tetragon.redactionFilters`.
- `export.mode` `stdout`; `exportDirectory` `/var/log/tetragon`.

## gRPC and health

- `tetragon.grpc.enabled` `true`; `tetragon.grpc.address` `unix:///var/run/tetragon/tetragon.sock` (a TCP address without TLS client verification exposes Tetragon).
- `tetragon.grpc.tls.enabled` `false`, `requireClientCert` `false`, `auto.method` `helm`|`cronJob`|`certmanager`, `server.existingSecret`.
- `tetragon.healthGrpc.enabled` `true`, port `6789`, interval `10`.

## Metrics

`tetragon.prometheus.enabled` `true`, port `2112`, `metricsLabelFilter` `namespace,workload,pod,binary`, `serviceMonitor.enabled` `false`, `scrapeInterval` `60s`. Operator: `tetragonOperator.prometheus.port` `2113`.

## Runtime hooks and operator

- `rthooks.enabled` `false`; `rthooks.interface` `oci-hooks` (CRI-O) or `nri-hook` (containerd); `rthooks.installDir` `/opt/tetragon`; `rthooks.failAllowNamespaces`, `rthooks.failAllowNamespacesRegex`.
- `tetragonOperator.enabled` `true`, `replicas` `1`, `tracingPolicy.enabled` `true`, `crds.installMethod` `operator` (or `helm`, `none`).
- `hostNetwork` `true`: Tetragon must be on the host network for process visibility.

## Checked

Date: 2026-11-07

Helm chart reference (about 28 KB) read in full; every default listed was matched. Clarified that the file-sinks-only note belongs to the denylist. The fieldFilters and redactionFilters description cells are truncated on the page.

Method: documentation only; no commands were run.
