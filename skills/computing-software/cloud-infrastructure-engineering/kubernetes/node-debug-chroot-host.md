---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-debug-chroot-host
name: node-debug-chroot-host
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-debug, chroot-host, node-debug, crictl]
level: practitioner
status: docs-checked
description: "Use kubectl debug node with chroot /host to run node tools (journalctl, crictl, systemctl), the profile it uses, cleanup of debugger pods, and limits."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#debugging-profiles", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node debug sessions with chroot /host

```bash
kubectl debug node/worker-3 -it --image=ubuntu --profile=sysadmin
# inside the debugger pod:
chroot /host
journalctl -u kubelet --since -15m
crictl ps -a
systemctl status containerd
```

## What you get
- Pod in the node's host IPC, network and PID namespaces, scheduled on that node.
- Node root filesystem mounted at `/host`.
- `--profile=sysadmin` makes it privileged (needed for `chroot /host`); `netadmin` adds NET_ADMIN and
  NET_RAW. Valid profiles are `legacy`, `general`, `baseline`, `restricted`, `netadmin` and `sysadmin`;
  `legacy` is deprecated, the kubectl v1.37 flag help names `general` as the default while the docs
  page still says `legacy`, so pass `--profile` explicitly.

`chroot /host` makes the node's binaries and config the root, so `crictl` uses the node's
`/etc/crictl.yaml` and `journalctl` reads the node journal.

## Cleanup
The debugger pod is left behind after exit:
```bash
kubectl get pods | grep node-debugger
kubectl delete pod node-debugger-worker-3-abcde
```
Delete them; they are privileged pods on your nodes.

## Limits and alternatives
- Pod Security Admission: the debugger pod lands in the current namespace; restricted or
  baseline namespaces reject privileged profiles. Run from a namespace allowed to be privileged
  (`-n kube-system` or a dedicated debug namespace).
- Nodes that cannot schedule pods (NotReady, kubelet down) need SSH or cloud serial console;
  `kubectl debug node` relies on the kubelet.

## Audit
Node debug is a privileged action; restrict `pods/create` in debug namespaces and watch audit
logs for `node-debugger-` pods.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- The debugger pod runs in host IPC, network and PID namespaces with the node root at `/host`, is not privileged by default
  so `chroot /host` fails without `--profile=sysadmin`, is named `node-debugger-<node>-<suffix>` and must be deleted, and
  `kubectl debug node` fails when the kubelet is down: kubectl-node-debug page.
- Profile names, `legacy` deprecation and the `general` flag default; `netadmin` adds NET_ADMIN and NET_RAW, `sysadmin` sets
  privileged: kubectl `debug.go` and `profiles.go` v1.37.1, debug-running-pod page.
- Removed: the pinned `ubuntu:24.04` image and the remark about Talos and Bottlerocket tooling, which the checked sources do
  not cover.

Method: documentation only; no commands were run.
