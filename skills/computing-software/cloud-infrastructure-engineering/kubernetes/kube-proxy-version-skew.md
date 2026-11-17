---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-version-skew
name: kube-proxy-version-skew
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, version-skew, kube-proxy-skew, kube-proxy, cluster-upgrade]
level: practitioner
status: docs-checked
description: "Apply the kube-proxy skew rules (not newer than apiserver, up to three minors older, within three of the kubelet) when upgrading nodes and the DaemonSet."
sources: ["https://kubernetes.io/releases/version-skew-policy/#kube-proxy", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/core/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-proxy version skew

## Policy
- kube-proxy must not be newer than kube-apiserver.
- It may be up to three minor versions older than kube-apiserver (two for kube-proxy older than 1.25).
- It may be up to three minor versions older or newer than the kubelet on the same node (two for versions
  older than 1.25).
- With mixed kube-apiserver versions in an HA cluster, the allowed kube-proxy versions narrow.

## Where it bites
In kubeadm clusters kube-proxy is a DaemonSet whose image is bumped by `kubeadm upgrade apply`
on the first control plane, so every node, including not-yet-upgraded workers, gets the new
kube-proxy immediately. That is allowed (kube-proxy can be newer than the local kubelet by up
to three) as long as the apiserver was upgraded first, which `upgrade apply` guarantees.

Trouble cases:
- Hand-managed kube-proxy (systemd unit on nodes, some hardened distros): you must upgrade it
  per node, after the control plane.
- Node pools left more than three minors behind: kube-proxy (new) vs kubelet (old) exceeds the limit. The
  policy page warns against running kube-proxy persistently three minors behind.
- Pinning the kube-proxy image in GitOps: a sync would revert kubeadm's bump; keep the image in the
  same change as the control-plane upgrade.

## Check
```bash
kubectl -n kube-system get ds kube-proxy -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
kubectl get nodes -o custom-columns=NODE:.metadata.name,KUBELET:.status.nodeInfo.kubeletVersion,PROXY:.status.nodeInfo.kubeProxyVersion
```
`status.nodeInfo.kubeProxyVersion` is marked deprecated in the Node API; read the pod image instead:
```bash
kubectl -n kube-system get pods -l k8s-app=kube-proxy -o custom-columns=NODE:.spec.nodeName,IMAGE:.spec.containers[0].image
```

## Replacing kube-proxy
With a CNI that replaces kube-proxy there is no kube-proxy to skew, but that CNI has its own
compatibility matrix against Kubernetes versions; check its documentation before each upgrade.

## Checked

2026-10-26: kubernetes.io version-skew policy page and kubeadm-upgrade page (v1.37 docs, kubernetes/website main 2026-10-25) and the core v1 Node API source. Confirmed: all three kube-proxy skew rules including the pre-1.25 exception, HA narrowing, kubeadm upgrade applying the kube-proxy manifests, and the deprecated kubeProxyVersion field.

Method: documentation only; no commands were run.
