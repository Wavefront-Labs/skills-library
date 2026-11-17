---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-component-down-triage
name: control-plane-component-down-triage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane, apiserver-down, apiserver-crashloop, connection-refused-6443, scheduler-not-running, controller-manager-down, leader-election, cka]
level: advanced
status: docs-checked
description: "Recover a broken control plane: kube-apiserver down (6443 refused, crashloop, etcd/cert errors) and scheduler or controller-manager not running or not leading."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/", "https://kubernetes.io/docs/concepts/architecture/leases/", "https://kubernetes.io/docs/reference/using-api/health-checks/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane component down

## kube-apiserver down
`The connection to the server <ip>:6443 was refused` — kubectl is useless, go to the node.
```bash
crictl ps -a --name kube-apiserver          # Exited? restart count climbing?
crictl logs $(crictl ps -a --name kube-apiserver -q | head -1) 2>&1 | tail -30
journalctl -u kubelet | grep -i apiserver | tail
ss -tlnp | grep 6443
```
| Log | Fix |
|---|---|
| unknown flag or invalid value | manifest edit typo in `/etc/kubernetes/manifests/kube-apiserver.yaml` |
| `open /etc/kubernetes/pki/...: no such file` | wrong path or missing hostPath mount |
| connection refused to etcd on 127.0.0.1:2379 | etcd down → fix etcd first (`crictl ps --name etcd`, its logs) |
| certificate expired (x509 error) | `kubeadm certs check-expiration`; `kubeadm certs renew all`, restart static pods (see `expired-control-plane-certificates`) |
| no container at all | kubelet can't parse the manifest (YAML) — check kubelet journal |
| starts then killed | liveness probe failing (`--secure-port`/bind address changed) |
Behind a load balancer, also check LB health checks and which endpoint your kubeconfig uses (kubeadm's `controlPlaneEndpoint`).

## kube-scheduler or kube-controller-manager not working
Symptoms: new pods stay `Pending` with **no** events (scheduler) ; Deployments don't create
ReplicaSets/pods, no endpoints updates, no node NotReady detection (controller-manager).
```bash
kubectl -n kube-system get pods -l tier=control-plane -o wide
kubectl -n kube-system logs kube-scheduler-<cp> --tail=50
kubectl -n kube-system get lease kube-scheduler kube-controller-manager -o custom-columns=NAME:.metadata.name,HOLDER:.spec.holderIdentity,RENEW:.spec.renewTime
```
- Holder identity points to a dead node and renewTime is stale → the other replicas should take
  over after the lease duration (the default `--leader-elect-lease-duration` is 15s for
  kube-controller-manager); if not, they can't reach the API or are crashlooping.
- Logs `failed to acquire lease` / `error retrieving resource lock` → API connectivity or
  RBAC/kubeconfig (`/etc/kubernetes/scheduler.conf`) broken or cert expired.
- Pods Pending with event `0/3 nodes are available` → scheduler is fine; it's a fit problem.
- `schedulerName` typo in the pod → no scheduler picks it up (no events).

## Verify
```bash
kubectl get --raw='/readyz?verbose'
kubectl get --raw='/livez?verbose'
kubectl run t --image=busybox --restart=Never -- true && kubectl get pod t -w
```
- [ ] All control-plane pods Running with stable restart counts; leases renewing; test pod schedules.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: debug-cluster and crictl task pages (crictl endpoint configuration, control-plane debugging), leases page (kube-controller-manager and kube-scheduler use Leases for leader election), kube-controller-manager reference (--leader-elect-lease-duration default 15s), kubeadm source (control-plane static pods carry the label tier=control-plane) and the health-checks page (livez and readyz with ?verbose). Replaced quoted error strings no document covers with plain descriptions.

Method: documentation only; no commands were run.
