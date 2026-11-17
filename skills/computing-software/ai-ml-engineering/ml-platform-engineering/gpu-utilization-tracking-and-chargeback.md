---
id: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-utilization-tracking-and-chargeback
name: gpu-utilization-tracking-and-chargeback
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu-chargeback, showback, gpu-utilization, opencost, dcgm-exporter, cost-allocation, finops]
level: practitioner
status: draft
description: "Attribute GPU cost to teams and jobs: allocated vs used GPU-hours from DCGM and Kubernetes labels, idle GPU detection, OpenCost/Kubecost and showback reports."
sources:
  - https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html
  - https://www.opencost.io/docs/
  - https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html#profiling-metrics
  - https://www.finops.org/framework/capabilities/allocation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU utilization tracking and chargeback

**Goal:** every GPU-hour is attributed to a team/project, and teams see how much of what they reserve they actually use.

## Measure two things
1. **Allocated GPU-hours:** GPUs requested by pods/jobs x wall time. This is what you pay for.
2. **Used:** how busy those GPUs were. From dcgm-exporter:
   - `DCGM_FI_DEV_GPU_UTIL` - % of time a kernel was running. Coarse: one tiny kernel = "100%".
   - `DCGM_FI_PROF_SM_ACTIVE` / `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` - fraction of SMs / tensor cores busy. Much better efficiency signals.
   - `DCGM_FI_DEV_FB_USED` - memory in use.

dcgm-exporter adds `namespace`, `pod` and `container` labels when the kubelet pod-resources API is mapped in, so you can join metrics to workload owners.

## Attribution
- Enforce labels on every workload: `team`, `project`, `cost-center` (admission policy via Kyverno/Gatekeeper rejecting unlabeled GPU pods).
- Slurm: `sacct --format=User,Account,AllocTRES,Elapsed` gives allocated GPU-hours per account.
- OpenCost/Kubecost allocate node cost (including GPU price per hour) to pods by requests; configure custom GPU pricing for on-prem.

## Idle GPU detection
PromQL for GPUs allocated but idle for the last hour:
```
avg_over_time(DCGM_FI_DEV_GPU_UTIL{pod!=""}[1h]) < 5
```
Typical offenders: notebooks left running with a GPU, crashed jobs holding a pod, inference replicas sized for peak. Act with notebook culling (JupyterHub idle culler), job TTLs, and autoscaling minimums.

## Showback before chargeback
Start with a weekly report per team: allocated GPU-hours, cost, average SM-active, idle hours. Only move to actual chargeback once labels are reliable and teams have tools to reduce waste; otherwise you create disputes instead of savings.

## Gotchas
- MIG slices and time-sliced GPUs: attribute the fraction, not the whole GPU; dcgm-exporter reports per MIG instance with `GPU_I_ID`.
- Reserved/committed capacity is paid whether used or not; charge it as a shared overhead or to the team that requested the reservation.
- `nvidia-smi` utilisation looks high for memory-bound or tiny-kernel workloads; don't use it alone to judge efficiency.

## Verify
- [ ] >95% of GPU-hours carry a team label.
- [ ] Idle-GPU alert fires on a test notebook left open.
- [ ] Monthly report reconciles to the cloud bill within a few percent.
