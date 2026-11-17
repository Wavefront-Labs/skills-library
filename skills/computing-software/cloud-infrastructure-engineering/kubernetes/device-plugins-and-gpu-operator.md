---
id: computing-software.cloud-infrastructure-engineering.kubernetes.device-plugins-and-gpu-operator
name: device-plugins-and-gpu-operator
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, device-plugin, nvidia-gpu-operator, gpu, extended-resources, mig, time-slicing, node-feature-discovery]
level: advanced
status: docs-checked
description: "Schedule GPUs and other devices: device plugins and extended resources, NVIDIA GPU Operator install, MIG and time-slicing sharing, GPU node taints, and validating the stack."
sources: ["https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/", "https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/", "https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html", "https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html", "https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-operator-mig.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device plugins and the NVIDIA GPU Operator

## How devices are scheduled
A device plugin (DaemonSet) registers with the kubelet over gRPC
(`/var/lib/kubelet/device-plugins/kubelet.sock`) and advertises an **extended resource**
(`nvidia.com/gpu: 8`) in node capacity. Pods request it in **limits** (requests default to
limits; must be integers; no overcommit):
```yaml
resources:
  limits: {nvidia.com/gpu: 1}
tolerations:
- {key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}
```
Taint GPU nodes (and tolerate the taint in GPU pods) so non-GPU pods don't consume their CPU/memory.

## GPU Operator
Manages driver (containerised), container toolkit, device plugin, DCGM exporter, GPU Feature
Discovery and MIG manager (each has an `enabled` switch in the chart values).
```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm install gpu-operator nvidia/gpu-operator -n gpu-operator --create-namespace \
  --set driver.enabled=false           # only when the nodes already have the NVIDIA driver; default true (Operator installs it)
kubectl get pods -n gpu-operator      # all Running/Completed, incl. nvidia-operator-validator
```
On managed clusters, follow NVIDIA's provider-specific pages (Amazon EKS, Google GKE). If a node already has a
driver and you omit `driver.enabled=false`, the driver pod is terminated on that node, per the getting-started guide.

## Sharing GPUs
- **MIG** (Ampere and later, such as A100): hardware partitions with memory and fault isolation. The chart's
  `mig.strategy` is `single` (default in the chart values) or `mixed`; with `mixed`, label
  nodes `nvidia.com/mig.config=all-1g.10gb` and pods request per-profile resources such as `nvidia.com/mig-1g.10gb: 1`.
- **Time-slicing**: a ConfigMap whose entry holds `sharing.timeSlicing.resources` with `name: nvidia.com/gpu` and
  `replicas: 4`, referenced from the ClusterPolicy (`spec.devicePlugin.config.name`, with `default` for a
  cluster-wide default or a node label `nvidia.com/device-plugin.config=<name>`); unlike MIG there is **no
  memory or fault isolation** between replicas.

## Validate
```bash
kubectl describe node <gpu-node> | grep -A3 nvidia.com/gpu
kubectl run cuda --rm -it --restart=Never --image=nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0-ubuntu22.04 \
  --overrides='{"spec":{"tolerations":[{"key":"nvidia.com/gpu","operator":"Exists"}],"containers":[{"name":"cuda","image":"nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0-ubuntu22.04","resources":{"limits":{"nvidia.com/gpu":1}}}]}}'
# expect "Test PASSED"
```
The DCGM exporter (enabled by default in the chart) exposes GPU metrics for dashboards.

## Verify
- [ ] Node allocatable shows expected GPUs; sample pod passes; idle GPU alert in place.

## Checked

Checked on 2026-10-26 against the Kubernetes docs `device-plugins.md` and `scheduling-gpus.md` (`kubernetes/website`), the `NVIDIA/gpu-operator` chart values (`deployments/gpu-operator/values.yaml`, latest release v26.7.2, 2026-10-14) and the NVIDIA GPU Operator pages (getting started, GPU sharing, MIG) on docs.nvidia.com.
Confirmed: device plugin DaemonSet registering over `/var/lib/kubelet/device-plugins/kubelet.sock`; extended resources are integer-only and cannot be overcommitted; GPUs belong in `limits`; Helm repo `https://helm.ngc.nvidia.com/nvidia`; `driver.enabled` (default true) and the driver-pod behaviour on preinstalled drivers; `mig.strategy` default `single`; `nvidia.com/mig.config=all-1g.10gb` label and `nvidia.com/mig-1g.10gb` resources with `mixed`; time-slicing ConfigMap shape and ClusterPolicy patch; no isolation between time-sliced replicas; cuda-sample validation image and "Test PASSED".
Corrected: the sample image tag now carries the `-ubuntu22.04` suffix.
Removed as unconfirmed: GKE and EKS driver specifics, H100 MIG wording, the MPS bullet, the DRA GA release claim, the DCGM metric name, the kernel-upgrade and autoscaler gotchas, and the `gpu.product` node selector.

Method: documentation only; no commands were run.
