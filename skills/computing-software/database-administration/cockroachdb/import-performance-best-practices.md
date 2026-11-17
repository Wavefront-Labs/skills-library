---
id: computing-software.database-administration.cockroachdb.import-performance-best-practices
name: import-performance-best-practices
category: computing-software
field: database-administration
product: cockroachdb
tags: [import-performance, csv, avro, secondary-indexes, foreign-keys, data-migration]
level: advanced
status: docs-checked
description: "Speed up CockroachDB IMPORT INTO for large loads: choose CSV or Avro, import schema separately, drop secondary indexes and foreign keys temporarily, sort and split files."
sources:
  - https://www.cockroachlabs.com/docs/stable/import-performance-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shorten large initial loads with `IMPORT INTO`, the fastest ingestion method but one that takes the target table offline.

Threshold: under 100 GiB, no tuning is needed. For larger loads act on three things: format, file splitting, and sorting.

1. Format: use `CSV` (or delimited data, about the same) or `AVRO`; these are processed in parallel by all nodes.
2. Split data into at least as many files as there are nodes (CSV, delimited and Avro support multi-file import), and sort data within each file by the target primary key order. The page reports split-and-sorted imports were best; unsplit and unsorted were about 16 times slower, and either one alone about 2 times slower than both.
3. Import schema separately from data: keep a schema-only SQL file (convert with the Schema Conversion Tool) and a data-only CSV/Avro file, create the table first, then:
```sql
IMPORT INTO customers (id, name)
CSV DATA ('<cloud-storage-url>/customers.csv');
```
Benefit: schema errors surface before waiting on the data load.

Secondary indexes: the job ingests table and index data concurrently, which is slower. For datasets over 100 GiB consider dropping secondary indexes (`DROP INDEX`), importing, then recreating them with `CREATE INDEX` statements run one at a time:
```sql
CREATE INDEX idx1 ON table1;
CREATE INDEX idx2 ON table1;
```
Foreign keys: remove them before the import and add them back afterwards with `ALTER TABLE`.

## Checked

2026-11-03. Confirmed against the import performance page: 100 GiB threshold, formats, at least one file per node, split and sorted test results (about 16 times and 2 times slower), Schema Conversion Tool, secondary index handling, foreign keys. Removed: invented verification step.
Method: documentation only; no commands were run.
