---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-failover-test
name: control-plane-failover-test
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-failover-test, control-plane-ha, etcd, game-day, leader-election]
level: practitioner
status: docs-checked
description: "Prove control-plane HA works by stopping one control-plane node and checking the API, etcd quorum, leader leases and load-balancer health checks."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/", "https://etcd.io/docs/v3.5/faq/", "https://kubernetes.io/docs/concepts/architecture/leases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane failover test

## Before
```bash
etcdctl endpoint status --cluster -w table
for l in kube-controller-manager kube-scheduler; do
  kubectl -n kube-system get lease $l -o jsonpath='{.spec.holderIdentity}{"\n"}'; done
```
Note which node holds the etcd leader and each lease. Start a watcher from a client machine:
```bash
while true; do date +%T; kubectl get --raw='/readyz' --request-timeout=2s; echo; sleep 1; done
```

## Fail one node (pick the etcd leader for the hard case)
```bash
sudo systemctl stop kubelet
sudo mkdir /root/manifests-off && sudo mv /etc/kubernetes/manifests/*.yaml /root/manifests-off/
# or power the VM off to also test the load balancer
```

## What must happen
- `readyz` keeps answering within a few seconds (LB health check removes the dead backend).
- etcd elects a new leader; `endpoint status` shows quorum with one unreachable member.
- Leases move to another node within the lease duration (the default `--leader-elect-lease-duration` is 15s).
- `kubectl create deploy failover-check --image=registry.k8s.io/pause:<tag>` creates pods,
  proving controller-manager and scheduler work.

## Restore
```bash
sudo mv /root/manifests-off/*.yaml /etc/kubernetes/manifests/ && sudo systemctl start kubelet
etcdctl endpoint health --cluster
kubectl delete deploy failover-check
```

## Common findings
- LB health check uses TCP only (the kubeadm HA guide's cloud example does), so a node whose
  apiserver is up but not ready still gets traffic; consider an HTTPS `/readyz` probe.
- kubeconfigs on nodes point at one control-plane IP instead of the LB name.
- Two members down in a 3-member cluster: writes stop. Never test two at once.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: leases page and kube-controller-manager reference (--leader-elect-lease-duration default 15s, Leases used for leader election), kubeadm HA guide (TCP health check in the load balancer example), etcd v3.5 FAQ (three members tolerate one failure) and etcdctl README (endpoint status --cluster, -w table). Replaced the pinned pause tag with a placeholder.

Method: documentation only; no commands were run.
