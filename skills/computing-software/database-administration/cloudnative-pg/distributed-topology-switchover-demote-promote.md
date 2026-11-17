---
id: computing-software.database-administration.cloudnative-pg.distributed-topology-switchover-demote-promote
name: distributed-topology-switchover-demote-promote
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [replica-cluster, distributed-topology, demotiontoken, promotiontoken, switchover, disaster-recovery, externalclusters]
level: advanced
status: docs-checked
description: "Switch over between two clusters: set spec.replica primary and source, demote for a demotionToken, promote the other."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replica_cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a distributed topology every `Cluster` carries the same `externalClusters` list and a `.spec.replica` stanza. The primary side:

```yaml
replica:
  primary: cluster-eu-south
  source: cluster-eu-central
```

The replica side sets `primary: cluster-eu-south` and `source: cluster-eu-south`. When `primary` equals the `Cluster` name (or `.spec.replica.self`) the cluster is the global primary; otherwise it replicates from `source`. Use identical role definitions and secrets in all clusters.

**Demote.** On the current primary, change `primary` to the new one:

```yaml
replica:
  primary: cluster-eu-central
  source: cluster-eu-central
```

The operator archives the shutdown-checkpoint WAL as a `.partial` file and writes `.status.demotionToken` (base64 JSON from `pg_controldata`: system identifier, timestamp, timeline, REDO location and WAL file). Read it:

```sh
kubectl get cluster cluster-eu-south \
  -o jsonpath='{.status.demotionToken}'
```

**Promote.** The demotion token is the promotion token of the other cluster. Set both fields in the same change:

```yaml
replica:
  primary: cluster-eu-central
  promotionToken: <PROMOTION_TOKEN>
  source: cluster-eu-south
```

Warning: omit the token and a failover is triggered, forcing a rebuild of the former primary. The cluster waits to replay WAL up to the LSN in the token, then switches timeline and archives the history file, which unblocks the old primary as a replica. Verify with `kubectl cnpg status`.

## Checked

2026-11-08. replica primary/source/promotionToken fields, demotion steps and the simultaneous-change warning confirmed on the Replica clusters page, section Distributed Topology.

Method: documentation only; no commands were run.
