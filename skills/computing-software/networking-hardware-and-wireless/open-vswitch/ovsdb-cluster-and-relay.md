---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovsdb-cluster-and-relay
name: ovsdb-cluster-and-relay
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovsdb, cluster, raft, relay, cluster-status, active-backup, ovsdb-server]
level: sme
status: docs-checked
description: "Operate clustered OVSDB: cluster/status, kick, leave and election timer commands, plus relay databases that offload read clients, and the config-file service model."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovsdb-server.1.txt
  - http://www.openvswitch.org/support/dist-docs/ovsdb.7.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OVSDB cluster and relay
Cluster commands (ovsdb-server runtime commands, sent with ovs-appctl; they apply only to clustered-format databases made by `ovsdb-tool create-cluster` or `join-cluster`):
- `cluster/status DB` prints this server's status in the cluster and its connections to the other servers.
- `cluster/cid DB` and `cluster/sid DB` print the cluster ID and this server's ID.
- `cluster/kick DB SERVER` starts graceful removal of any server; SERVER is a server ID or the address given to create-cluster or join-cluster.
- `cluster/leave DB` starts graceful removal of this server. At least one server must remain and over half the servers must be up. A server that has left can never rejoin; create a new server and join it.
- `cluster/change-election-timer DB MS` sets the leader election timeout base in milliseconds (default 1000). Run it on the leader; check `cluster/status` to see when the change is committed.

Create and join files with ovsdb-tool (see ovsdb-tool-basics).

Relay: a relay database keeps an in-memory copy of another OVSDB server (the relay source) and scales out the number of clients. It handles read-only transactions and monitors itself and proxies writes to the source. It has no on-disk storage and does not add availability, which comes from the source's service model.
Start one against an already running database: `ovsdb-server relay:<DB_NAME>:<relay source>`, where the source may be a comma-separated list of connection methods, for example to reach any server of a clustered database. Several relay servers can share one source.

From Open vSwitch 3.3, `--config-file` can define databases with a `service-model` of standalone, clustered, active-backup or relay, instead of command-line arguments. `--config-file` and `--remote` are mutually exclusive.

Active-backup (non-Raft) is configured with `--sync-from` (see ovsdb-server-runtime).

## Checked
2026-11-04. Confirmed against ovsdb-server(1) and ovsdb(7): the cluster/* commands and their conditions, the election timer default and leader rule, the relay description and start syntax, the 3.3 config-file support and service models, and the --sync-from role. Removed because the pages did not confirm them: the since-2.16 claim, the concrete ptcp relay example, the role and term wording for cluster/status, the "changed gradually" wording, the verify line and the majority-loss gotcha.
Method: documentation only; no commands were run.
