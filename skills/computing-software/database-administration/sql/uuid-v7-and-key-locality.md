---
id: computing-software.database-administration.sql.uuid-v7-and-key-locality
name: uuid-v7-and-key-locality
category: computing-software
field: database-administration
product: sql
tags: [sql, uuid-v7-and-key-locality]
level: advanced
status: docs-checked
description: "Weigh UUID primary keys against index locality and pick time-ordered ids."
sources: ["https://www.postgresql.org/docs/current/datatype-uuid.html", "https://www.postgresql.org/docs/current/functions-uuid.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UUID keys and index locality

- Random version 4 UUIDs have no creation-time order; version 7 UUIDs are time-ordered (48-bit millisecond Unix timestamp plus sub-millisecond bits plus random). The PostgreSQL manual does not discuss b-tree insert locality, so measure the effect of key choice on your own load.
- PostgreSQL manual (version 18 pages): `gen_random_uuid()` and `uuidv4()` generate version 4; `uuidv7([shift interval])` generates version 7 and errors if a shifted timestamp falls outside 1970-01-01 to about year 10889. Check which version you run before relying on `uuidv7()`; otherwise generate ids in the application or use the `uuid-ossp` module for other algorithms.
- `uuid_extract_timestamp(uuid)` returns a timestamp for version 1 or 7 and NULL otherwise; the value is not necessarily the exact generation time. `uuid_extract_version(uuid)` returns the version.
- The `uuid` type stores any version as a 128-bit value (RFC 9562); store ids as `uuid`, not as text.
- UUIDs give a better uniqueness guarantee across distributed systems than sequences, which are unique only within one database.
- Self-check: compare index size and insert rate for bigint, random uuid and time-ordered uuid keys on a test load.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 manual pages UUID Type and UUID Functions. Removed the "13+" version gate for `gen_random_uuid()`, the claim that `uuidv7()` first arrived in 18, the 16 versus 36 byte sizes, and the page-split explanation, none of which the pages state.
Method: documentation only; no commands were run.
