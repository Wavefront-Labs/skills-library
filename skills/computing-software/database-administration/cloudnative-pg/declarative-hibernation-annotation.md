---
id: computing-software.database-administration.cloudnative-pg.declarative-hibernation-annotation
name: declarative-hibernation-annotation
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [hibernation, cnpg-hibernation, annotation, rehydration, pvc, batch-workloads, cost]
level: intro
status: docs-checked
description: "Hibernate a cluster with cnpg.io/hibernation to remove pods but keep PVCs, read the condition, rehydrate later."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/declarative_hibernation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hibernation suits batch-driven workloads whose database must be up only while the batch runs. It saves CPU by removing the database pods and keeping the PVCs, replicas included.

```sh
kubectl annotate cluster <cluster-name> --overwrite cnpg.io/hibernation=on
```

The operator deletes the primary pod first and then the replica pods, avoiding a switchover so that replicas stay in sync. The cluster has no running pods afterwards, but the volumes remain so it can be rehydrated.

Monitor the `cnpg.io/hibernation` condition:

```sh
kubectl get cluster <cluster-name> -o "jsonpath={.status.conditions[?(.type==\"cnpg.io/hibernation\")]}"
```

When done the condition carries `"reason":"Hibernated"`, `"status":"True"` and `"message":"Cluster has been hibernated"`. `kubectl cnpg status <cluster-name>` shows the same in a Hibernation section with `Ready instances: 0`.

Rehydrate by setting the annotation to `off`, or removing it:

```
kubectl annotate cluster <cluster-name> --overwrite cnpg.io/hibernation=off
kubectl annotate cluster <cluster-name> cnpg.io/hibernation-
```

The pods are recreated and the cluster resumes operation. Because only compute is removed, storage cost continues while the cluster is hibernated, since the PVCs are retained.

## Checked

2026-11-08. Annotation values, pod deletion order, status condition and rehydration commands confirmed on the Declarative hibernation page.

Method: documentation only; no commands were run.
