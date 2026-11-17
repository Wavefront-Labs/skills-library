---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-component-skew-during-ha-upgrade
name: control-plane-component-skew-during-ha-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, version-skew, apiserver-instance-skew, controller-manager-skew, control-plane-ha, cluster-upgrade]
level: practitioner
status: docs-checked
description: "Skew rules between kube-apiserver instances and controller-manager, scheduler and cloud-controller-manager during an HA control-plane upgrade window."
sources: ["https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane component skew during HA upgrades

## The rules
- **kube-apiserver instances**: in an HA cluster, the newest and oldest apiserver must be
  within one minor version. You cannot jump 1.32 to 1.34 even briefly.
- **kube-controller-manager, kube-scheduler, cloud-controller-manager**: must not be newer
  than any apiserver they talk to; may be one minor older. Because they reach the apiserver
  through a load balancer, they can hit ANY instance, so they must not be newer than the
  oldest apiserver in rotation.

## Consequence for ordering
1. Upgrade all kube-apiserver instances first. kubeadm upgrades apiserver, controller-manager
   and scheduler together per node; that is safe because recent kubeadm versions write
   `controller-manager.conf` and `scheduler.conf` pointing at the LOCAL apiserver
   (the node's advertise address, per the kubeadm source), so each talks to an apiserver of
   the same version. Confirm with the `grep server:` check below.
2. If those kubeconfigs point at the LB endpoint instead (older clusters, hand-built ones), a
   new controller-manager on node 1 may reach an old apiserver on node 2. That is a skew
   violation for the duration: keep the window short or repoint them at the local apiserver.
3. Leader election means only one controller-manager is active; a new leader running against
   old apiservers is where new-field bugs appear.

## Check during the window
```bash
kubectl -n kube-system get pods -l tier=control-plane \
  -o custom-columns=POD:.metadata.name,IMAGE:.spec.containers[0].image
kubectl -n kube-system get lease kube-controller-manager kube-scheduler \
  -o custom-columns=NAME:.metadata.name,HOLDER:.spec.holderIdentity
grep server: /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf
```

## Effect on nodes
While apiserver instances differ in version, the allowed kubelet and kube-proxy versions
narrow: they must not be newer than the oldest apiserver instance. kubelet and kube-proxy
may be up to three minor versions older than kube-apiserver (two for versions below 1.25).

## Managed clusters
Managed services operate the control plane for you; check the provider's documentation for
what it enforces. Your side is the node components (kubelet and kube-proxy skew).

## Gotchas
- Cloud-controller-manager deployed as a Deployment by Helm is often forgotten; upgrade it in
  the same window, after apiservers.
- A controller-manager, scheduler or cloud-controller-manager newer than any apiserver it can reach is outside the supported skew, so do not roll an apiserver back below them.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: version-skew policy page (apiserver instances within one minor, controller-manager/scheduler/cloud-controller-manager not newer and at most one minor older, narrowing behind a load balancer, kubelet and kube-proxy up to three minors older) and the kubeadm kubeconfig phase source (controller-manager.conf and scheduler.conf use the local API endpoint).

Method: documentation only; no commands were run.
