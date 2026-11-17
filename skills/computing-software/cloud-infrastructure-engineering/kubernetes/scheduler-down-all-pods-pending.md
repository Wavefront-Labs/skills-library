---
id: computing-software.cloud-infrastructure-engineering.kubernetes.scheduler-down-all-pods-pending
name: scheduler-down-all-pods-pending
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pending, scheduler-down-pending, kube-scheduler, control-plane-troubleshooting]
level: practitioner
status: docs-checked
description: "Recognise a dead or leaderless kube-scheduler (all new pods Pending with no events), confirm via leases and static pod logs, and restore it."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduler down: everything Pending

## Signature
- New pods stay `Pending` with **no events at all** (no FailedScheduling, no Scheduled).
- `spec.nodeName` empty; pods with `nodeName` set manually still run (scheduler bypassed).
- DaemonSet pods are also bound by the default scheduler, so they stay Pending too.

## Confirm
```bash
kubectl -n kube-system get pods -l component=kube-scheduler -o wide
kubectl -n kube-system get lease kube-scheduler -o yaml
```
The default leader-election object is named `kube-scheduler` in `kube-system`; a `renewTime` that is
long past means no active leader (a custom `--config` can change the name).

## On the control-plane node
kubeadm clusters run the scheduler as a static pod from `/etc/kubernetes/manifests/kube-scheduler.yaml`
(kubeadm names its scheduler kubeconfig `scheduler.conf`). Read that manifest and the container
and kubelet logs with your node's tooling.
Common causes:
- Manifest typo: wrong image, bad flag or kubeconfig path, YAML error.
- Expired or missing client credentials in the scheduler kubeconfig.
- `--config` pointing at a KubeSchedulerConfiguration with an invalid or unknown field.
- Leader-election flags changed by hand across HA control-plane nodes.

## Restore
Fix the manifest; the kubelet recreates the static pod from the changed file. Pending pods are
scheduled once a leader is elected.

## Verify
```bash
kubectl run sched-test --image=<image> --restart=Never && kubectl get pod sched-test -o wide
kubectl get events --field-selector reason=Scheduled
```

## Checked
2026-10-23, against the Kubernetes website DaemonSet page (default scheduler binds DaemonSet pods), kubeadm implementation details (manifest directory and scheduler.conf), and kube-scheduler source defaults (leader-election resource name kube-scheduler, namespace kube-system). Specific log strings, crictl commands and the 1.12 version note were removed as unconfirmed.
Method: documentation only; no commands were run.
