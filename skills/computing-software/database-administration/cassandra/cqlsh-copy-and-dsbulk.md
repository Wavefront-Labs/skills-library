---
id: computing-software.database-administration.cassandra.cqlsh-copy-and-dsbulk
name: cqlsh-copy-and-dsbulk
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, copy-from, copy-to, dsbulk, bulk-loading, cqlsh-copy, cdc, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Importing and exporting CSV with cqlsh COPY"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/cqlsh.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cqlsh COPY and DSBulk

Goal: import and export tables.
- `COPY ks.t (a,b) FROM 'f.csv' WITH HEADER = true;` suits small data.
- `COPY ... TO` exports and `COPY ... FROM` copies data from a CSV file into a table; both take `WITH` options.
Verify: row counts match between source and target.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `COPY TO` / `COPY FROM` syntax and the `HEADER` option (cqlsh page). Removed: the DataStax Bulk Loader (dsbulk) commands, whose documentation was unreachable.

Method: documentation only; no commands were run.
