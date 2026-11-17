---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-kernel-issues-dmesg-oom-hung-tasks
name: node-kernel-issues-dmesg-oom-hung-tasks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-nodes, node-kernel-issues, hung-task, dmesg, oom-killer]
level: practitioner
status: docs-checked
description: "Read kernel logs on a node with kubectl debug to find OOM kills, hung tasks, disk and NIC errors behind NotReady nodes or unexplained pod restarts."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#debugging-profiles", "https://github.com/kubernetes/node-problem-detector", "https://github.com/kubernetes/node-problem-detector/blob/master/config/kernel-monitor.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel-level node issues

## Get to the kernel log
```bash
kubectl debug node/<node> -it --image=busybox --profile=sysadmin -- chroot /host sh
dmesg -T | tail -200
journalctl -k --since "-2h" --no-pager
```

## What to grep for
| Pattern | Meaning |
|---|---|
| `Killed process <pid> (<name>) total-vm:...kB, anon-rss:...kB, file-rss:...kB` | kernel OOM killer; if the cgroup is a pod, the container shows `OOMKilled` |
| `task <name>:<pid> blocked for more than <n> seconds.` | hung task, usually stuck I/O (NFS, failing disk, overloaded volume) |
| `EXT4-fs error ...` / `Buffer I/O error ...` | disk or filesystem failure |
| `XFS ... Shutting down filesystem` | XFS shut down; the filesystem is unusable |
| `unregister_netdevice: waiting for <dev> to become free. Usage count = <n>` | network device teardown stuck |
| `BUG: unable to handle kernel NULL pointer dereference` | kernel oops |

These are the patterns in node-problem-detector's default `kernel-monitor.json` rules.

```bash
dmesg -T | grep -E -i 'killed process|blocked for more than|i/o error|ext4-fs error|shutting down filesystem|unregister_netdevice'
```

## Node-wide OOM vs pod OOM
Node-level OOM kills (not pod cgroup) mean system reservations are too small: raise
`systemReserved`/`kubeReserved` and keep `evictionHard memory.available` high enough that the
kubelet evicts before the kernel kills.

## Automate detection
node-problem-detector's kernel monitor turns these log lines into Events (`OOMKilling`, `TaskHung`,
`Ext4Error`, `IOError`, `KernelOops`) and node conditions (`KernelDeadlock` when a docker task is
hung, `XfsShutdown`), which you can alert on.

## Verify
After the fix, `kubectl describe node` shows no new kernel events and the pattern stops appearing in `journalctl -k`.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `kubectl debug node` mounts the node root at `/host`, runs in host namespaces and is not privileged unless
  `--profile=sysadmin` is used: kubectl-node-debug page and debug-running-pod page.
- Log patterns and the Event / condition each maps to (`OOMKilling`, `TaskHung`, `Ext4Error`, `IOError`, `KernelOops`,
  `XfsShutdown`, and `KernelDeadlock` only for the docker hung-task rule): node-problem-detector `config/kernel-monitor.json`.
- Removed: cgroup-OOM, conntrack, NIC watchdog and soft-lockup message strings and the pinned `busybox:1.36` image, which
  none of the checked sources covers.

Method: documentation only; no commands were run.
