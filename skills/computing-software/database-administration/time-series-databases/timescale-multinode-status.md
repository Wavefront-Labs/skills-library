---
id: computing-software.database-administration.time-series-databases.timescale-multinode-status
name: timescale-multinode-status
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-multinode, timescale-multinode-status, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Know what happened to TimescaleDB multi-node so you do not start a new design on it."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-node deprecation

**Goal:** Know what happened to TimescaleDB multi-node so you do not start a new design on it.

## Steps
- Multi-node (access node plus data nodes, `add_data_node`, `create_distributed_hypertable`) is sunsetted. The docs mark it as sunsetted from v2.14.x and say TimescaleDB v2.13 is the last release with multi-node support, for PostgreSQL 13, 14 and 15.
- Do not start new designs on it; the docs point to a deprecation notice in the TimescaleDB repository.
- For existing clusters, plan a move to single-node hypertables or another approach before upgrading past 2.13.
- Data can be moved out with `COPY` per time range (see the pg_dump / restore skill) and loaded into one hypertable.
- Read scaling: use streaming replicas.
- For horizontal write scaling, shard by tenant at the application layer (a design option, not a documented feature).

**Gotcha:** Every multi-node page in the docs carries the sunset warning; treat the feature as unavailable on current releases.

## Verify
- `SELECT * FROM timescaledb_information.data_nodes;` is empty or absent on the target.
- Application writes go to a single hypertable successfully.

## Checked

Checked 2026-11-03 against the timescale/docs repository: _partials/_multi-node-deprecation, self-hosted/multinode-timescaledb/index and about-multinode, api/distributed-hypertables, api/informational-views/data_nodes. Removed: 'removed in 2.14 (confirm)' (replaced by the documented wording), the 'tens of TB' vendor claim and the claim that upgrades across the removal version are blocked.

Method: documentation only; no commands were run.
