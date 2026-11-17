---
id: computing-software.cloud-infrastructure-engineering.kubernetes.component-version-audit
name: component-version-audit
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, version-skew, component-version-audit, cluster-upgrade, kubectl-skew]
level: practitioner
status: docs-checked
description: "Audit every component version in a cluster (apiserver, control plane, kubelets, kube-proxy, runtimes, addons, kubectl clients) against the skew policy."
sources: ["https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/releases/patch-releases/", "https://github.com/containerd/containerd/blob/main/RELEASES.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component version audit

Run before any upgrade and quarterly; the output tells you what is out of policy or out of
support (each minor gets about 14 months of patches).

## Script
```bash
echo "== server"; kubectl version -o json | jq -r '.serverVersion.gitVersion'
echo "== control plane"
kubectl -n kube-system get pods -l tier=control-plane -o custom-columns=POD:.metadata.name,IMAGE:.spec.containers[0].image --no-headers
echo "== nodes"
kubectl get nodes -o custom-columns=NODE:.metadata.name,KUBELET:.status.nodeInfo.kubeletVersion,RUNTIME:.status.nodeInfo.containerRuntimeVersion,OS:.status.nodeInfo.osImage,KERNEL:.status.nodeInfo.kernelVersion --no-headers
echo "== kubelet versions summary"
kubectl get nodes -o jsonpath='{range .items[*]}{.status.nodeInfo.kubeletVersion}{"\n"}{end}' | sort | uniq -c
echo "== kube-proxy / coredns"
kubectl -n kube-system get ds kube-proxy deploy coredns -o custom-columns=NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image --no-headers 2>/dev/null
echo "== aggregated APIs"; kubectl get apiservices -o custom-columns=NAME:.metadata.name,SVC:.spec.service.name,OK:.status.conditions[0].status | grep -v Local
```

## Evaluate against policy
| Component | Allowed vs apiserver |
|---|---|
| other apiservers (HA) | within 1 minor |
| controller-manager, scheduler, CCM | same or 1 older |
| kubelet | same or up to 3 older (2 for kubelet below 1.25), never newer |
| kube-proxy | same or up to 3 older (2 below 1.25), never newer; within 3 minors of its kubelet |
| kubectl | 1 newer or 1 older |

## Beyond core
- CNI, CSI drivers, ingress controller, cert-manager, metrics-server: each publishes a
  supported Kubernetes range; list Helm releases with `helm list -A` and check chart app versions.
- Container runtime: check the containerd RELEASES.md table for support status and the Kubernetes compatibility table (at the time of checking, 1.6 and 1.7 were marked End of Life, 2.0 was LTS to March 2027 and 2.2 was Active).
- Client side: CI images bundling old kubectl (`kubectl version --client`), client-go versions in
  operators (check `go.mod` for `k8s.io/client-go`).

## Output
Record a table of component, current, target, supported-until; anything outside policy blocks
the upgrade until fixed.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: version-skew policy page (apiserver, kubelet, kube-proxy, controller-manager, scheduler, cloud-controller-manager and kubectl skew rules), patch-releases page (roughly fourteen months of support per minor) and containerd RELEASES.md (support status and Kubernetes compatibility tables). Replaced the stale containerd statement.

Method: documentation only; no commands were run.
