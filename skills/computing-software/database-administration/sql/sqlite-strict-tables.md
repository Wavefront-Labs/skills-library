---
id: computing-software.database-administration.sql.sqlite-strict-tables
name: sqlite-strict-tables
category: computing-software
field: database-administration
product: sql
tags: [sql, sqlite-strict-tables]
level: practitioner
status: docs-checked
description: "Enforce column types in SQLite with STRICT tables."
sources: ["https://www.sqlite.org/stricttables.html", "https://www.sqlite.org/datatype3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STRICT tables

- Add the `STRICT` table option after the closing parenthesis: `CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT NOT NULL, n INT) STRICT;`. Supported from SQLite 3.37.0 (2021-11-27) and enabled per table.
- Every column must declare a type, and it must be one of INT, INTEGER, REAL, TEXT, BLOB or ANY. Other names such as VARCHAR(10) are not allowed.
- A value inserted into a non-ANY column must be NULL (if no NOT NULL constraint) or the declared type. SQLite first tries to coerce it with the usual affinity rules (the string '123' into an INT column becomes the integer 123); if it cannot be converted losslessly, it raises an `SQLITE_CONSTRAINT_DATATYPE` error.
- ANY accepts any kind of data and does no coercion in a STRICT table, so '000123' stays text. In an ordinary table an ANY column converts number-looking strings, so '000123' becomes integer 123.
- Without STRICT, any column except an INTEGER PRIMARY KEY may hold a value of any storage class; declared types only set an affinity.
- `PRAGMA integrity_check` and `PRAGMA quick_check` verify the type of the content of STRICT columns.
- Everything else (CHECK, NOT NULL, FOREIGN KEY, UNIQUE, DEFAULT, COLLATE, generated columns, indexes, AUTOINCREMENT, on-disk format) works as in an ordinary table. An INTEGER PRIMARY KEY column is a rowid alias but an INT PRIMARY KEY column is not.
- Compatibility: a database file with STRICT tables can in general only be read and written by SQLite 3.37.0 or later. Older versions report an error on the keyword.
- Self-check: insert 'abc' into an INT column and expect `SQLITE_CONSTRAINT_DATATYPE`; insert '123' and expect integer 123.

## Checked

2026-11-08. Confirmed against the SQLite pages STRICT Tables and Datatypes In SQLite: the version gate, the allowed type list, the coercion and error behaviour, ANY semantics in strict and ordinary tables, the integrity pragmas, the unchanged features and the backwards-compatibility statement. Removed the unsupported claim that wrong-typed values are always rejected (lossless coercion happens first) and the PostgreSQL docs root source, which does not cover SQLite.

Method: documentation only; no commands were run.
