---
id: computing-software.database-administration.tidb.tidb-sql-to-key-value-mapping
name: tidb-sql-to-key-value-mapping
category: computing-software
field: database-administration
product: tidb
tags: [tidb, key-value-mapping, rowid, tableid, indexid, coprocessor, pushdown, tidb-rowid, schema-version]
level: sme
status: docs-checked
description: "Learn how TiDB encodes table rows and indexes as TiKV keys, how metadata and schema versions are stored, and why operators are pushed down to storage."
sources: ["https://docs.pingcap.com/tidb/stable/tidb-computing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb sql to key value mapping

Row encoding. Each table gets a cluster-unique `TableID` and each row a table-unique `RowID`; if the table has an integer primary key, that value is used as the RowID. A row becomes:

```
Key:   tablePrefix{TableID}_recordPrefixSep{RowID}
Value: [col1, col2, col3, col4]
```

Index encoding uses an `IndexID`. Primary keys and unique indexes map the indexed values to the RowID; non-unique indexes append the RowID to the key and store a null value:

```
unique:     t{TableID}_i{IndexID}_{indexedColumnsValue} -> RowID
non-unique: t{TableID}_i{IndexID}_{indexedColumnsValue}_{RowID} -> null
```

The constants are `t` (tablePrefix), `r` (recordPrefixSep) and `i` (indexPrefixSep). All rows of a table share a prefix and all entries of an index share a prefix, so they sit contiguously in key order. Example from the docs: with TableID 10, rows land at `t10_r1`, `t10_r2`, `t10_r3`, and a non-unique index `idxAge` with IndexID 1 gives `t10_i1_10_1` and similar.

Metadata. Databases and tables are stored in TiKV under keys with the `m_` prefix. The global schema version lives in PD at `/tidb/ddl/global_schema_version` and increments with each DDL state change, because schema changes are applied online.

Execution. A naive plan scans a key range and filters in the TiDB server, costing at least one RPC per row. Instead TiDB pushes predicates (such as `name = "TiDB"`) and aggregates (such as partial `count(*)`) down to the storage nodes, so each returns one aggregated result.

## Checked

2026-11-09: key encodings, prefix constants, the User table example, `m_` metadata prefix, the PD schema-version key and the pushdown reasoning confirmed against the TiDB Computing page (pingcap/docs tidb-computing.md, read in full).

Method: docs-checked 2026-11-09 against pingcap/docs tidb-computing.md
