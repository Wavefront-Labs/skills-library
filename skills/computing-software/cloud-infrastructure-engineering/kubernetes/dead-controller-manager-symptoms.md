---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dead-controller-manager-symptoms
name: dead-controller-manager-symptoms
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting-control-plane, no-pods-created, kube-controller-manager, leader-election]
level: practitioner
status: docs-checked
description: "Recognise a dead or stuck kube-controller-manager (Deployments with no ReplicaSets or pods, no node eviction, stuck deletes) and get it running again."
sources: ["https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/", "https://kubernetes.io/docs/concepts/architecture/nodes/", "https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/", "https://kubernetes.io/docs/reference/using-api/health-checks/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symptoms of a dead controller-manager

## Tell it apart from a dead scheduler
| Symptom | Dead component |
|---|---|
| Deployment created, no ReplicaSet; or ReplicaSet with 0 pods and no events | controller-manager |
| Pods exist but stay `Pending` with no node and no scheduling events | scheduler |

## Other controller-manager symptoms
- Nodes `NotReady` but no `node.kubernetes.io/unreachable` taint and pods never evicted (the node
  controller is part of kube-controller-manager).
- PVCs `Pending` with dynamic provisioning that worked before (`persistentvolume-binder-controller`
  runs here).
- Jobs and CronJobs not creating pods; EndpointSlices not updated.
- Garbage collection stops: deleted Deployments leave ReplicaSets behind.

## Check
```bash
kubectl -n kube-system get pods -o wide            # static pod kube-controller-manager-<node>
kubectl -n kube-system get lease kube-controller-manager -o jsonpath='{.spec.holderIdentity} {.spec.renewTime}{"\n"}'
kubectl get --raw='/readyz?verbose'
# on the control-plane node
sudo crictl ps -a
sudo crictl logs <container-id>
```
The leader-election Lease is `kube-controller-manager` in `kube-system` by default
(`--leader-elect-resource-name`, `--leader-elect-resource-namespace`). A `renewTime` much older
than the lease duration (`--leader-elect-lease-duration`, default 15s) means no healthy leader.

## Common causes
Expired `controller-manager.conf` client certificate, bad flag after a manifest edit (static pod
crash loop), wrong `--cluster-signing-cert-file` or `--service-account-private-key-file` path,
apiserver unreachable on the kubeconfig address.

## Recover
Fix the manifest or certificate (`kubeadm certs renew controller-manager.conf`), restart the
static pod (move its manifest out of `/etc/kubernetes/manifests/` and back), then confirm the
lease renews and pending Deployments get ReplicaSets.

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): kube-controller-manager flag reference (`--leader-elect-resource-name` default
`kube-controller-manager`, namespace default `kube-system`, lease duration default 15s, signing
and service-account key flags, `persistentvolume-binder-controller`), Nodes (node controller in
kube-controller-manager adds unreachable taints and evicts), Lease fields `holderIdentity` and
`renewTime`, health checks (`/readyz?verbose`), crictl debugging page and kubeadm certificate
management (renewing `controller-manager.conf` and restarting static pods). Removed the
unconfirmed `component=` label selector, Terminating-namespace and ServiceAccount-token bullets.

Method: documentation only; no commands were run.
