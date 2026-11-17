---
id: computing-software.database-administration.mysql.mysql-router-for-innodb-cluster
name: mysql-router-for-innodb-cluster
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-router, innodb-cluster, mysqlrouter-bootstrap, read-write-split, connection-routing, router-ports, innodb-clusterset]
level: practitioner
status: docs-checked
description: "Bootstrap and run MySQL Router in front of InnoDB Cluster/ReplicaSet: ports for RW/RO, read-write splitting, deployment next to apps, and health checks."
sources:
  - https://dev.mysql.com/doc/mysql-router/8.4/en/mysql-router-deploying-bootstrapping.html
  - https://dev.mysql.com/doc/mysql-router/8.4/en/router-read-write-splitting.html
  - https://dev.mysql.com/doc/mysql-router/8.4/en/mysql-router-general-using-deploying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL Router

**Goal:** applications connect to one local endpoint and always reach the current primary (writes) or secondaries (reads) of an InnoDB Cluster, ClusterSet or ReplicaSet.

## Bootstrap
```bash
mysqlrouter --bootstrap clusteradmin@db1:3306 --user=mysqlrouter --directory /etc/mysqlrouter/app --conf-use-sockets --account routerapp --name app-router
/etc/mysqlrouter/app/start.sh   # or a systemd unit using that directory
```
Bootstrap reads cluster metadata, creates a router account, writes `mysqlrouter.conf` and keyring.

## Default ports
| Port | Purpose |
|---|---|
| 6446 | Classic protocol, read-write (primary) |
| 6447 | Classic, read-only (secondaries, round-robin; falls back to primary if none) |
| 6448 / 6449 | X protocol RW / RO |
| 6450 | Read-write splitting: one port, Router sends reads to secondaries, writes and transactions to primary |

## Read-write splitting port
`access_mode=auto` routes autocommit SELECTs to secondaries and anything in an explicit transaction or writing to the primary; sessions can force with `ROUTER SET access_mode = 'read_write'`. It needs connection sharing (`connection_sharing=1`) and comes with session-state caveats (temp tables, user variables pin the connection).

## Deploy
Run Router on each application host (or as a sidecar), not as a central tier: no extra hop, no single point of failure. Router keeps no affinity to any particular server; its metadata cache refreshes periodically and follows group membership changes.

## Health and status
```bash
mysqlsh clusteradmin@db1 -- cluster list-routers
```
In Shell: `cluster.listRouters()`, `cluster.removeRouterMetadata('host::app-router')` for stale ones.

## Gotchas
- Re-bootstrap (`--force`) after cluster rename/rebuild; Router caches metadata servers in its state file.
- Long-lived connections stay on the old primary until it fails: after a planned switchover, Router disconnects RW clients of the demoted member; apps must reconnect and retry.
- Router does not pool connections unless connection sharing is on.

## Verify
`mysql -h127.0.0.1 -P6446 -e 'SELECT @@hostname, @@super_read_only'` returns the primary with 0; on 6447 a secondary with 1; after `cluster.setPrimaryInstance`, 6446 follows.

## Checked

2026-10-31: confirmed the bootstrap default ports 6446/6447 (classic read-write/read-only) and 6448/6449 (X protocol) and --directory/--conf-use-sockets/--account/--account-create options on the MySQL Router bootstrapping page; read-write splitting on bind_port 6450 with access_mode=auto and connection_sharing=1, ROUTER SET/query_attributes routing and unsupported statements on the read-write-splitting pages; same-host deployment guidance and no server affinity on the deploying page (dev.mysql.com 8.4). Removed the REST API port/curl example (not confirmable on the cited pages) and unconfirmed ttl/version details.
Method: documentation only; no commands were run.
