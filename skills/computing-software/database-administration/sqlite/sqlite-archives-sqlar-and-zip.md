---
id: computing-software.database-administration.sqlite.sqlite-archives-sqlar-and-zip
name: sqlite-archives-sqlar-and-zip
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlar, sqlite-archive, zipfile, sqlite3-shell, sqlite-cli]
level: practitioner
status: verified
description: "Use SQLite archives (.archive / sqlite3 -A) to bundle files into a single queryable database, and read or write ZIP files through the zipfile virtual table."
sources:
  - https://sqlite.org/sqlar.html
  - https://sqlite.org/cli.html#sqlite_archive_support
  - https://sqlite.org/zipfile.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLite archives (sqlar) and zip files

**Goal:** a transactional, single-file container of files you can also query with SQL (deploy bundles, asset packs, config snapshots).

## Create, list, extract
```bash
sqlite3 assets.sqlar -Acv images/ css/        # create (-c), verbose
sqlite3 assets.sqlar -At                      # list
sqlite3 assets.sqlar -Ax                      # extract all into cwd
sqlite3 assets.sqlar -Ax images/logo.png      # extract one
sqlite3 assets.sqlar -Au css/site.css         # update (add or replace newer)
sqlite3 assets.sqlar -Ai new/                  # insert
```
Inside the shell: `.archive --create --file assets.sqlar images/`. `-C DIR` (read/extract files from DIR) is an option letter of the first argument, so write `-AxvC ex3` (value follows); `-Ax -C ex3` treated `-C` as a member name (`not found in archive: -C`). `-Au` is "add or update files with changed mtime", `-Ai` is "like -u but always add", `-r` removes (`.help archive`).
On Windows 3.54.1, passing `images/` with a trailing slash stored the member as `images//logo.png` and a later `-Ax` failed with `failed to create directory: images/`; pass `images` without the slash.

## Format
A table in any SQLite database:
```sql
CREATE TABLE sqlar(name TEXT PRIMARY KEY, mode INT, mtime INT, sz INT, data BLOB);
```
`data` is zlib-compressed when smaller (`sz` = original size; equal length means stored raw): in a test a repetitive 8,500-byte CSS file stored as 64 bytes, while a 5,000-byte random file and a 7-byte JSON file were stored raw (`sz` = `length(data)`). Because it is just a table, you can add it to an application database and update files transactionally.
```sql
SELECT name, sz, length(data) FROM sqlar ORDER BY sz DESC LIMIT 10;
SELECT sqlar_uncompress(data, sz) FROM sqlar WHERE name='config/app.json';
```

## ZIP files directly
```bash
sqlite3 -Atvf release.zip              # the archive commands also accept .zip files
```
SQL access via the `zipfile` virtual table (shell includes it):
```sql
SELECT name, sz, mtime FROM zipfile('release.zip');   -- worked on a zip written by Python's zipfile
CREATE VIRTUAL TABLE temp.z USING zipfile('new.zip');
INSERT INTO temp.z(name, data) VALUES ('hello.txt', 'hi');
```

## Comparison with ZIP
sqlar supports atomic updates and SQL queries; ZIP has universal tooling. Both compress each file separately (a ratio comparison was not measured).

## Verify
`sqlite3 assets.sqlar -At | wc -l` equals the source file count; extract to an empty dir and `diff -r` against the originals.
