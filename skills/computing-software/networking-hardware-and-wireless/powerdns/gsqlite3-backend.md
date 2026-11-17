---
id: computing-software.networking-hardware-and-wireless.powerdns.gsqlite3-backend
name: gsqlite3-backend
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, gsqlite3, sqlite3, backend, zone2sql, pragma, wal]
level: practitioner
status: docs-checked
description: "Set up the PowerDNS gsqlite3 backend: launch, gsqlite3-database and pragma settings, schema file, importing a BIND zone with zone2sql, and SQLite caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/generic-sqlite3.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gsqlite3 backend

Setup:
1. In `pdns.conf` set `launch=gsqlite3` and `gsqlite3-database=/path/to/powerdns.sqlite3`.
2. Create the schema from `modules/gsqlite3backend/schema.sqlite3.sql` in the source tree; it serves primary, secondary and autosecondary use.
3. Load data by AXFR, by hand with the `sqlite3` program, or from a BIND config:
   `zone2sql --named-conf=/path/to/named.conf --gsqlite | sqlite3 powerdns.sqlite3`
4. Start PowerDNS; it logs that it connected to the database.

Settings:
- `gsqlite3-database`: path of the database file.
- `gsqlite3-pragma-journal-mode`: default `WAL`; leave empty to keep the file's existing mode.
- `gsqlite3-pragma-synchronous`: the synchronous pragma; the page says to set it to `0` for speed.
- `gsqlite3-pragma-foreign-keys`: turn on foreign key constraints.
- `gsqlite3-dnssec`: enable DNSSEC handling.

Caveats:
- Run `analyze;` after a large import, or SQLite may pick very poor indexes.
- Never swap the database file under a running server. If you distribute it with rsync, stop PowerDNS first, then restart.
- Only SQLite 3 is supported, not SQLite 2.
- Building from source: `./configure --with-modules="gsqlite3"`; most binary releases already include it.

## Checked

2026-11-04. Read backends/generic-sqlite3.rst in full and confirmed setup steps, zone2sql command, pragma settings and the WAL default, analyze warning, rsync warning, SQLite 3 only and the configure line. Reworded the synchronous pragma note to what the page says (set to 0 for speed) and dropped an unsupported durability remark.

Method: documentation only; no commands were run.
