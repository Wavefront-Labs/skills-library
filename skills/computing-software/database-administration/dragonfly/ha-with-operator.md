---
id: computing-software.database-administration.dragonfly.ha-with-operator
name: ha-with-operator
category: computing-software
field: database-administration
product: dragonfly
tags: [operator-ha, high-availability, failover, kubernetes, dragonfly]
level: practitioner
status: docs-checked
description: "Get automatic failover for Dragonfly on Kubernetes by setting replicas above 1 in the Operator custom resource."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/high-availability.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/operator/installation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly high availability rests on replication with read replicas as failover targets. On Kubernetes the Dragonfly Operator provides it out of the box.

Semantics of `replicas` (it counts instances, not only replicas):

- `replicas=1`: one primary only
- `replicas=2`: one primary and one replica
- `replicas=3`: one primary and two replicas
- There is always exactly one primary.

Steps:

1. Install the Operator (see operator install skill).
2. Apply a `Dragonfly` resource with `spec.replicas` above 1.
3. Connect through the service `<dragonfly-name>.<namespace>.svc.cluster.local`, which selects the primary and updates when the primary changes.
4. Find the primary: `kubectl get pods -l role=master`.

Failure test from the docs: `kubectl delete pod -l role=master`. The Operator creates a new master, repoints the service and reconfigures replication; data written earlier remains available. Clients keep the same service address.

## Checked

2026-11-04. Confirmed in the High Availability page (Operator section: replicas above 1, service selecting the master, `role=master` label, pod deletion test) and the Operator installation page (replicas semantics). Nothing removed.

Method: documentation only; no commands were run.
