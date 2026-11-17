---
id: computing-software.cloud-infrastructure-engineering.velero.data-mover-priority-class
name: data-mover-priority-class
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [priorityclassname, data-mover-priority, node-agent-priority-class, preemption, scheduling]
level: advanced
status: docs-checked
description: "Set priorityClassName for data mover pods in the node-agent ConfigMap versus the DaemonSet flag, and the scheduling trade-offs."
sources:
  - https://velero.io/docs/main/data-movement-pod-resource-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two places set priority classes:
- Data mover pods take `priorityClassName` from the node-agent ConfigMap (the one passed by `--node-agent-configmap`).
- The node-agent DaemonSet itself takes the class from `--node-agent-priority-class-name` at install time. The priority class must exist before you install Velero.

```json
{
    "priorityClassName": "backup-priority"
}
```

Higher priority (`system-cluster-critical`, `system-node-critical`, or a custom high class) suits dedicated backup nodes, time-critical backups and disaster recovery restores. Effects: pods schedule quickly and are less likely preempted, but they can pressure production workloads and in extreme cases cause production pod evictions.

Lower priority (`low-priority` or negative values) protects production during peaks and suits non-critical backups. Effects: production stays stable, but backups may start late, data mover pods can be preempted so backups fail, and in a constrained cluster backups might not run at all.

Pick by what you can tolerate: failed backups or squeezed workloads. Repository maintenance jobs have their own `priorityClassName`, read only from the `global` entry of the maintenance job ConfigMap. Remember to restart node-agent after editing the ConfigMap.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/data-movement-pod-resource-configuration/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
