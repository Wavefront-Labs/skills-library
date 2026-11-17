---
id: computing-software.database-administration.scylladb.procedure-remove-datacenter
name: procedure-remove-datacenter
category: computing-software
field: database-administration
product: scylladb
tags: [decommission, datacenter, alter-keyspace, network-topology-strategy, rack-list]
level: advanced
status: docs-checked
description: "Decommission a whole data center: verify no unique data, repair, ALTER KEYSPACE the DC to 0 (stepwise for tablets, rack lists), then decommission its nodes."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/decommissioning-data-center.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remove a data center

Verify the DC holds no unique data and that no client writes go to its nodes. Check layout with `nodetool status`.

1. Vnode keyspaces: run `nodetool repair -pr` on every node of the DC being removed so everything is in sync with the other DCs.
2. Tablet keyspaces: run `nodetool cluster repair` on any node, so updates held only by the departing replicas propagate.
3. ALTER every keyspace so it stops replicating to the DC. Look at the definition first with `DESCRIBE`:

```
ALTER KEYSPACE nba WITH REPLICATION = {'class':'NetworkTopologyStrategy','US-DC':3,'ASIA-DC':0,'EUROPE-DC':3};
```
For tablet keyspaces lower the RF one step at a time (for example 2, then 1, then 0), keeping `AND tablets = {'enabled': true}`.

With `rf_rack_valid_keyspaces` set, a tablet keyspace must use rack-list replication, for example `'ASIA-DC': ['RAC4','RAC5']`; reduce the list stepwise to `[]`. Consider enforce_rack_list so all tablet keyspaces use rack lists. In one ALTER of a rack-list keyspace, existing DCs must keep their RF.

4. Run `nodetool decommission` on every node of the DC and verify with `nodetool status`.

If audit is enabled, also ALTER the `audit` keyspace to remove the DC, or decommission fails with errors such as "zero replica after the removal". Until the DC is fully decommissioned, avoid global consistency levels (`ALL`, `EACH_QUORUM`) and use `LOCAL_*` levels. Removal of replicas by ALTER cannot be aborted; to go back, wait for it to finish and ALTER the replicas back in.

## Checked

2026-11-04. Confirmed against decommissioning-data-center.rst: prerequisites, repair per keyspace type, ALTER examples, stepwise tablet RF, rack-list rules, enforce_rack_list, decommission and status. Corrected the decommission step (every node, not one at a time). Replaced the unsupported closing sentence with the audit keyspace, LOCAL_* consistency and non-abortable ALTER notes from the page.

Method: documentation only; no commands were run.
