---
id: computing-software.database-administration.cockroachdb.cockroach-start-flags
name: cockroach-start-flags
category: computing-software
field: database-administration
product: cockroachdb
tags: [cockroach-start, node-flags, listen-addr, advertise-addr, locality, join]
level: practitioner
status: docs-checked
description: "Choose the right cockroach start flags for a node: addressing, join, locality, cache and SQL memory, store attributes, cluster name, security and WAL failover."
sources:
  - https://www.cockroachlabs.com/docs/stable/cockroach-start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start a production node with explicit, correct flags.

Networking:
- `--listen-addr` interface and port for node and client connections; `--advertise-addr` what other nodes are told to use (must be resolvable and routable from every node).
- `--sql-addr` / `--advertise-sql-addr` separate SQL listener; `--http-addr` for the DB Console; `--locality-advertise-addr` lets nodes in specific localities use another address (multi-network clusters).
- `--join` (or `-j`) lists node addresses used to discover the cluster; `--experimental-dns-srv` tries SRV records for each join name first.
- Deprecated: `--host`, `--port`, `--advertise-host`, `--http-host`, `--http-port`.

Placement and identity:
- `--locality` key-value pairs such as country, region, zone; a `region` tier is needed to use multi-region features. `--locality-file` is a file alternative.
- `--attrs` colon-separated capability labels; `--cluster-name` plus `--disable-cluster-name-verification` guard against joining the wrong cluster.

Resources:
- `--cache` sizes the Pebble block cache, `--max-sql-memory` bounds SQL working memory (percentage like `.25` or a byte size), `--max-go-memory` defaults to max-sql-memory x 2.25 and cannot exceed 90% of RAM, `--max-disk-temp-storage` caps spill-to-disk, `--max-tsdb-memory` serves DB Console metrics, `--temp-dir` sets spill location.

Security and ops: `--certs-dir`, `--insecure` (non-production only), `--cert-principal-map`, `--tls-cipher-suites`, `--enterprise-encryption` (per store), `--wal-failover`, `--background`, `--pid-file`, `--listening-url-file`, `--socket-dir`, `--clock-device` for a PTP hardware clock.

Verify: node output prints the SQL URL and DB Console URL, and the node shows in `cockroach node status`.

## Checked
2026-11-03. Confirmed on the cockroach start page: each flag named above, the deprecated host/port flags, `--max-go-memory` default (`--max-sql-memory` x 2.25, capped at 90% of RAM), `--experimental-dns-srv`, `--clock-device` for a PTP clock, `--cluster-name` with `--disable-cluster-name-verification`, and `--insecure` for non-production only.
Method: documentation only; no commands were run.
