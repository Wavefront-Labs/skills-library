---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-scheduling-node-selector-tolerations-affinity
name: awx-operator-scheduling-node-selector-tolerations-affinity
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, node-selector, tolerations, affinity, topology-spread, postgres-selector, db-migration]
level: practitioner
status: docs-checked
description: "Pin AWX web, task and Postgres pods to nodes with selectors, tolerations, affinity and topology spread, including per-component overrides."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/assigning-awx-pods-to-specific-nodes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator scheduling node selector tolerations affinity

`node_selector` and `postgres_selector` restrict AWX and Postgres pods to nodes matching all key/value pairs; `tolerations` and `postgres_tolerations` allow scheduling onto tainted nodes; `topology_spread_constraints` and `affinity` take Kubernetes specs. Prefix a setting with `web_` or `task_` (e.g. `task_tolerations`, `web_node_selector`) to constrain the web and task pods individually. `annotations` sets AWX pod annotations.

```yaml
spec:
  node_selector:
    disktype: ssd
    kubernetes.io/os: linux
  topology_spread_constraints:
    - maxSkew: 100
      topologyKey: "topology.kubernetes.io/zone"
      whenUnsatisfiable: "ScheduleAnyway"
      labelSelector:
        matchLabels:
          app.kubernetes.io/name: "<resourcename>"
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "AWX"
      effect: "NoSchedule"
  postgres_selector:
    disktype: ssd
```

`affinity` takes Kubernetes affinity rules (the page's example uses `nodeAffinity` and `podAntiAffinity`). All of these settings default to an empty string.

DB migration job: it applies migrations at cluster startup and is scheduled using the `task_*` settings (`task_node_selector`, `task_tolerations`, ...). If those are not defined it falls back to the global `node_selector` and `tolerations`.

## Checked

2026-11-04. Confirmed against the AWX Operator "Assigning AWX pods to specific nodes" page: all setting names and the web_/task_ prefix rule, defaults, the example, and the DB-migration job note. Changed the examples from `|` block strings to the plain YAML the page shows and removed the "string block" remark.
Method: documentation only; no commands were run.
