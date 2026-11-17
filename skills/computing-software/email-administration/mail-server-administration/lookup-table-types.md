---
id: computing-software.email-administration.mail-server-administration.lookup-table-types
name: lookup-table-types
category: computing-software
field: email-administration
product: mail-server-administration
tags: [lookup-table-types, postfix-lookup-tables, postmap, lmdb, hash-table, texthash]
level: practitioner
status: docs-checked
description: "Choose lookup table types (hash, lmdb, cdb, texthash, regexp, pcre) and rebuild them correctly with postmap."
sources:
  - https://www.postfix.org/DATABASE_README.html
  - https://www.postfix.org/LMDB_README.html
  - https://www.postfix.org/postmap.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lookup table types

**Goal:** pick the right database format (DATABASE_README).
## Steps
1. `postconf -m` lists what your build supports.
2. Build: `postmap hash:/etc/postfix/access` (creates `.db`); for lmdb `postmap lmdb:/etc/postfix/access`.
3. `texthash:` reads the file directly, no postmap step, fine for small tables.
4. Regexp/pcre/cidr/texthash files are read as-is; no postmap step (DATABASE_README).
## Failure modes
- Your build may lack a type (`hash:`, `lmdb:`): `postconf -m` lists the supported ones; `lmdb:` is the OpenLDAP LMDB type (LMDB_README).
- Table source updated but the index not rebuilt with `postmap`: lookups use the old index.
## Verify
- `postmap -q key hash:/etc/postfix/access`; `postmap -s` dumps.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): DATABASE_README, LMDB_README, postmap(1).
Confirmed: `postconf -m`, `postmap hash:` / `postmap lmdb:`, `texthash:`, `postmap -q`, `postmap -s`, regexp/pcre/cidr as plain files.
Corrected or removed: the claim that distros are dropping Berkeley DB (not in the docs read), the 'silently ignored' wording.
Method: documentation only; no commands were run.
