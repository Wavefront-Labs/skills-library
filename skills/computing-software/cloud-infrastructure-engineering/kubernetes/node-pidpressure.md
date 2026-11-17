---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-pidpressure
name: node-pidpressure
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-nodes, pidpressure, podpidslimit, node-conditions]
level: practitioner
status: docs-checked
description: "Diagnose and fix PIDPressure on nodes: find the process or pod leaking PIDs, kubelet pid eviction thresholds, podPidsLimit and system PID reservations."
sources: ["https://kubernetes.io/docs/concepts/policy/pid-limiting/", "https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/", "https://kubernetes.io/docs/reference/labels-annotations-taints/#node-kubernetes-io-pid-pressure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIDPressure

## Symptom
Node condition `PIDPressure=True`, taint `node.kubernetes.io/pid-pressure:NoSchedule`, pods
evicted with `The node was low on resource: pids`, or workloads failing to get a new PID once
the per-pod or node limit is hit.

## Find the leak
```bash
kubectl describe node <n> | grep -A8 Conditions
# on the node
cat /proc/sys/kernel/pid_max
ps -eo pid,nlwp,cmd --sort=-nlwp | head          # processes with most threads
# per-pod pids.current files sit in each pod's cgroup directory; the path depends on cgroup driver and QoS class
```
Map a pod UID found in a cgroup path back to a pod:
`kubectl get pods -A -o custom-columns=UID:.metadata.uid,NS:.metadata.namespace,POD:.metadata.name | grep <uid-fragment>`.

## Protect the node
```yaml
# KubeletConfiguration
podPidsLimit: 4096              # example value; the kubelet default is -1 (no per-pod limit)
systemReserved: {pid: "1000"}   # example values
kubeReserved: {pid: "1000"}
evictionHard:
  pid.available: "10%"          # example; the kubelet has no default hard threshold for pid.available
```
Raise `/proc/sys/kernel/pid_max` if the OS default is low (the docs note some installs use 32768).
The `pid.available` signal is calculated periodically and does not enforce a limit; even with a hard
threshold a fast PID leak can hit the node limit, so set `podPidsLimit` as well.

## Verify
The offending pod's PID count stays below `podPidsLimit`; node condition returns to False;
alert on `kube_node_status_condition{condition="PIDPressure",status="true"}`.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `pid=<number>` in `--system-reserved` and `--kube-reserved`, `--pod-max-pids` / `podPidsLimit`, `pid.available` signal and its
  limits (calculated periodically, does not enforce): pid-limiting page.
- PIDPressure condition and `pid-pressure` NoSchedule taint: node-status and labels/taints pages.
- Eviction message `The node was low on resource: pids.` and the `pids` resource name: kubelet eviction source v1.37.1.
- `podPidsLimit` default -1 and no default hard threshold for `pid.available`: kubelet defaults source and node-pressure
  eviction page (default hard thresholds list).
- Removed: cgroup path glob, zombie-reaper and `tini` advice, specific `pid_max` value, which no documentation covers.

Method: documentation only; no commands were run.
