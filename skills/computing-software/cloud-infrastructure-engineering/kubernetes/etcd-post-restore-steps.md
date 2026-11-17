---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-post-restore-steps
name: etcd-post-restore-steps
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-restore, post-restore-checks, etcd-backup]
level: practitioner
status: docs-checked
description: "After an etcd restore: restart control-plane components and kubelets, handle stale watches and resourceVersions, reconcile drifted state and verify workloads."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/recovery/", "https://kubernetes.io/docs/reference/using-api/health-checks/", "https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_restart.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-restore steps after an etcd restore

The restore puts the cluster back to snapshot time, but every running component still holds
caches and watches from "the future". Kubernetes docs recommend restarting them.

## 1. Restart control-plane components
Restart kube-scheduler and kube-controller-manager (the components Kubernetes docs name), and any other
control-plane component that keeps watch caches, by moving their manifests out of and back into
`/etc/kubernetes/manifests`. etcd docs explain why: after a restore the revision can go backwards, and
informer caches may not refresh, causing unpredictable and inconsistent controller behaviour. If you did not
restore with `--bump-revision <n> --mark-compacted`, expect more of this and restart more components.

## 2. Restart kubelets
```bash
sudo systemctl restart kubelet     # on every node
```
Kubernetes docs recommend restarting the kubelets too. Critical components lose their leader lock during
the restore and restart themselves, so give the restore a few minutes to settle.

## 3. Restart in-cluster controllers
Operators and other in-cluster controllers use watches and informers, the consumers etcd docs say are
affected by revisions going backwards. Restart them if they misbehave:
```bash
kubectl -n argocd rollout restart deployment
kubectl -n argocd rollout restart statefulset
kubectl -n kube-system rollout restart deployment/coredns
```

## 4. Reconcile drift
- Anything created after the snapshot is gone: recent Deployments, Secrets (rotated
  credentials may now be reverted), PVCs. PVs dynamically provisioned after the snapshot become
  orphaned cloud disks.
- GitOps re-applies desired state; run a sync and review diffs.

## 5. Verify
```bash
kubectl get --raw='/readyz?verbose'
kubectl get nodes
kubectl get pods -A | grep -vE 'Running|Completed'
kubectl get events -A --sort-by=.lastTimestamp | tail -40
```
Compare a known list of critical workloads and recent Secrets with what the API now returns,
and record the data-loss window in the incident notes.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Confirmed: Kubernetes docs recommend restarting kube-scheduler, kube-controller-manager and the kubelets after a restore so they do not rely on stale data; etcd docs warn that after a restore revisions can go backwards and informer caches may not refresh, and recommend `--bump-revision` with `--mark-compacted` for Kubernetes; `kubectl rollout restart deployment -n <namespace>` form; `kubectl get --raw='/readyz?verbose'`. Removed as unconfirmed: the descriptions of what each kubelet reconciles, the `too old resource version` loop claim, the `deploy,sts` shorthand, and cloud-controller-manager as a named component.

Method: documentation only; no commands were run.
