---
id: computing-software.database-administration.duckdb.duckdb-parquet-encryption
name: duckdb-parquet-encryption
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, parquet, encryption, add-parquet-key, security]
level: advanced
status: docs-checked
description: "Write and read encrypted Parquet files in DuckDB with PRAGMA add_parquet_key and encryption_config, including limitations and measured overhead."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/encryption.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt Parquet output and read it back, knowing what is unsupported.

DuckDB supports encrypted Parquet since 0.10.0 and broadly follows the Parquet Modular Encryption spec.

1. Register a named key in the session (kept in memory only, so repeat it in every session). Keys must be 128, 192 or 256 bits; a base64 form is accepted:

```sql
PRAGMA add_parquet_key('key128', '0123456789112345');
PRAGMA add_parquet_key('key192', '012345678911234501234567');
PRAGMA add_parquet_key('key256', '01234567891123450123456789112345');
PRAGMA add_parquet_key('key256base64', 'MDEyMzQ1Njc4OTExMjM0NTAxMjM0NTY3ODkxMTIzNDU=');
```

2. Write:

```sql
COPY tbl TO 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
```

3. Read (either form):

```sql
COPY tbl FROM 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
SELECT * FROM read_parquet('tbl.parquet', encryption_config = {footer_key: 'key256'});
```
The `footer_key` value is the key's name, not the key material.

Limitations:
- Not compatible with encryption produced by tools such as PyArrow until missing details are implemented.
- The footer and all columns are encrypted with the single `footer_key`. Per-column keys (`column_keys: {key256: ['col0','col1']}`) are in the spec but unsupported; using them raises `Not implemented Error: Parquet encryption_config column_keys not yet implemented`.

Performance: TPC-H `lineitem` at SF1 (6M rows, 15 columns) read in 0.26 s and wrote in 0.99 s unencrypted, versus 0.64 s and 2.21 s encrypted, about 2.5 times slower.

`parquet_file_metadata(f)` returns an `encryption_algorithm` column (see duckdb-parquet-metadata-functions).

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages data/parquet/encryption.md and data/parquet/metadata.md in full. Confirmed: support since 0.10.0, Parquet Modular Encryption, 128/192/256-bit named in-memory keys, all four add_parquet_key examples, COPY and read_parquet forms, both limitations including the column_keys error text, the TPC-H SF1 timings (0.26/0.99 s vs 0.64/2.21 s, about 2.5x), and the `encryption_algorithm` column. Removed: the invented Verify step and the unsupported claim that the column is useful to confirm a file is encrypted (the metadata page only lists the column). Added the metadata page to sources.

Method: documentation only; no commands were run.
