---
id: computing-software.database-administration.scylladb.procedure-safe-cluster-shutdown-and-start
name: procedure-safe-cluster-shutdown-and-start
category: computing-software
field: database-administration
product: scylladb
tags: [shutdown, start, drain, maintenance, cluster-restart]
level: practitioner
status: docs-checked
description: "Shut down and start a whole ScyllaDB cluster cleanly: stop clients, drain every node in parallel, confirm DN, stop, then start in parallel and confirm UN."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/safe-shutdown.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/safe-start.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clean cluster shutdown and start

Use this when hardware must be moved or the whole cluster has to be stopped.

**Shutdown**
Before you begin confirm that no application is still using the cluster as backend storage. Then on every node, in parallel:
1. Run `nodetool drain`. It flushes memtables to SSTables and stops the node listening to clients and peers.
2. Validate the drain with `nodetool status`: a node listed as `DN` means the drain completed.
3. Stop the ScyllaDB service on the node after the drain has finished successfully.

**Start**
Only after the cluster was shut down with the procedure above:
1. Start the nodes in parallel.
2. Run `nodetool status`. If every node reports `UN` (Up Normal), the cluster is back.

Example of the commands per node:

```
nodetool drain
sudo systemctl stop scylla-server
sudo systemctl start scylla-server
nodetool status
```

## Checked

2026-11-04. Confirmed against safe-shutdown.rst and safe-start.rst, and the systemctl commands in rst_include: drain, DN check, stop, parallel start, UN check. Removed the unsupported rolling-restart advice.

Method: documentation only; no commands were run.
