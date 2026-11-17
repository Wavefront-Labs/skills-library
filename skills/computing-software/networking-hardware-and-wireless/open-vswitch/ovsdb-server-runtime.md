---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovsdb-server-runtime
name: ovsdb-server-runtime
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovsdb-server, remote, active-backup, sync-from, manager, ptcp, pssl, ovsdb-appctl]
level: advanced
status: docs-checked
description: "Run and control ovsdb-server: --remote forms, SSL options, active-backup with --sync-from, ovs-appctl ovsdb-server commands, and the ovs-vsctl set-manager Manager table."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovsdb-server.1.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovsdb-server runtime
ovsdb-server provides JSON-RPC access over active or passive TCP/IP or Unix domain sockets to one or more databases (ovsdb-server(1)). Database files must already exist (ovsdb-tool create, create-cluster or join-cluster); with none named, the default is `/usr/local/etc/openvswitch/conf.db`. It supports standalone, active-backup, relay and clustered service models, and since 2.9 also hosts a built-in `_Server` database.

Listeners: `--remote=remote` adds an OVSDB active or passive connection method such as `pssl:6640`; repeat it for several. The extra form `db:db,table,column` reads connection methods from a column, adding and dropping them as it changes. A UUID column referencing a table is read for `target` (mandatory), `max_backoff`, `inactivity_probe` and `read_only`. `--config-file=file` (JSON with `remotes` and `databases`) is an alternative, mutually exclusive with `--remote`, database arguments and the active-backup options; run `ovs-appctl ovsdb-server/reload` after editing it.

SSL/TLS (identity for outgoing connections): `-p`/`--private-key`, `-c`/`--certificate` (signed by the CA the peer uses), `-C`/`--ca-cert`; each accepts `db:db,table,column` to read the file name from the database. Daemon options include `--detach` (detaches once listening on all remotes; clustered databases may not be ready yet, so use `ovsdb-client wait`), `--pidfile`, `--monitor`, `--no-chdir`, `--unixctl=socket`. `--run=command` runs a command in a shell and exits when it ends.

Active-backup: `--sync-from=server` starts the server as a backup replicating from `server` (an active connection method); a backup rejects all transactions that modify the database, including locks. Add `--active` to start as the active server but prepared to switch to backup. `--sync-exclude-tables=db:table[,db:table]...` excludes tables from replication. Relay databases are given as `relay:schema_name:remote` (see ovsdb-cluster-and-relay).

Runtime commands (`ovs-appctl -t ovsdb-server`, ovsdb-server(1)):
- `exit`, `ovsdb-server/compact [db]` (also automatic: over 2 times the previous compacted size and at least 10 MB, after 100 commits or 10 minutes; or after 24 hours with 100 commits), `ovsdb-server/reconnect` (drops all client connections).
- `ovsdb-server/add-remote remote`, `remove-remote`, `list-remotes` (only remotes named on `--remote` or add-remote, not those found through a database), `add-db database`, `remove-db database`, `list-dbs`, `tlog-set database:table on|off`, `tlog-list`.
- Active-backup: `set-active-ovsdb-server server` (overrides `--sync-from`), `get-active-ovsdb-server`, `connect-active-ovsdb-server` (switch to backup role, closing client connections), `disconnect-active-ovsdb-server` (switch to active), `set-active-ovsdb-server-probe-interval`, `set-sync-exclude-tables db:table[,db:table]...`, `get-sync-exclude-tables`, `sync-status`.
- Cluster: `cluster/cid db`, `cluster/sid db`, `cluster/status db`, `cluster/leave db` (the server may never rejoin afterwards).

Manager (ovs-vsctl(8), ovs-vswitchd.conf.db(5)): `ovs-vsctl set-manager target...` sets manager targets, each an OVSDB active or passive connection method such as `pssl:6640`; `get-manager` prints them and `del-manager` deletes them. The Manager table has `target` (unique) with `ptcp:[port][:host]`, `pssl:[port][:host]`, `tcp:` and `ssl:` forms where the port defaults to 6640, plus `max_backoff` (at least 1,000) and `inactivity_probe` (optional integer).

## Checked
2026-11-04. Confirmed against ovsdb-server(1), ovs-vsctl(8) and ovs-vswitchd.conf.db(5) (Manager table). Corrected the runtime command list (`reconnect` drops client connections; `add-db` and `remove-db` are real; removed nothing invented) and the `--active` meaning, and removed the Verify line and the unsourced ptcp-unauthenticated gotcha.
Method: documentation only; no commands were run.
