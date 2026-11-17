---
id: computing-software.database-administration.mysql.utf8mb4-character-sets-and-collations
name: utf8mb4-character-sets-and-collations
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, utf8mb4, character-set, collation, utf8mb4-0900-ai-ci, utf8mb3, emoji, charset-conversion, illegal-mix-of-collations]
level: practitioner
status: verified
description: "Run MySQL fully on utf8mb4: server/connection/table charsets, choosing a collation, converting utf8mb3 tables, and fixing illegal mix of collations errors."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/charset-unicode-utf8mb4.html
  - https://dev.mysql.com/doc/refman/8.4/en/charset-connection.html
  - https://dev.mysql.com/doc/refman/8.4/en/charset-unicode-conversion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# utf8mb4 character sets and collations

**Goal:** store any Unicode (emoji included) end to end and never see `???` or `Incorrect string value`.

## Why
`utf8` in MySQL historically meant `utf8mb3` (max 3 bytes, no emoji/supplementary chars). Use `utf8mb4` everywhere. MySQL 8.0+ defaults: `character_set_server = utf8mb4`, `collation_server = utf8mb4_0900_ai_ci` (both confirmed on 9.7.4). The `character_set_client`/`connection`/`results` values come from the client, not the server: the Windows `mysql.exe` console client reported `cp850` here, and with it `COLLATE utf8mb4_0900_ai_ci` on a literal failed with error 1253 and a UTF-8 script file with `é` failed with error 1366. Start it with `--default-character-set=utf8mb4`.

## Server config
```ini
[mysqld]
character_set_server = utf8mb4
collation_server     = utf8mb4_0900_ai_ci
[client]
default-character-set = utf8mb4
```

## Collation choice
| Collation | Behaviour |
|---|---|
| `utf8mb4_0900_ai_ci` | UCA 9.0.0 weights, accent- and case-insensitive, NO PAD (MySQL 8 default) |
| `utf8mb4_0900_as_cs` | Accent and case sensitive |
| `utf8mb4_bin` | Byte order; fastest exact compare |
| `utf8mb4_unicode_ci`, `utf8mb4_general_ci` | Older, needed for MariaDB/5.7 compatibility |
MariaDB documents its own `uca1400` collations (its character-set table lists `ucs2_uca1400_ai_ci` and `utf16_uca1400_ai_ci` as defaults from MariaDB 11.5); check the MariaDB collation list before moving dumps between the two, since the MySQL-only `0900` names are not guaranteed there (not run here).

## Connection
Client charset must match what the app sends: `SET NAMES utf8mb4` or the connector's charset option (see your driver's documentation; the JDBC, PyMySQL and Go spellings were not run here). Check `SHOW VARIABLES LIKE 'character_set_%';` from the app connection.

## Converting a table
```sql
ALTER TABLE t CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;  -- rewrites table; use gh-ost/pt-osc for big ones
ALTER DATABASE app CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;        -- default for NEW tables only
```
Index length: InnoDB DYNAMIC row format allows 3072-byte keys = 768 utf8mb4 chars; old COMPACT format limits 767 bytes = `VARCHAR(191)`. Run on 9.7.4 (default `innodb_default_row_format = dynamic`): `VARCHAR(768)` indexed fine, `VARCHAR(769)` gave `ERROR 1071 ... max key length is 3072 bytes`, and with `ROW_FORMAT=COMPACT` `VARCHAR(192)` gave `max key length is 767 bytes` while `VARCHAR(191)` worked.
Find leftovers: `SELECT table_schema, table_name, column_name, character_set_name FROM information_schema.columns WHERE character_set_name IN ('utf8mb3','latin1') AND table_schema NOT IN ('mysql','sys','information_schema','performance_schema');`

## Gotchas
- `Illegal mix of collations` (error 1267) in joins/comparisons: columns with different collations; align them or `COLLATE` explicitly (reproduced with an `utf8mb4_0900_ai_ci` and an `utf8mb4_unicode_ci` column; an explicit `COLLATE` on only one side is not enough when both sides are explicit and different; whether it prevents index use on the converted side was not tested).
- Data double-encoded (latin1 column holding UTF-8 bytes) needs a conversion to binary first, then to utf8mb4, not a direct convert: a latin1 column holding bytes `C3A9` became `C383C2A9` after `CONVERT TO CHARACTER SET utf8mb4`, but `MODIFY c VARBINARY(20)` then `MODIFY c VARCHAR(20) CHARACTER SET utf8mb4` gave back `é` (`C3A9`).
- Changing collation changes uniqueness: `ai_ci` treats `resume` and `résumé` as equal, so unique indexes may fail on conversion (`ERROR 1062 Duplicate entry` when converting a latin1 unique column holding both).
- Inserting a 4-byte character into a `utf8mb3` column fails with `ERROR 1366 Incorrect string value` in strict mode.

## Verify
Insert `'😀'` from the application, read it back unchanged, and `SELECT HEX(col)` shows `F09F9880` (confirmed: `hex = F09F9880`, `LENGTH = 4`, `CHAR_LENGTH = 1`).
