---
id: computing-software.database-administration.patroni.patroni-sync-state-invariants
name: patroni-sync-state-invariants
category: computing-software
field: database-administration
product: patroni
tags: [patroni, synchronous-mode, sync-key, dcs, invariants]
level: sme
status: docs-checked
description: "The /sync DCS key and the ordering invariants Patroni maintains in synchronous mode."
sources:
  - https://patroni.readthedocs.io/en/latest/replication_modes.html
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reason about what the /sync key guarantees during failures.

In synchronous mode Patroni maintains a `/sync` key in the DCS with the latest primary and the current synchronous standby databases. It is updated under strict ordering constraints that preserve these invariants:

1. A node must be marked as the latest leader whenever it can accept write transactions. Patroni crashing or PostgreSQL not shutting down can violate this.
2. A node must be set as the synchronous standby in PostgreSQL as long as it is published as the synchronous standby in the `/sync` key.
3. A node that is neither the leader nor the current synchronous standby cannot promote itself automatically.
4. Patroni assigns one or more synchronous standbys, based on `synchronous_node_count`, to `synchronous_standby_names`.

Example (`synchronous_node_count: 2`):

```
/sync  {"leader": "node0", "sync_standby": "node1,node2"}
synchronous_standby_names = 'FIRST 2 (node1,node2)'
```

Only node1 and node2 are known to be synchronous and allowed to be promoted automatically if node0 fails.

Candidate rules from the REST API page: for a switchover (with or without candidate) in synchronous mode the candidate must be in the `/sync` key members; for a manual failover this check is omitted, and a candidate in a cluster without a leader may promote even if it is not in `/sync`, its lag exceeds the limit, or its timeline is behind.

## Checked

2026-11-08. Confirmed against the Patroni replication modes page (synchronous mode implementation, the /sync example) and the REST API page (healthy standby rules). Removed the claim about a 4.1.1 release fix, which the cited pages do not cover.

Method: documentation only; no commands were run.
