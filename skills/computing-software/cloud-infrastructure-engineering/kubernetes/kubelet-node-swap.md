---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-node-swap
name: kubelet-node-swap
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet-config, node-swap, limitedswap, kubelet]
level: practitioner
status: docs-checked
description: "Enable swap on Linux nodes with the kubelet's memorySwap LimitedSwap behaviour: which pods may swap, cgroup v2 requirement, sizing and risks."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/swap-memory-management/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubelet/config/v1beta1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node swap support

Historically the kubelet refused to run with swap on. The NodeSwap feature (beta from 1.28, on by default from 1.30,
stable in 1.34) allows it with controlled behaviour.

## Configure
```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
failSwapOn: false
memorySwap:
  swapBehavior: LimitedSwap      # or NoSwap (default when swap is on)
```
Requirements: swap provisioned on the node and the kubelet restarted with `failSwapOn: false`. On cgroup v2 the
runtime applies the limit through `memory.swap.max`.

## Behaviour
- `NoSwap`: the node has swap but Kubernetes workloads do not use it (system daemons may).
- `LimitedSwap`: only **Burstable** pods with memory requests may swap, proportionally to their
  memory request vs node memory. Guaranteed and BestEffort pods, and high-priority
  (system-critical) pods, never swap.
- A Burstable container whose memory request equals its limit does not get swap.

## Sizing and risks
- Swap trades OOM kills for latency. Latency-sensitive services should be Guaranteed so they
  never swap.
- The project recommends encrypted swap (encryption is an OS concern, not the kubelet's) and a dedicated disk
  so workloads do not interfere with system processes; swapped pages otherwise reach disk.
- Eviction: set the kubelet eviction thresholds slightly below the node's `vm.min_free_kbytes` so
  pods are evicted before the kernel OOM killer runs.
- To stop system services swapping, set `memory.swap.max=0` on the system slice cgroup.

## Verify
```bash
kubectl get --raw /api/v1/nodes/<n>/proxy/configz | jq '.kubeletconfig.memorySwap'
kubectl get node <n> -o jsonpath='{.status.nodeInfo.swap.capacity}'   # unset when no swap is provisioned
```

## Checked

2026-10-26: kubernetes.io swap-memory-management page (v1.37 docs, kubernetes/website main 2026-10-25), the NodeSwap feature-gate page and the kubelet config API source. Confirmed: stage history (beta 1.28, default on 1.30, stable 1.34), failSwapOn default true, swapBehavior values and NoSwap default, LimitedSwap Burstable-only rule, node.status.nodeInfo.swap.capacity, memory.swap.max, eviction advice. Removed the unconfirmed cgroup v2 hard requirement, OOM remark and host cgroup path.

Method: documentation only; no commands were run.
