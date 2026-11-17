---
id: computing-software.database-administration.scylladb.kb-increase-replication-factor
name: kb-increase-replication-factor
category: computing-software
field: database-administration
product: scylladb
tags: [replication-factor, alter-keyspace, consistency-level, repair, tablets]
level: advanced
status: docs-checked
description: "Safely increase ScyllaDB replication factor: tablet keyspaces need client restarts; vnode keyspaces need CL_new = CL_old + RF_new - RF_old, ALTER KEYSPACE, repair, lower the CL."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/rf-increase.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Safely increasing the replication factor

RF is per keyspace, changed with `ALTER KEYSPACE`. Existing data is not streamed to the new replicas (a common misconception).

**Tablet keyspaces (default)**: consistency is not affected. But drivers do not pick up new tablet replicas after an RF increase, so requests are not routed to them and load is unbalanced. Restart the client applications after the ALTER succeeds.

**Vnode keyspaces (tablets disabled)**: effective consistency for pre-existing data drops by `RF_new - RF_old` until repaired. Procedure:
1. Raise the read CL: `CL_new = CL_old + RF_new - RF_old`.
2. `ALTER KEYSPACE` to the new RF.
3. Repair all tables of the keyspace (if only one DC changed, repair only that DC nodes).
4. Lower the read CL back.

Example: 5 nodes, RF 3, reads at TWO, going to RF 5. Needed increase is 5 - 3 = 2, so the read CL must rise by 2; QUORUM is not high enough here, so read at ALL, ALTER to RF 5, repair, then return to QUORUM. Skipping this can return stale or null data.

```
ALTER KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','dc1':5};
```

## Checked

2026-11-04. Confirmed against kb/rf-increase.rst: tablets and vnode behaviour, driver restart, no streaming of existing data, CL_new formula, repair, the five-node example. Reworded the example arithmetic to match the page.

Method: documentation only; no commands were run.
