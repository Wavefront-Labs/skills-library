---
id: computing-software.database-administration.cassandra.materialized-view-limits
name: materialized-view-limits
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, materialized-view, mv-repair, base-table-sync, materialized-views, mv, sai-index, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "When to avoid MVs"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/mvs.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/configuration/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Materialized views and their limits

Goal: decide on MVs.
- A view primary key must contain all primary key columns of the base table and can add at most one column that is not in the base primary key.
- Every view primary key column must be restricted with `IS NOT NULL` in the view's WHERE clause.
- Views are enabled by the `materialized_views_enabled` setting in `cassandra.yaml` (previously `enable_materialized_views`).
- Transient replication keyspaces cannot use materialized views.
Verify: base and view row counts match on test data.

## Checked

2026-11-02. Checked against the Materialized Views page (primary key rules, IS NOT NULL) and the configuration page (materialized_views_enabled rename), and Transient Replication (restriction). Removed: the experimental label, 'many teams dual-write' and 'hot view partitions amplify write cost' (not on the pages).

Method: documentation only; no commands were run.
