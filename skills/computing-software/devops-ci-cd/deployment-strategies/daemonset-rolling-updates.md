---
id: computing-software.devops-ci-cd.deployment-strategies.daemonset-rolling-updates
name: daemonset-rolling-updates
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, daemonset-rolling-update, rolling-update, maxunavailable]
level: practitioner
status: docs-checked
description: "Update DaemonSets safely: RollingUpdate maxUnavailable and maxSurge, OnDelete for node-critical agents, minReadySeconds, and monitoring rollout progress per node."
sources: ["https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet rolling updates

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 10%      # nodes without the pod at once (default 1)
      maxSurge: 0              # >0 runs old+new pod on a node briefly (default 0; cannot be 0 if maxUnavailable is 0)
  minReadySeconds: 30
```

## Choosing values
- `maxUnavailable: 1` on large clusters takes forever (hundreds of nodes x pod start time); use a percentage.
- `maxSurge` avoids gaps for agents like log shippers, but two copies must coexist on a node.
- `minReadySeconds` gives readiness probes time to catch crash loops before moving on.

## OnDelete
```yaml
updateStrategy: { type: OnDelete }
```
New pods only when you delete old ones. Use for node-critical daemons (CNI, CSI, GPU drivers) where
you roll node-by-node with drain/cordon, or with node pool upgrades.

## Monitoring
```bash
kubectl rollout status ds/fluent-bit -n logging
kubectl get ds fluent-bit -n logging   # DESIRED / CURRENT / UP-TO-DATE / AVAILABLE
```

## Gotchas
- Pods unschedulable on some nodes (taints, resources) stall the rollout at UP-TO-DATE < DESIRED;
  check tolerations and resource requests.

## Verify
- [ ] UP-TO-DATE equals DESIRED; no node without the agent for longer than minReadySeconds plus start time.

## Checked

2026-10-28. Confirmed against the Kubernetes DaemonSet update task and API reference: RollingUpdate is the default strategy and OnDelete the alternative; `maxUnavailable` takes a number or percentage with default 1; `maxSurge` default 0 and cannot be 0 when `maxUnavailable` is 0; `minReadySeconds`; `kubectl rollout status ds/...`. Removed: the 1.25 stable claim, hostPort and host-socket constraints, `--timeout`, the rollback and `--sort-by` commands, and the priorityClass and nodeSelector gotchas, which could not be checked.

Method: documentation only; no commands were run.
