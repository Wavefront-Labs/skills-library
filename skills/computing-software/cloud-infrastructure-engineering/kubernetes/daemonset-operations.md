---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-operations
name: daemonset-operations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, node-agent, rollingupdate, ondelete, maxunavailable, maxsurge, tolerations, control-plane-taint, hostnetwork, hostpath, node-selector, csi-node-plugin, cni-plugin, log-agent, nfd, node-drain, cordon]
level: practitioner
status: docs-checked
description: "DaemonSet scheduling and updates: one pod per matching node via the default scheduler, RollingUpdate vs OnDelete, control-plane tolerations, and surviving node drains."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/", "https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/", "https://kubernetes.io/docs/tasks/manage-daemon/rollback-daemon-set/", "https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet operations — exactly one pod per node, kept that way

**Goal:** run node-local agents (CNI, CSI node plugin, log/metrics collectors, security
scanners) reliably across every node that should have one, and update them without a window
where a node has zero coverage. General taints/affinity mechanics are in
`computing-software.cloud-infrastructure-engineering.kubernetes.pod-scheduling-and-resource-requests`;
this is what's specific to DaemonSet.

## 1. How placement actually works
The DaemonSet controller creates one pod per eligible node and sets the pod's
`spec.affinity.nodeAffinity` to match that host; the default scheduler (ScheduleDaemonSetPods,
beta from 1.12, stable 1.17) then binds the pod by setting `.spec.nodeName`. Consequences:
- If the new pod cannot fit on the node, the default scheduler may preempt existing pods based
  on priority. The docs suggest setting `.spec.template.spec.priorityClassName` to a PriorityClass
  with higher priority when it is important that the pod runs on each node (for example
  `system-node-critical` or `system-cluster-critical`).
- You can set a different scheduler with `.spec.template.spec.schedulerName`.
- The controller automatically adds a toleration for `node.kubernetes.io/unschedulable:NoSchedule`,
  so DaemonSet pods are placed on cordoned (unschedulable) nodes too, and running pods stay.
- Pod template `restartPolicy` must be `Always` (or unset), and `.spec.selector` cannot be
  changed after creation.

## 2. Reaching control-plane / tainted nodes
The controller adds tolerations for `not-ready` and `unreachable` (NoExecute, so pods are not
evicted from such nodes), `disk-pressure`, `memory-pressure`, `pid-pressure`, `unschedulable`
(NoSchedule) and, for `hostNetwork: true` pods, `network-unavailable`. Custom taints, such as the
control-plane taint, need explicit tolerations:
```yaml
tolerations:
- operator: Exists      # tolerate every taint: typical for a "must run everywhere" agent
```
or scope it narrowly:
```yaml
tolerations:
- {key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule}
```
Network-plugin DaemonSets often use `hostNetwork: true` and `hostPath` mounts, which gives them
node-level reach; keep them in their own namespace and scope any relaxed Pod Security level to that
namespace only (see `computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`).

## 3. Update strategy
```yaml
updateStrategy:
  type: RollingUpdate
  rollingUpdate: {maxUnavailable: 1, maxSurge: 0}   # defaults; maxSurge is stable since 1.25
```
- `RollingUpdate` (default): after a template change old pods are killed and new ones created in
  a controlled fashion, bounded by `maxUnavailable` (absolute or percentage; default 1; cannot be
  0 when `maxSurge` is 0). History is kept as `ControllerRevision` objects.
- `OnDelete`: new pods are created only when you delete the old pod on that node. Use it when a
  controlled, audited one-node-at-a-time rollout matters more than speed.
- Higher `maxUnavailable` speeds the rollout but leaves that many nodes without the agent at once;
  keep it conservative for anything on the data path. See `daemonset-maxsurge-updates` for the
  start-new-first alternative.
- A broken template (crash loop, bad image) stalls the rollout; fix it by updating the template
  again, as the update task page describes. Rollback uses `kubectl rollout undo daemonset <name>
  --to-revision=<n>`.

## 4. Draining and node lifecycle
- `kubectl drain` does not actually drain DaemonSet pods: the controller would immediately replace
  them. Pass `--ignore-daemonsets` so drain skips them; without that flag drain cannot succeed
  while DaemonSet-managed pods are present.
- A DaemonSet pod being deleted still honours its own `terminationGracePeriodSeconds` and
  `preStop` hook, so a log shipper should flush buffers before exit (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.graceful-termination-and-node-drain`).
- When nodes are removed from the cluster, their DaemonSet pods are garbage collected. The
  controller uses the original template the next time a node (even with the same name) is created.

## Gotchas
- A DaemonSet has no replica count; to shrink coverage, change which nodes match (taint or
  relabel nodes).
- Because the controller adds the `not-ready` and `unreachable` NoExecute tolerations, DaemonSet
  pods are not evicted from unhealthy or partitioned nodes by those taints.
- `kubectl delete ds --cascade=orphan` leaves the pods; a new DaemonSet with the same selector
  adopts them.

## Verify
- [ ] `kubectl get ds <name> -o wide` shows DESIRED, CURRENT and READY equal to the count of
      nodes that should run it, including control-plane nodes if intended.
- [ ] `kubectl rollout status ds/<name>` completes after a template change, and no node shows
      zero pods for a data-path agent (CNI/CSI) during it.
- [ ] `kubectl drain <node> --ignore-daemonsets` succeeds and the DaemonSet pod stays or is
      recreated on that node.
- [ ] `kubectl get controllerrevision -l <selector-key>=<selector-value>` shows the expected history.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the DaemonSet concept page, the update and rollback tasks and the safely-drain-node task: controller-set node affinity and scheduler binding, preemption by priority, the PriorityClass note, `schedulerName`, the auto-added tolerations table (including unschedulable and network-unavailable), restartPolicy Always, immutable selector, node-removal garbage collection, orphan-and-adopt behaviour; update strategies OnDelete and RollingUpdate with defaults; ControllerRevision history and `kubectl rollout undo daemonset`; `--ignore-daemonsets` semantics for drain. Feature gate ScheduleDaemonSetPods beta 1.12, stable 1.17; DaemonSetUpdateSurge stable 1.25.
Wrong in the draft and corrected: cordoned nodes do not block DaemonSet pods (the controller adds an unschedulable toleration); `--ignore-daemonsets` makes drain skip DaemonSet pods rather than being needed to remove them; DaemonSet pods do receive not-ready and unreachable tolerations automatically; `maxSurge` is stable, not beta-era.
Removed: eviction and OOM-scoring claims for system-node-critical, a tolerationSeconds: 0 example, speculation about CNI pods stuck without networking, and a claim about validation errors on older clusters.

Method: documentation only; no commands were run.
