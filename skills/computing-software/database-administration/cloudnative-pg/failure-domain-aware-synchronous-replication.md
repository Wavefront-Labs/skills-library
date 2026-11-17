---
id: computing-software.database-administration.cloudnative-pg.failure-domain-aware-synchronous-replication
name: failure-domain-aware-synchronous-replication
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [synchronous-replication, failure-domain, podfailuredomainkeys, nodefailuredomainkeys, availability-zone, topology]
level: advanced
status: docs-checked
description: "Place synchronous standbys outside the primary's zone with podFailureDomainKeys or nodeFailureDomainKeys; read the topology condition."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Restrict synchronous standby choice to instances outside the primary's failure domain using one of two mutually exclusive options in `.spec.postgresql.synchronous`:

- `podFailureDomainKeys`: pod label keys, read from each instance pod without consulting the node (recommended).
- `nodeFailureDomainKeys`: node label keys, such as `topology.kubernetes.io/zone`, read from the hosting node.

Instances share a domain when all listed labels have the same values. From Kubernetes 1.35 the zone and region labels are copied onto pods automatically; on 1.34 or older, or without the `PodTopologyLabelsAdmission` feature, use `nodeFailureDomainKeys`.

```yaml
  postgresql:
    synchronous:
      podFailureDomainKeys:
      - topology.kubernetes.io/zone
      method: first
      number: 2
```

Behaviour is all-or-nothing: the constraint applies only when enough cross-domain standbys exist (the full `number` for `required`, just one for `preferred`). Otherwise, including when topology cannot be extracted (deleted node, missing pod label), the keys are ignored and selection proceeds as if unset, so writes never wait for acknowledgments that cannot arrive. With `preferred`, one cross-domain standby among two healthy replicas means one required acknowledgment instead of two.

Observe it through the `SyncReplicationTopologySatisfied` status condition (reason shown in the `SYNCTOPOLOGY` column of `kubectl get clusters -o wide`), `kubectl cnpg status`, and `.status.topology`. Names in `standbyNamesPre`/`Post` are not checked.

## Checked

2026-11-08. Failure domain options, all-or-nothing rule, Kubernetes 1.35 pod topology labels and status condition confirmed on the Replication page.

Method: documentation only; no commands were run.
