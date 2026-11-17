---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pvc-usage-monitoring-and-alerts
name: pvc-usage-monitoring-and-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, persistentvolumeclaim, kubelet-volume-stats, prometheus, storage]
level: practitioner
status: docs-checked
description: "Monitor PVC fill levels and inode use with kubelet_volume_stats metrics, alert before volumes fill, and handle drivers that report no stats."
sources: ["https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://github.com/kubernetes-monitoring/kubernetes-mixin/blob/master/alerts/storage_alerts.libsonnet", "https://raw.githubusercontent.com/kubernetes/kubelet/master/pkg/apis/stats/v1alpha1/types.go", "https://raw.githubusercontent.com/container-storage-interface/spec/master/spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PVC usage monitoring

## Metrics (from kubelet, labelled by namespace and persistentvolumeclaim)
- `kubelet_volume_stats_capacity_bytes`
- `kubelet_volume_stats_used_bytes`
- `kubelet_volume_stats_available_bytes`
- `kubelet_volume_stats_inodes`, `_inodes_used`, `_inodes_free`

Scraped from the kubelet `/metrics` endpoint (kube-prometheus-stack does this).

## Alerts (kubernetes-mixin style)
```yaml
- alert: PVCFillingUp
  expr: |
    kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes < 0.15
    and predict_linear(kubelet_volume_stats_available_bytes[6h], 4*24*3600) < 0
  for: 1h
- alert: PVCAlmostFull
  expr: kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes < 0.03
  for: 1m
- alert: PVCInodesLow
  expr: kubelet_volume_stats_inodes_free / kubelet_volume_stats_inodes < 0.05
```
The mixin's version uses a 6h sampling window for the prediction (`volumeFullPredictionSampleTime`), a 3%
(critical, 1m) and 15% (warning, 1h) free-space threshold, and excludes `ReadOnlyMany` volumes and PVCs
matched by its `pvExcludedSelector` on `kube_persistentvolumeclaim_labels`.

## Ad hoc
```bash
kubectl exec <pod> -- df -h /data
kubectl get --raw /api/v1/nodes/<node>/proxy/stats/summary | jq '.pods[].volume[]? | select(.pvcRef) | {pvc: .pvcRef.name, used: .usedBytes, cap: .capacityBytes}'
```

## Gaps
- Volume stats come from drivers that implement the CSI `NodeGetVolumeStats` call (the `GET_VOLUME_STATS`
  node capability); a driver without it reports nothing. Fall back to app metrics or storage
  backend metrics.
- For block volumes (`volumeMode: Block`) the CSI spec lets a driver omit `used` and `available`.

## Response
Expand (if `allowVolumeExpansion`), clean data, or move to a bigger volume; for databases,
expand well before 90% because compaction needs headroom.

## Checked
2026-10-28. Confirmed: the `kubelet_volume_stats_*` metric names against the Kubernetes metrics reference;
the alert shapes (15% free with a 4-day `predict_linear` over a 6h window, warning for 1h; 3% free, critical
for 1m; `ReadOnlyMany` exclusion; label-based exclusion) against the kubernetes-mixin `storage_alerts.libsonnet`;
`pvcRef`, `capacityBytes` and `usedBytes` in the kubelet stats summary types; `NodeGetVolumeStats`,
`GET_VOLUME_STATS` and the block-mode note against the CSI spec. Removed: the claim that NFS drivers report
nothing and that block volumes have no stats at all.
Method: documentation only; no commands were run.
