---
id: computing-software.database-administration.duckdb.duckdb-attach-detach
name: duckdb-attach-detach
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, attach, detach, encryption, read-only, storage-version, sqlite]
level: practitioner
status: docs-checked
description: "ATTACH and DETACH DuckDB databases: aliases, ATTACH options, read-only HTTP/S3, STORAGE_VERSION, AES encryption keys and ciphers, and the single-database write rule."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/attach.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: open additional databases in one session, safely.

```sql
ATTACH 'file.db';                         -- alias inferred: file
ATTACH 'file.db' AS file_db (READ_ONLY);
ATTACH IF NOT EXISTS 'file.db' AS file_db;
ATTACH OR REPLACE 'file2.db' AS file_db;  -- detaches and replaces the alias
ATTACH 'sqlite_file.db' AS sqlite_db (TYPE sqlite);
ATTACH 'file.db' (BLOCK_SIZE 16_384, ROW_GROUP_SIZE 2048);
DETACH file_db;
SHOW DATABASES;
```

Attachments are not persisted: re-attach each session. HTTP(S) and S3 attaches are read-only by default (same as adding `(READ_ONLY)`).

Options: `ACCESS_MODE` (`AUTOMATIC` default, `READ_ONLY`, `READ_WRITE`), `COMPRESS` (in-memory databases only), `TYPE` (`DUCKDB` default or `SQLITE`; MySQL/PostgreSQL deduced from the string), `BLOCK_SIZE` (power of two in [16384, 262144], default 262144, new files only), `ROW_GROUP_SIZE` (default 122880), `STORAGE_VERSION` (default `v1.0.0`), `ENCRYPTION_KEY`, `ENCRYPTION_CIPHER` (`CBC`, `CTR`, `GCM`).

Storage version: `ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');` opts into newer features; the file cannot be opened by older DuckDB releases than that version.

Encryption: AES-256 in GCM mode by default; covers the database file, WAL and temp files. `ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'quack_quack');` Add `ENCRYPTION_CIPHER 'CBC'` or `'CTR'` to change mode. `LOAD httpfs;` first for faster OpenSSL instead of the built-in mbedtls. Encryption implies storage version 1.4.0 or later. The docs warn it does not yet meet NIST requirements.

DETACH releases file locks. You cannot detach the default database; first `ATTACH ':memory:' AS memory_db; USE memory_db;`. Closing a client connection (e.g. Python `close()`) does not release locks because the main DuckDB instance holds the file handles.

Transactions: one transaction per database, started lazily (`SET immediate_transaction_mode = true` starts them eagerly). A single transaction can only write to one attached database, else: `a single transaction can only write to a single attached database`. Name resolution is in `duckdb-catalog-search-path`.

Verify: `SHOW DATABASES;`.

## Checked

2026-11-07. Read the ATTACH and DETACH Statements page in full and confirmed the examples, options table (names, defaults, BLOCK_SIZE range, TYPE values, ciphers), read-only HTTP and S3 default, STORAGE_VERSION semantics, encryption defaults and the NIST warning, DETACH and default-database rule, Python close() warning, lazy per-database transactions with `immediate_transaction_mode`, and the single-database write error text. Nothing removed.

Method: documentation only; no commands were run.
