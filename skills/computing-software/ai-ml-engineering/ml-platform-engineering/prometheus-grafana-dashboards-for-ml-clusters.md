---
id: computing-software.ai-ml-engineering.ml-platform-engineering.prometheus-grafana-dashboards-for-ml-clusters
name: prometheus-grafana-dashboards-for-ml-clusters
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, grafana-ml, prometheus, dcgm-exporter, gpu-monitoring, kubernetes]
level: practitioner
status: draft
description: "Build Prometheus and Grafana monitoring for GPU ML clusters: DCGM exporter metrics, per-job and per-team views via labels, Kueue and storage panels, recording rules and alerts."
sources:
  - https://docs.nvidia.com/datacenter/cloud-native/gpu-telemetry/latest/dcgm-exporter.html
  - https://github.com/NVIDIA/dcgm-exporter
  - https://kueue.sigs.k8s.io/docs/reference/metrics/
  - https://grafana.com/grafana/dashboards/12239-nvidia-dcgm-exporter-dashboard/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Prometheus / Grafana dashboards for ML clusters

**Goal:** platform and ML teams see GPU health, utilisation by job and team, queueing and storage at a glance, and get alerted on failing hardware and wasted GPUs.

## Collect
- **DCGM exporter** (DaemonSet, included with the NVIDIA GPU Operator): per-GPU metrics labelled with pod, namespace and container.
- **kube-state-metrics:** pod phases, requests, job status; join to get team/job labels.
- **node-exporter:** CPU, memory, disk, network (EFA via additional exporters).
- **Kueue metrics:** `kueue_pending_workloads`, `kueue_admitted_active_workloads`, cluster queue usage.
- Training jobs push throughput (tokens/s, samples/s, step time) as custom metrics.

## Key GPU metrics
| Metric | Meaning |
|---|---|
| `DCGM_FI_DEV_GPU_UTIL` | % time a kernel ran (coarse; 100% does not mean efficient) |
| `DCGM_FI_PROF_SM_ACTIVE`, `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` | how busy SMs and tensor cores really are |
| `DCGM_FI_DEV_FB_USED` | GPU memory used |
| `DCGM_FI_DEV_POWER_USAGE`, `DCGM_FI_DEV_GPU_TEMP` | power and thermals |
| `DCGM_FI_DEV_XID_ERRORS` | last XID error code (hardware/driver faults) |
| `DCGM_FI_PROF_NVLINK_TX_BYTES` / PCIe counters | interconnect traffic |
Profiling (`DCGM_FI_PROF_*`) metrics need to be enabled in the exporter's counters CSV.

## Recording rules
```yaml
- record: namespace:gpu_util:avg
  expr: avg by (namespace) (DCGM_FI_DEV_GPU_UTIL)
- record: namespace:gpus_allocated:count
  expr: count by (namespace) (DCGM_FI_DEV_GPU_UTIL{pod!=""})
```
Pre-aggregate high-cardinality per-GPU series for long-range dashboards.

## Dashboards
1. **Cluster:** GPUs allocated vs idle vs total, utilisation heatmap by node, XID errors, temperature.
2. **Team/namespace:** GPU-hours, average SM activity, idle allocated GPUs (allocated with util < 5% for 1h).
3. **Job:** per-rank GPU util and memory, step time, throughput, straggler detection (rank with lower util).
4. **Queues:** pending workloads and wait time per cluster queue.
5. **Storage:** FSx/NFS throughput and latency during training.

## Alerts
- Any non-zero XID of fatal classes (e.g. 48, 63, 64, 79) -> cordon node, runbook.
- GPU temperature or power throttling sustained.
- Allocated GPU idle > 2 hours (cost waste) -> notify owner.
- Job throughput drop > 20% vs its baseline.
- Queue wait time above target.

## Verify
- [ ] Dashboards filter by namespace, job and node.
- [ ] XID alert tested (inject via test metric).
- [ ] Idle-GPU report reaches owners weekly.
