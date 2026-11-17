---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovsdb-tool-basics
name: ovsdb-tool-basics
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovsdb-tool, ovsdb, create, compact, convert, show-log, create-cluster, join-cluster]
level: practitioner
status: docs-checked
description: "Manage OVSDB database files offline with ovsdb-tool: create, compact, convert, show-log, query, transact, and create-cluster, join-cluster, check-cluster."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovsdb-tool.1.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovsdb-tool
ovsdb-tool manages OVSDB database files (ovsdb-tool(1)). Defaults when `db` or `schema` is omitted: db `/usr/local/etc/openvswitch/conf.db`, schema `/usr/local/share/openvswitch/vswitch.ovsschema`. Standalone and active-backup databases share one on-disk format and clustered databases use another; some commands work with only one, as noted.

Creation (these never overwrite an existing file; delete the old file first):
- `create [db [schema]]` makes an empty standalone or active-backup database with the schema (a JSON schema file). `cp` copies a database with its schema and data.
- `[--election-timer=ms] create-cluster db contents local` initialises the first server of a cluster of 3 or more. `local` is `protocol:ip:port` with protocol tcp or ssl (IPv6 in square brackets), used for cluster traffic and not the OVSDB client port. `contents` is a schema file or a standalone database file. The leader election timer defaults to 1000 ms; `--election-timer` takes 100 to 600000 ms.
- `[--cid=uuid] join-cluster db name local remote...` initialises each later server; `name` is the schema or database name from create-cluster (find it with `schema-name` or `db-name`). It does no network access: the server joins the first time ovsdb-server serves the file. `--cid` pins the cluster ID so it cannot join the wrong cluster.
- `cluster-to-standalone db clusterdb` makes a standalone file from a cluster database when the cluster is down and cannot be revived.

Versions and conversion:
- `convert [db [schema [target]]]` rewrites db to the schema, in place or to a new `target` file that must not exist. In-place conversion cannot be done while ovsdb-server is serving the database (stop it, or use ovsdb-client convert). It can cause unrecoverable data loss; back up first. Standalone and active-backup only.
- `needs-conversion [db [schema]]` prints yes or no. `db-version`, `schema-version`, `db-cksum`, `schema-cksum` print versions and checksums (blank if none). `compare-versions a op b` exits 0 if true, 2 if false, 1 on error.

Other commands:
- `compact [db [target]]` writes a compacted version, in place or to `target`. Not normally needed since ovsdb-server compacts automatically. It does not work while the db is served or locked, or for clustered databases; use `ovs-appctl ovsdb-server/compact` instead.
- `[--rbac-role=role] query [db] transaction` opens the db read-only (safe alongside ovsdb-server) and prints results of a JSON transaction; modifications have no effect. `transact [db] transaction` executes and commits changes; it does not work while the db is served or locked. Neither works on clustered databases (use ovsdb-client). Default role is superuser.
- `[-m | --more]... show-log [db]` summarises the log with times and comments; one `-m` adds records added, deleted or modified per transaction, two add the changed column values. It works on both formats, with different output.
- `check-cluster db...` checks databases collected from the servers of one cluster for consistency (warnings on stdout, errors on stderr with exit 1).
- `db-name`, `schema-name`, `db-cid` (clustered only; error if not yet known), `db-sid`, `db-local-address`, `db-is-clustered`, `db-is-standalone` (exit 0 for yes, 2 for no, 1 for error).

## Checked
2026-11-04. Confirmed against ovsdb-tool(1). Removed the invented vtep.db example, the Verify line and the "can corrupt state" gotcha (the page only says the commands do not work while the file is served or locked), and added the clustered-database limits and defaults.
Method: documentation only; no commands were run.
