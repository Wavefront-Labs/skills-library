---
id: computing-software.database-administration.scylladb.admin-maintenance-socket-and-mode
name: admin-maintenance-socket-and-mode
category: computing-software
field: database-administration
product: scylladb
tags: [maintenance-socket, maintenance-mode, cqlsh, unix-socket, recovery]
level: advanced
status: docs-checked
description: "ScyllaDB maintenance socket (unauthenticated local CQL over a Unix socket, option values, group access) and maintenance mode (node isolated, local data only)."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/maintenance-socket.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/maintenance-mode.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Maintenance socket and maintenance mode

**Maintenance socket**: CQL over a Unix domain socket, with no authentication and full permissions. Permissions are `755`, so it is unreachable from outside the node and from other POSIX groups. It is created before the node joins the cluster.

Option `maintenance-socket`:
- `ignore`: no socket.
- `workdir`: socket at `<workdir>/cql.m`.
- Any other value: that path. It must be shorter than 108 characters and must not already exist as a file or directory.
`maintenance-socket-group` sets the owning group (default: the group of the user running scylla). The scylla user must be in that group or be root. To connect, join that group, run cqlsh as the scylla user, or change the group option.

```
cqlsh <workdir>/cql.m
```
Python driver: use `UnixSocketEndPoint(path)` with `WhiteListRoundRobinPolicy([socket])` so the driver does not try other nodes.

**Maintenance mode**: start with `--maintenance-mode true` or `maintenance_mode: true` in the config. The node refuses all incoming RPC connections and does not join the cluster: schema changes and other operations that need synchronisation are disabled, cluster-wide operations like repair are disabled for it, other nodes see it as dead, and it cannot read or write data on other nodes. The Alternator ports and TCP CQL port are not opened, so the only CQL access is the maintenance socket, serving local data only. The REST API works, except routes such as authorization_cache, failure_detector and hinted_hand_off_manager.

## Checked

2026-11-04. Confirmed against the ScyllaDB docs pages maintenance-socket.rst and maintenance-mode.rst: socket permissions, option values, path limit, group option, cqlsh and Python driver connection, maintenance-mode behaviour and disabled REST routes. Removed the unsupported claim that the socket is used to create the first superuser.

Method: documentation only; no commands were run.
