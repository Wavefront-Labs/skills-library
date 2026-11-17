---
id: computing-software.database-administration.scylladb.admin-scylla-sstable-tool
name: admin-scylla-sstable-tool
category: computing-software
field: database-administration
product: scylladb
tags: [scylla-sstable, sstable, dump-data, validate, schema-detection, object-storage]
level: advanced
status: docs-checked
description: "The scylla sstable offline tool: operations (dump-data, validate, scrub, query, script, upgrade, write), directory and s3:// paths, schema sources and auto-detection order."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/scylla-sstable.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# scylla sstable

Built into the ScyllaDB executable: `scylla sstable <operation> <path to SStable>...`. Run `scylla sstable --help` for details.

Operations: `dump-data`, `dump-index`, `dump-compression-info`, `dump-summary`, `dump-statistics`, `dump-scylla-metadata`, `dump-schema`, `validate`, `scrub`, `validate-checksums`, `decompress`, `write`, `shard-of`, `query`, `script`, `upgrade`, `filter`, `split`, `layout`. dump-data can produce output larger than the binary file; filter with `--partitions`.

Input:
- More than one SSTable may be given; or pass a table directory to process every sealed SSTable in it.
- An SSTable with missing components fails the run. The data directory of a running node is a moving target (compaction can delete a table while loading), so add `--ignore-incomplete-sstables` to report and skip them.
- Paths can be `s3://bucket/prefix/sstable-TOC.txt` or `gs://...`, including live object-storage SSTables (layout `sstables/<id>/Data.db`, `TOC.txt`, with version and format kept as attributes on TOC.txt). Credentials must be in the environment, and `--scylla-yaml-file` must contain a matching object-storage endpoint.

Schema: every operation needs one. Explicit sources: `--schema-file` (DDL file), `--system-schema --keyspace K --table T` (system tables only), `--schema-tables` (read the schema tables from the data directory, with `--scylla-yaml-file`, `--scylla-data-dir`), `--sstable-schema --keyspace K --table T` (serialization headers).

Default auto-detection order, stopping at the first success: a `schema.cql` file next to the SSTable (always wins, to allow manual override); deduce data dir and table from the path; load from the data directory via the config (`./conf/scylla.yaml`, `SCYLLA_CONF`, `SCYLLA_HOME`, else `/var/lib/scylla`; needs `--keyspace` and `--table`); the SSTable headers.

## Checked

2026-11-04: operations, input rules, object-storage paths and layout, schema sources and the auto-detection order confirmed against the ScyllaDB scylla-sstable documentation page. Removed the unsupported closing advice about offline use and copies; added the filter, split and layout operations the page lists.

Method: documentation only; no commands were run.
