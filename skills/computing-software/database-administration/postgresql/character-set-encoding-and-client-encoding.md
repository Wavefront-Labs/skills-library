---
id: computing-software.database-administration.postgresql.character-set-encoding-and-client-encoding
name: character-set-encoding-and-client-encoding
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, client-encoding, server-encoding, utf8, character-set, encoding-conversion, localization]
level: practitioner
status: docs-checked
description: "Choose the PostgreSQL database encoding, set client_encoding correctly, and fix 'invalid byte sequence' and 'character has no equivalent' errors."
sources:
  - https://www.postgresql.org/docs/current/multibyte.html
  - https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-CLIENT-ENCODING
  - https://www.postgresql.org/docs/current/sql-createdatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character set encodings and client_encoding

## Rules
- The **server encoding** is fixed per database at `CREATE DATABASE` (cannot be changed later). Use `UTF8` for everything new.
- `SQL_ASCII` is "a declaration of ignorance about the encoding": no conversion or validation is done for non-ASCII bytes. The docs call it unwise unless all your data is ASCII.
- The **client encoding** tells the server what bytes the client sends/expects; the server converts on the fly.

```sql
SELECT datname, pg_encoding_to_char(encoding), datcollate, datctype FROM pg_database;
SHOW server_encoding; SHOW client_encoding;
CREATE DATABASE app TEMPLATE template0 ENCODING 'UTF8' LOCALE 'en_US.UTF-8';
```
`TEMPLATE template0` is required when the encoding/locale differs from the template's: copying any other database cannot change them, because that might result in corrupt data.

## Setting client_encoding
- libpq takes it from `PGCLIENTENCODING`, or the connection parameter `client_encoding=auto` derives it from the client locale (`LC_CTYPE` on Unix). In psql, `\encoding` changes it on the fly. If the client encoding is `SQL_ASCII`, conversion is disabled.
- Per connection: `SET client_encoding = 'UTF8';` or `options='-c client_encoding=UTF8'` in the DSN.
- Per role/database: `ALTER ROLE legacy_app SET client_encoding = 'LATIN1';`

## Errors and fixes
| Error | Meaning | Fix |
|---|---|---|
| `invalid byte sequence for encoding "UTF8": 0xe9 0x20` | client sent Latin-1 bytes labelled as UTF-8 | set client_encoding to the real encoding (LATIN1/WIN1252), or convert the file to UTF-8 before loading |
| `character with byte sequence ... in encoding "UTF8" has no equivalent in encoding "LATIN1"` | client encoding cannot represent the stored char | use UTF8 on the client |
| garbage like `Ã©` | double-encoded: UTF-8 bytes stored after being treated as Latin-1 | fix at source; repair with `convert_from(convert_to(col,'LATIN1'),'UTF8')` on affected rows, test first |

## Loading files
```sql
\copy t FROM 'data.csv' WITH (FORMAT csv, HEADER, ENCODING 'WIN1252')
```
`ENCODING` on COPY overrides client_encoding for that file only.

## Migrating SQL_ASCII to UTF8
Dump, find and convert the non-UTF-8 byte sequences (the server cannot do this for you, since `SQL_ASCII` does no validation), then restore into a database created with `TEMPLATE template0 ENCODING 'UTF8'`.

## Gotchas
- The character with code zero cannot appear in a string constant or quoted identifier; use `bytea` for binary data.
- `length()` counts characters, `octet_length()` bytes; varchar(n) limits characters.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Character Set Support chapter (server encoding set per database at creation and unchangeable by copying templates other than `template0`; `SQL_ASCII` behaviour; client encoding via `\encoding`, `SET client_encoding`, `PGCLIENTENCODING`; conversion errors; client `SQL_ASCII` disables conversion), libpq `client_encoding` including `auto`, COPY `ENCODING` option (default is the client encoding), syntax rule for the zero character, character-type length in characters, and the `convert_to`/`convert_from` function signatures. The two quoted error messages were confirmed in the server source (`mbutils.c`, REL_18_STABLE). Removed the `iconv` commands and the Windows-console remark, which no PostgreSQL documentation covers.
Method: documentation only; no commands were run.
