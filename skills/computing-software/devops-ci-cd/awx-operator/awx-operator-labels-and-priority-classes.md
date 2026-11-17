---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-labels-and-priority-classes
name: awx-operator-labels-and-priority-classes
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, priority-class, control-plane-priority-class, postgres-priority-class, eviction]
level: intro
status: docs-checked
description: "Set PriorityClasses for the AWX control plane and Postgres pods so low-priority pods are evicted first."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/priority-classes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator labels and priority classes

The AWX and Postgres pods can be assigned a custom PriorityClass to rank their importance compared to other pods in the cluster, which determines which pods get evicted first if resources are running low. First create your PriorityClass if needed, then set its name for the control plane and postgres pods:

```yaml
spec:
  control_plane_priority_class: awx-demo-high-priority
  postgres_priority_class: awx-demo-medium-priority
```

## Checked

2026-11-04. Confirmed against the AWX Operator "Priority Classes" page: `control_plane_priority_class`, `postgres_priority_class`, the eviction purpose and the example names. Removed the whole `additional_labels` section, the stated defaults for the priority fields, and the cross-reference to the database page; none are on this page. The skill id keeps "labels" in its name for stability.
Method: documentation only; no commands were run.
