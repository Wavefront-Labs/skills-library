---
id: computing-software.cloud-infrastructure-engineering.kubernetes.post-upgrade-verification
name: post-upgrade-verification
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-upgrade, post-upgrade-verification, version-skew, smoke-test]
level: practitioner
status: docs-checked
description: "Verify a Kubernetes upgrade actually finished: component and node versions, addon versions, API health, deprecated API errors and a workload smoke test."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/#verify-the-status-of-the-cluster", "https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/docs/reference/using-api/deprecation-guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-upgrade verification

## Versions
```bash
kubectl version                                         # server version
kubectl get nodes -o custom-columns=NAME:.metadata.name,KUBELET:.status.nodeInfo.kubeletVersion,RUNTIME:.status.nodeInfo.containerRuntimeVersion
kubectl -n kube-system get pods -o custom-columns=NAME:.metadata.name,IMAGE:.spec.containers[*].image | grep -E 'apiserver|controller|scheduler|etcd|proxy|coredns'
```
Every control-plane pod should show the target tag; kubelets may lag by policy but should
converge; kube-proxy DaemonSet image should be updated.

## Health
```bash
kubectl get --raw='/readyz?verbose' | tail -5
kubectl get --raw='/livez?verbose' | tail -3
kubectl get nodes                               # all Ready, none SchedulingDisabled left behind
kubectl get pods -A | grep -vE 'Running|Completed'
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp | tail -30
kubectl get apiservices | grep -v True          # aggregated APIs (metrics-server) still Available
```

## Deprecated and removed APIs
```bash
kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis
```
API versions the release no longer serves (see the deprecated API migration guide) are rejected; check CI pipelines and Helm releases too.

## Smoke test
```bash
kubectl create ns smoke
kubectl -n smoke create deploy web --image=nginx --replicas=2
kubectl -n smoke expose deploy web --port 80
kubectl -n smoke run t --rm -it --image=busybox --restart=Never -- wget -qO- web
kubectl -n smoke run d --rm -it --image=busybox --restart=Never -- nslookup kubernetes.default
kubectl delete ns smoke
```
Also test one PVC provisioning, one Ingress route and HPA scaling if those are in use.

## Close out
- `kubeadm certs check-expiration` (renewed during upgrade).
- Re-hold the packages (`apt-mark hold`) at the new version; the upgrade procedure unholds them temporarily.
- Record the old and new versions and delete `/etc/kubernetes/tmp` backups after a soak period.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: kubeadm-upgrade page (verify nodes with kubectl get nodes, /etc/kubernetes/tmp backups remain and must be cleared manually, certificate renewal during upgrade, apt-mark unhold/hold), health-checks page, deprecation guide (no longer served versions) and the metrics reference (apiserver_requested_deprecated_apis exists). Removed the unconfirmed 404 claim.

Method: documentation only; no commands were run.
