---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-allocatable-and-resource-reservations
name: node-allocatable-and-resource-reservations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, node-allocatable, kube-reserved, system-reserved, enforce-node-allocatable, node-stability]
level: advanced
status: docs-checked
description: "Size kubeReserved, systemReserved and eviction thresholds so Allocatable leaves headroom for the OS and kubelet, preventing node freezes and system OOMs under pod pressure."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node allocatable and resource reservations

`Allocatable = Capacity - kubeReserved - systemReserved - evictionHard` (the docs' worked example: 32Gi
memory, 2Gi + 1Gi reserved and a 500Mi eviction threshold give 28.5Gi). The scheduler treats
Allocatable as the capacity available for pods. With no reservations, pods can consume memory the kubelet,
containerd and sshd need → node goes NotReady or the kernel OOM-kills the kubelet.

## Configure
```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
kubeReserved: {cpu: 200m, memory: 1Gi, ephemeral-storage: 1Gi}
systemReserved: {cpu: 200m, memory: 500Mi, ephemeral-storage: 1Gi}
evictionHard: {memory.available: 200Mi, nodefs.available: 10%, imagefs.available: 15%}
enforceNodeAllocatable: [pods]            # default; add kube-reserved/system-reserved only with cgroups below
# kubeReservedCgroup: /kube.slice
# systemReservedCgroup: /system.slice
```
- `enforceNodeAllocatable: [pods]` (the default) enforces Allocatable across pods by evicting pods when
  their combined usage exceeds it; this is what protects the system. Enforcing `kube-reserved` /
  `system-reserved` as well needs `kubeReservedCgroup` / `systemReservedCgroup` and can leave system
  services CPU starved, OOM killed or unable to fork, so the docs advise it only for exhaustively profiled
  nodes. Enforcing only the compressible resources (`kube-reserved-compressible`,
  `system-reserved-compressible`) is less disruptive.

## Sizing
`kubeReserved` is typically a function of pod density on the node, and `pid` can be reserved too. Measure
the kubelet and runtime under load rather than copying a provider's formula.

## Inspect
```bash
kubectl describe node <n>                          # Capacity and Allocatable sections
kubectl get node <n> -o jsonpath='{.status.allocatable}'
```

## Gotchas
- Changing reservations shrinks Allocatable on existing nodes; already-running pods are not
  evicted, but the node may become overcommitted relative to requests.

## Verify
- [ ] Under a memory stress test filling pods, the node stays Ready and evicts pods rather than
      OOM-killing kubelet/containerd (check the node's kernel log for OOM kills).
- [ ] `describe node` shows Allocatable < Capacity by the configured amounts.

## Checked
2026-10-23, against the Kubernetes website reserve-compute-resources task (Allocatable formula and worked example, enforceNodeAllocatable default `pods` and eviction-based enforcement, cgroup requirement and risk guidance for kube/system-reserved, compressible-only enforcement, pid reservation) and the kubelet defaults source (EnforceNodeAllocatable defaults to pods). GKE and EKS reservation formulas, the Windows figure, the kubectl top statement and the kubepods memory.max statement were removed as unconfirmed.
Method: documentation only; no commands were run.
