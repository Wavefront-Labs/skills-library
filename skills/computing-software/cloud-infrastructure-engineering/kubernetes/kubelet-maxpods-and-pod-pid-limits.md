---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-maxpods-and-pod-pid-limits
name: kubelet-maxpods-and-pod-pid-limits
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet-config, maxpods, podpidslimit, kubelet, too-many-pods]
level: practitioner
status: docs-checked
description: "Size kubelet maxPods against pod CIDR and CNI IP limits, set podPidsLimit to stop fork bombs, and verify node capacity and allocatable pods."
sources: ["https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://kubernetes.io/docs/concepts/policy/pid-limiting/", "https://kubernetes.io/docs/setup/best-practices/cluster-large/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maxPods and podPidsLimit

## maxPods
```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
maxPods: 110          # default; Kubernetes is designed for no more than 110 pods per node
podPidsLimit: 4096      # default is -1 (node allocatable PID limit)
```
Constraints to check before raising maxPods:
- Pod CIDR per node: kube-controller-manager `--node-cidr-mask-size` (default /24 = 254 IPs
  for IPv4). maxPods must be below the usable IPs, with headroom for churn.
- CNI and cloud IP limits: some CNIs and managed node pools cap pods per node below `maxPods`; read
  your provider's documentation for the limit and when it is set.
- Kubelet and runtime overhead grows with pod count; the docs' design target is at most 110 pods per node.

## podPidsLimit
Caps PIDs per pod; a fork bomb or thread leak then fails inside that pod instead of exhausting
the node (`PIDPressure`). Pick a value well above legitimate peaks. The setting is
`--pod-max-pids` / `podPidsLimit`, a node-level limit rather than a per-pod resource. You can also reserve PIDs for the OS and daemons
with `kubeReserved` / `systemReserved` entries such as `pid: "1000"`.

## Apply
kubeadm clusters: the kubelet configuration is kept in the `kubelet-config` ConfigMap in kube-system
and delivered to each node as a kubelet configuration file; edit the file on the node (or the ConfigMap
for new nodes) and restart the kubelet.

## Verify
```bash
kubectl get node <n> -o jsonpath='{.status.capacity.pods} {.status.allocatable.pods}{"\n"}'
kubectl get --raw /api/v1/nodes/<n>/proxy/configz       # kubeletconfig.maxPods, podPidsLimit
kubectl get pods -A --field-selector spec.nodeName=<n>
```
Pods beyond the limit stay Pending with `Too many pods`.

## Checked
2026-10-23, against the kubelet defaults source (maxPods 110, PodPidsLimit default -1), the Kubernetes website pages on large clusters (no more than 110 pods per node), process ID limits (`--pod-max-pids`, PodPidsLimit, PID reservation), kubeadm kubelet integration (`kubelet-config` ConfigMap) and the kubelet-config-file task (`configz`), plus the kube-controller-manager node-cidr-mask-size help text (default 24 for IPv4). EKS, GKE and AKS pod limits, the PLEG remark, the default config path and the "lowering is safe" remark were removed as unconfirmed.
Method: documentation only; no commands were run.
