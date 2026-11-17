---
id: computing-software.database-administration.query-optimisation.bulk-loading-copy-load-data-bulk-insert
name: bulk-loading-copy-load-data-bulk-insert
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, bulk-loading, copy-command, load-data-infile, bulk-insert, query-patterns]
level: practitioner
status: draft
description: "Load large data volumes fast with COPY (PostgreSQL), LOAD DATA (MySQL) and BULK INSERT/bcp (SQL Server): batching, index and constraint handling, logging and verification."
sources:
  - https://www.postgresql.org/docs/current/populate.html
  - https://dev.mysql.com/doc/refman/8.4/en/load-data.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/import-export/prerequisites-for-minimal-logging-in-bulk-import
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk loading (COPY / LOAD DATA / BULK INSERT)

## Use the native bulk path, not row-by-row INSERTs
Single-row inserts with a commit each are limited by round trips and fsync. Bulk paths stream rows with minimal per-row overhead.

## PostgreSQL
```sql
\copy staging_orders FROM 'orders.csv' WITH (FORMAT csv, HEADER true)       -- client-side file (psql)
COPY staging_orders FROM STDIN WITH (FORMAT csv);                            -- from driver (copy_from / CopyManager)
```
Faster still for initial loads:
- Load into a table created in the same transaction with `wal_level = minimal` (skips WAL), or use `UNLOGGED` staging tables.
- Drop/disable secondary indexes and FKs, load, then `CREATE INDEX` (raise `maintenance_work_mem`) and re-add FKs (`NOT VALID` then `VALIDATE`).
- Temporarily raise `max_wal_size` to avoid checkpoint storms.
- `ANALYZE` afterwards.
- PG17: `COPY ... ON_ERROR ignore` skips malformed rows (`LOG_VERBOSITY verbose` reports them).

## MySQL
```sql
LOAD DATA LOCAL INFILE 'orders.csv' INTO TABLE orders
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
(id, customer_id, total, @created) SET created_at = STR_TO_DATE(@created, '%Y-%m-%d %H:%i:%s');
```
- Needs `local_infile=ON` on server and client for LOCAL; server-side files restricted by `secure_file_priv`.
- Sort input by primary key (InnoDB clustered inserts in order); `SET unique_checks=0, foreign_key_checks=0` for trusted data; MySQL Shell `util.importTable()` loads in parallel chunks.
- Multi-row `INSERT ... VALUES (...),(...)` with 1,000-5,000 rows per statement is the fallback.

## SQL Server
```sql
BULK INSERT dbo.orders FROM '\\fileserver\loads\orders.csv'
WITH (FORMAT = 'CSV', FIRSTROW = 2, TABLOCK, BATCHSIZE = 100000, MAXERRORS = 0);
```
`bcp dbo.orders in orders.dat -S srv -d db -T -n -b 100000 -h "TABLOCK"`. Minimal logging requires SIMPLE or BULK_LOGGED recovery, `TABLOCK`, and a heap or empty clustered index (2016+ rules). `SqlBulkCopy` from .NET.

## General
- Load into staging, validate, then `INSERT ... SELECT` into the real table (or partition switch / attach) to keep production consistent.
- Batch commits (10k-100k rows) for restartability.
- Disable triggers deliberately or accept their cost.

## Verify
Row counts match the source file (`wc -l` minus header), constraint checks pass after re-enabling, and spot-checked values (dates, decimals, encodings) are correct.
