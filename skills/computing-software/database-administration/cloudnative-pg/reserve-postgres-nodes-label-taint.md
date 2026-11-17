---
id: computing-software.database-administration.cloudnative-pg.reserve-postgres-nodes-label-taint
name: reserve-postgres-nodes-label-taint
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [scheduling, node-labels, taints, tolerations, nodeselector, dedicated-nodes, affinity]
level: practitioner
status: docs-checked
description: "Dedicate worker nodes to PostgreSQL with the node-role.kubernetes.io/postgres label and NoSchedule taint, then match them with nodeSelector and tolerations in the Cluster spec."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For production the docs strongly recommend dedicating `postgres` nodes, ideally in multiples of three with one node per availability zone, so a three-instance cluster lands on three different nodes. A label marks capable nodes; a taint keeps other workloads off.

Label (reserved `*.kubernetes.io` labels can only be applied after the node exists):

```sh
kubectl label node <NODE-NAME> node-role.kubernetes.io/postgres=
```

Taint:

```sh
kubectl taint node <NODE-NAME> node-role.kubernetes.io/postgres=:NoSchedule
```

Then pin the cluster to those nodes in the `Cluster`:

```yaml
spec:
  # <snip>
  affinity:
    # <snip>
    nodeSelector:
      node-role.kubernetes.io/postgres: ""
```

```yaml
spec:
  # <snip>
  affinity:
    # <snip>
    tolerations:
    - key: node-role.kubernetes.io/postgres
      operator: Exists
      effect: NoSchedule
```

This isolates compute and, with locally attached disks, storage. Several clusters may share a node; to go further, use labels and taints so a node serves one instance of one specific `Cluster`.

## Checked

2026-11-08. Read in full: docs/src/architecture.md. Label, taint, nodeSelector and tolerations snippets and the multiples-of-three guideline confirmed on the Architecture page, section Reserving nodes for PostgreSQL workloads. Removed: the unsourced advice to keep the operator off these nodes with its own tolerations.

Method: documentation only; no commands were run.
