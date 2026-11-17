---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.gpu-utilisation
name: gpu-utilisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimization, gpu-utilisation, gpu-costs, dcgm, mig, time-slicing, ai-finops, kubernetes]
level: advanced
status: docs-checked
description: "Raise GPU utilisation to cut cost: measure with DCGM and nvidia-smi, right-size GPU type, share GPUs via MIG or time-slicing, batch inference, and use spot for training."
sources: ["https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html", "https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html", "https://www.finops.org/wg/finops-for-ai-overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU utilisation optimisation

GPU instances are among the most expensive cloud compute and are often idle or underused: notebooks left running,
inference replicas sized for peak, small models on large GPUs.

## Measure
- Spot checks with `nvidia-smi` on the node.
- Fleet: NVIDIA DCGM (and its exporter) into your metrics system. Prefer profiling metrics such as
  `DCGM_FI_PROF_SM_ACTIVE` over the coarse GPU-utilisation field, which only says a kernel was running.
- Cost view: GPU cost per node-hour x (1 - utilisation) = idle cost; report per team.

## Levers
1. **Kill idle**: auto-stop notebooks and dev GPU instances when idle; TTL on experiment clusters.
2. **Right GPU type**: match GPU memory (model weights plus working memory) and throughput per currency unit to
   the workload rather than defaulting to the largest GPU.
3. **Share GPUs** (NVIDIA GPU Operator docs):
   - **MIG** partitions a supported GPU into predefined instances, each with memory and fault isolation at the
     hardware layer. Good for many small services.
   - **Time-slicing** lets several pods share one GPU through replicas set in the device plugin config. Unlike MIG there
     is no memory or fault isolation between replicas. It also works on older GPUs without MIG, and can be combined
     with MIG.
4. **Batch inference** so each GPU serves more requests per second.
5. **Autoscale inference** on a load metric such as queue depth, scaling to zero where cold start allows.
6. **Training**: checkpoint so interruptible capacity can be used; keep data loading from starving GPUs.
7. **Capacity commitments** only for the proven steady baseline.

## Gotchas
- A high coarse utilisation figure can still mean poor use; check SM-active style profiling metrics.
- MIG layouts are predefined per GPU and need planning per node pool.
- Time-slicing gives no memory isolation; one pod can affect others.

## Verify
- [ ] GPU idle cost per team reported weekly.
- [ ] Inference services have measured throughput per GPU and a sharing/batching decision.

## Checked
2026-11-01. Confirmed in the NVIDIA GPU Operator GPU sharing page (time-slicing replicas, no memory or fault isolation,
works on older GPUs, combinable with MIG; MIG memory and fault isolation at the hardware layer) and the DCGM feature
overview (`DCGM_FI_PROF_SM_ACTIVE`). Removed: other DCGM field names and the nvidia-smi query string (not on pages
read), MIG profile names and GPU model lists, MPS, Triton/vLLM, quantisation formats, spot guidance specifics and the
dollar-per-hour claim. The MIG user guide returned almost no text and was dropped from sources.
Method: documentation only; no commands were run.
