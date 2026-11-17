---
id: computing-software.database-administration.yugabytedb.architecture-master-and-tserver-roles
name: architecture-master-and-tserver-roles
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-master, yb-tserver, architecture, tablets, raft, system-catalog, cluster-balancer]
level: intro
status: docs-checked
description: "What YB-Master and YB-TServer do, how many of each to run, their ports and web UIs, and which process to check first when diagnosing a YugabyteDB cluster."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/yb-master.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/yb-tserver.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/key-concepts.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/default-ports.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YB-Master and YB-TServer roles

A YugabyteDB universe runs two server types. Know which one owns a problem before touching flags.

- **YB-Master** holds the system catalog in a Raft group, handles DDL, tracks tablet locations and runs the cluster balancer. It stores no user rows.
- **YB-TServer** hosts tablet peers (the Raft replicas of table shards), serves YSQL and YCQL, runs the storage engine and performs compactions.

Sizing rule: the number of master peers is decided by the replication factor (RF). Surviving f failures needs RF 2f+1, so RF 3 survives one failure and RF 5 survives two.

Default ports:
- master RPC 7100, master web UI 7000
- tserver RPC 9100, tserver web UI 9000
- YSQL 5433, YCQL 9042
- YCQL webserver 12000, YSQL webserver 13000

Useful master UI pages: `/tablet-servers` (liveness and load) and `/cluster-config` (placement). Server data lives under the `yb-data` directory, with INFO logs in `yb-data/master/logs` and `yb-data/tserver/logs`.

Each tablet elects its own Raft leader, so leaders spread across tservers; the master only coordinates. If the master leader is lost, a new one is elected from the other masters.

## Checked

2026-11-04. Confirmed against the YB-Master and YB-TServer architecture pages (roles, Raft group of masters sized by RF, leader re-election, tablet peers and per-tablet Raft groups), key-concepts (fault tolerance needs 2ft + 1 domains), default-ports (5433, 9042, 7100, 9100, 7000, 9000, 12000, 13000) and the start-masters page (`yb-data/master/logs`, `yb-data/tserver/logs`, `cluster-config` page). Removed: the claim that tservers number at least the RF, and the `/tablet-replication` and Load Balancer page mentions for this skill (not in the cited pages).

Method: documentation only; no commands were run.
