---
id: computing-software.database-administration.sql.sql-identity-sequences-and-uuid-keys
name: sql-identity-sequences-and-uuid-keys
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-surrogate-keys, identity-columns, sequences, uuid-v7, id-generation]
level: practitioner
status: docs-checked
description: "Pick surrogate key generation: identity columns, sequences and UUIDs, with gap and index implications."
sources: ["https://www.postgresql.org/docs/current/sql-createtable.html", "https://www.postgresql.org/docs/current/functions-sequence.html", "https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.postgresql.org/docs/current/datatype-uuid.html", "https://www.postgresql.org/docs/current/functions-uuid.html", "https://www.sqlite.org/autoinc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surrogate keys

- Standard syntax in PostgreSQL: `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`. The column gets an implicit sequence and is implicitly NOT NULL. With `ALWAYS`, an explicit value in INSERT is accepted only with `OVERRIDING SYSTEM VALUE`, and an UPDATE to anything but `DEFAULT` is rejected. With `BY DEFAULT`, a user value takes precedence. `COPY` always uses supplied values.
- `serial`, `bigserial` and `smallserial` are only a notational shorthand for a sequence-backed column. `integer` holds up to 2147483647 and `bigint` up to 9223372036854775807, so choose `bigint` unless the table is certain to stay small.
- SQLite: a column declared `INTEGER PRIMARY KEY` is an alias for the 64-bit signed `ROWID` (except in WITHOUT ROWID tables) and is filled automatically, usually one more than the current maximum. `AUTOINCREMENT` additionally prevents reuse of ids from deleted rows, at extra CPU, memory and I/O cost, and the SQLite docs say to avoid it unless needed. Failed inserts can still leave gaps.
- PostgreSQL sequences are not transactional: `nextval` values are not reclaimed when a transaction aborts, and a crash can also leave gaps, as can `INSERT ... ON CONFLICT`. PostgreSQL states its sequences cannot give gapless numbering. `setval` is not undone by rollback either. If a number must be gap-free (invoice numbers), keep a separate counter updated under a lock.
- After restoring or bulk loading explicit ids, move the sequence past the maximum with `setval('<sequence name>', (SELECT max(id) FROM t))`. `setval(seq, n)` makes the next `nextval` return `n + 1`; with a third argument `false` it returns `n`.
- `nextval` is atomic: concurrent sessions each get a distinct value. A sequence is unique within one database only; for distributed systems the PostgreSQL docs say UUIDs give a better uniqueness guarantee.
- PostgreSQL has native `uuid` generation for RFC 9562 versions 4 and 7: `gen_random_uuid()` / `uuidv4()` return a random v4, and `uuidv7()` returns a time-ordered v7 (millisecond Unix timestamp plus sub-millisecond part and random bits). `uuid_extract_timestamp()` reads the timestamp back from v1 or v7. UUIDs can also be generated outside the database. Store them in the native 128-bit `uuid` type, not text.
- Expose opaque public ids if sequential ids would leak counts.

## Checked

2026-11-08. Read: PostgreSQL `CREATE TABLE` identity option text, 9.17 Sequence Manipulation Functions, 8.1 numeric types (serial and integer ranges), 8.12 UUID type, 9.14 UUID functions, SQLite AUTOINCREMENT page. Removed claims the pages do not support: version numbers for identity (PostgreSQL 10, Oracle 12c), `gen_random_uuid()` in 13 and `uuidv7()` in 18, other engines' syntax (MySQL `AUTO_INCREMENT`, SQL Server `IDENTITY`), and the B-tree page-split/locality argument for v7 over v4 (the PostgreSQL pages say only that each UUID version has distinct benefits and drawbacks). `pg_get_serial_sequence` was not read, so the example uses a placeholder sequence name.
Method: documentation only; no commands were run.
