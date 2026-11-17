---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-problem-detector-and-node-conditions
name: node-problem-detector-and-node-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-problem-detector, npd, node-conditions, taints, kernel-monitor, custom-plugin-monitor, draino, cluster-autoscaler, node-health, remediation]
level: advanced
status: docs-checked
description: "How node-problem-detector reports kernel and system problems as Node conditions and Events, and which remedy systems can act on them."
sources: ["https://github.com/kubernetes/node-problem-detector", "https://github.com/kubernetes/node-problem-detector/blob/master/config/kernel-monitor.json", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node-problem-detector: turning kernel noise into Kubernetes signal

**Goal:** know what node-problem-detector (NPD) actually watches, how its findings become
Node `.status.conditions` and Events, and how to close the loop so a detected hardware/kernel
problem actually drains the node instead of sitting as a condition nobody acts on.

## 1. What NPD watches
NPD runs as a DaemonSet (one per node) with pluggable **problem daemons**, each polling a
different source and reporting into a shared exporter:
- **SystemLogMonitor** — tails logs (the node's kernel log through `/dev/kmsg`, the journal, or
  files) and matches regex rules against known-bad patterns, using a JSON rule file such as
  `kernel-monitor.json` (OOM kills, hung tasks, filesystem errors, hardware errors). Conditions
  it sets include `KernelDeadlock`, `ReadonlyFilesystem`, `FrequentKubeletRestart`,
  `FrequentDockerRestart` and `FrequentContainerdRestart`. This is **pattern matching against
  known strings**, so a new kernel version with reworded log messages can silently stop matching
  until the rule file is updated.
- **CustomPluginMonitor** — runs a user-defined check script or binary and maps the result to a
  problem; the extension point for checks nothing built-in covers.
- **HealthChecker** — checks kubelet and container runtime health, setting `KubeletUnhealthy` and
  `ContainerRuntimeUnhealthy`.
- **SystemStatsMonitor** — collects health-related system stats as metrics; it sets no node
  conditions.

## 2. How findings surface
The Kubernetes exporter (enabled by default, `--enable-k8s-exporter`) reports temporary problems
as Events and permanent problems as node conditions:
- **Node conditions** — persistent state, e.g. `KernelDeadlock`, `ReadonlyFilesystem`,
  `FrequentKubeletRestart`, surfacing in `kubectl describe node` alongside built-in
  conditions like `Ready`/`MemoryPressure`/`DiskPressure`. These are what
  `kube_node_status_condition` in kube-state-metrics exposes to Prometheus
  (`computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-object-state-and-cardinality`)
  — NPD is the producer, KSM is the Prometheus-side reader for the same condition objects.
- **Events** — transient, for issues that don't warrant a persistent condition
  (for example the `OOMKilling` and `TaskHung` rules in the default kernel monitor).
- A Prometheus exporter also publishes problem metrics (default port 20257, bound to 127.0.0.1).

Critically, **NPD only reports Events and conditions — it does not cordon, drain, or remediate
anything by itself**. NPD's README describes separate *remedy systems* that act on its output;
without one, a node can sit in `KernelDeadlock: True` indefinitely.

## 3. Wiring conditions to action
- The Kubernetes **node controller** auto-taints on the *built-in* conditions
  (`node.kubernetes.io/memory-pressure`, `/disk-pressure`, `/pid-pressure`, `/not-ready`, etc.).
- NPD's README lists these remedy systems that consume its conditions and events: the
  **Descheduler** (strategy `RemovePodsViolatingNodeTaints`, which needs the
  `TaintNodesByCondition` feature; the Cluster Autoscaler can then terminate drained nodes),
  **mediK8S** (Node Health Check Operator with external remediators) and Cluster API
  **MachineHealthCheck**.
- Cloud-managed node pools often have their own node auto-repair — check whether it already
  acts on node health before deploying a second remediation path that fights it.

## 4. Operational gotchas
- Rule files are versioned with NPD itself; a kubelet/OS upgrade that changes kernel log
  wording (common across major kernel versions or distro switches) silently breaks pattern
  matches — periodically verify KernelMonitor rules still match real log output on current
  node images, don't assume they transferred correctly from an older base image.
- Monitor NPD's own DaemonSet health; if NPD stops running, no new problems are reported.
- Over-aggressive custom plugin monitors (checking too frequently, or a check with false
  positives under load) can trigger drain churn — a "remediation" system that drains
  nodes on a flaky signal is worse than no automation; dry-run custom checks as
  Events-only before wiring them to drains.
- Hardware-specific checks (for example GPU errors) are not in the built-in rule files; add them
  as custom plugin monitors.

## Gotchas
- `kubectl describe node | grep -A2 <ConditionType>` is the fast check, but conditions not
  in the "known" list (`Ready`, `DiskPressure`, etc.) only show up if you look at the full
  conditions list — `kubectl get node <name> -o json | jq .status.conditions` is the
  complete, unfiltered view.
- Alerting rules should name the exact condition and `status="true"` rather than alerting on
  anything that is not `False`.

## Verify
- [ ] `kubectl get node <name> -o json | jq .status.conditions` shows the expected custom condition types, not just built-ins.
- [ ] A deliberately injected test condition (or a staged kernel-log pattern) results in the expected taint/drain within the expected time window.
- [ ] NPD's own DaemonSet pod health is monitored separately from the conditions it reports.
- [ ] KernelMonitor rule files have been checked against the current node OS/kernel version's actual log wording within the last upgrade cycle.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Problem daemon types, the conditions each sets, the Kubernetes exporter (temporary problems as Events, permanent as
  node conditions, `--enable-k8s-exporter` default true), Prometheus exporter default port 20257 and the list of remedy
  systems (Descheduler, mediK8S, MachineHealthCheck): node-problem-detector README (main branch).
- Default kernel rules, `OOMKilling` / `TaskHung` as temporary Events and `KernelDeadlock` set only by the docker hung-task
  rule: `config/kernel-monitor.json`.
- Built-in node-controller taints: taint-and-toleration page.
- Removed: the claimed NPD taint-exporter plugin, Draino, the heartbeat/TTL and `Unknown` condition behaviour, the
  `Remounting filesystem read-only` rule text and GPU Xid specifics, which the NPD documentation does not cover.

Method: documentation only; no commands were run.
