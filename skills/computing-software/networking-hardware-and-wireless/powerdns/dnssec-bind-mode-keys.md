---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-bind-mode-keys
name: dnssec-bind-mode-keys
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, bind-backend, create-bind-db, hybrid, bind-dnssec-db, sqlite3]
level: practitioner
status: docs-checked
description: "DNSSEC for BIND-backend zones in PowerDNS: create-bind-db and bind-dnssec-db setup, and hybrid mode with keys in a database backend plus the manual domains insert."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC keys with the BIND backend

BIND mode (keys in their own SQLite3 database):
1. `pdnsutil create-bind-db /var/lib/powerdns/bind-dnssec-db.sqlite3`
2. Set `bind-dnssec-db` in `pdns.conf` to that path.
3. Restart PowerDNS.
4. Run `pdnsutil zone secure` (`secure-zone` before 5.0) and the other pdnsutil commands on the BIND zones.

This database is not the generic SQLite3 backend's database.

Hybrid BIND mode (zone files in BIND, keys in a database backend):
- The BIND backend serves records with full DNSSEC support but cannot store keys, so include at least one database backend in `launch`.
- Generic SQLite3 is recommended, as it needs no server. It must use the normal generic-sqlite3 schema; a database from `create-bind-db` will not work.
- A manual insert is needed to create a zone ID in the key backend:
```
insert into domains (name, type) values ('powerdnssec.org', 'NATIVE');
```
- Enable with `bind-hybrid`.

## Checked

2026-11-04. Read dnssec/modes-of-operation.rst (BIND-mode and hybrid sections) and confirmed the create-bind-db path, bind-dnssec-db, restart, pre-5.0 command name, hybrid launch requirement, SQLite3 recommendation and schema note, and the manual domains insert. Nothing removed.

Method: documentation only; no commands were run.
