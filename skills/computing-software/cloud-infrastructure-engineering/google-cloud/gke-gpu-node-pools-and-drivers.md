---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-gpu-node-pools-and-drivers
name: gke-gpu-node-pools-and-drivers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-gpu-node-pools, gke-gpu-drivers, nvidia-gpu, gpu-time-sharing, mig-partitioning, accelerators]
level: practitioner
status: docs-checked
description: "Create GKE Standard GPU node pools with automatic NVIDIA driver installation, schedule pods with GPU limits, share GPUs (time-sharing, MIG), and debug pending GPU pods."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpus", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/timesharing-gpus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE GPU node pools and drivers

## Create
```bash
gcloud container node-pools create l4-pool --cluster=ml --location=us-central1 \
  --node-locations=us-central1-a,us-central1-b \
  --machine-type=g2-standard-8 \
  --accelerator=type=nvidia-l4,count=1,gpu-driver-version=latest \
  --enable-autoscaling --min-nodes=0 --max-nodes=10 --spot
```
`gpu-driver-version=default|latest|disabled`: `default` installs the default driver for the GKE version (the default option from 1.30.1-gke.1156000), `latest` installs the newest driver (Container-Optimized OS nodes only), `disabled` skips automatic installation and you install a driver yourself. When a GPU node pool joins a cluster that has non-GPU pools, GKE adds the taint `nvidia.com/gpu=present:NoSchedule`, and the ExtendedResourceToleration admission controller adds the toleration to Pods that request GPUs.

## Pod
```yaml
resources:
  limits: {nvidia.com/gpu: 1}
nodeSelector:
  cloud.google.com/gke-accelerator: nvidia-l4
```

## Sharing GPUs
- **Time-sharing**: `--accelerator=type=nvidia-l4,count=1,gpu-sharing-strategy=time-sharing,max-shared-clients-per-gpu=4`; memory limits are not enforced on GPUs.
- **Multi-instance GPU**: `gpu-partition-size=<PARTITION_SIZE>` in the `--accelerator` flag (see the GKE multi-instance GPU guide for supported sizes).
- **NVIDIA MPS**: see the GKE MPS guide for its `gpu-sharing-strategy` value.

## Debugging pending pods
A Pod stuck Pending with insufficient `nvidia.com/gpu` means no GPU node has capacity: with autoscaling from 0, check GPU quota in the region and capacity in the zones. If GPUs are visible but drivers are missing, check the driver installation (or that `gpu-driver-version` is not `disabled`).

## Gotchas
- GPU machine types must match the accelerator (G2 for L4, A2 for A100 40 GB, A3 for H100).
- Container-Optimized OS is recommended for GPU nodes; Ubuntu has minimum driver version requirements per GPU.
- Spot nodes can be reclaimed at any time; checkpoint training jobs.
- Autopilot: no node pools, request via selectors and limits only.

## Verify
- [ ] A Pod requesting `nvidia.com/gpu: 1` with the accelerator node selector schedules on the GPU pool and can run `nvidia-smi`.

## Checked

2026-10-24, GKE GPU and GPU time-sharing pages on docs.cloud.google.com. Confirmed: `--accelerator type=...,count=...,gpu-driver-version=...` and its three values, taint and node selector keys, ExtendedResourceToleration, machine series per GPU, COS recommendation and Ubuntu driver requirements, time-sharing flags and the statement that GPU memory limits are not enforced, `gpu-partition-size` flag name. Removed unconfirmed claims: partition size example, MPS value, scheduler and quota error strings, `nvidia-gpu-device-plugin` pod name, the CUDA image tag.

Method: documentation only; no commands were run.
