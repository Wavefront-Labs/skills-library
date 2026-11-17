---
id: computing-software.systems-network-administration.openldap.slapadd-loading
name: slapadd-loading
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slapadd, bulk-load, quick-mode, ldif-import, restore]
level: practitioner
status: docs-checked
description: "Load LDIF into an OpenLDAP database offline with slapadd: -l, -n, -b, -q quick mode, -s, -S, -w, -u, -j resume, ownership and safety caveats."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapadd&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/dbtools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapadd loading
```
slapadd -F /usr/local/etc/openldap/slapd.d -b "dc=example,dc=com" -l data.ldif
slapadd -q -n 1 -l big.ldif
```
Options:
- `-l file` (else stdin); `-b suffix` or `-n dbnum` (not together; `-n 0` is the existing config database).
- `-q` quick mode: fewer integrity checks, much faster; any error or interruption leaves an unusable database. Incompatible with `-o value-check=yes`.
- `-s` disable schema checking (special objects only); `-o schema-check={yes|no}` (default yes).
- `-S SID` server ID in generated entryCSN (default 0); `-w` rewrite contextCSN after load; use only to seed a fresh syncrepl provider.
- `-u` dry run; `-c` continue on errors; `-g` skip subordinate databases; `-j lineno` resume an aborted load after fixing LDIF.

Rules:
- Stop slapd first so the database stays consistent.
- Files are owned by the user running slapadd; run as slapd's user or fix ownership.
- Input must be completely valid: slapadd may not provide naming or schema checks. Indexes are built during the load.
- Use offline loads for many thousands of entries; use ldapadd for new entries in an existing directory.

Verify: `slapcat -b "dc=example,dc=com"` after loading and count the entries.

## Checked
2026-11-08: confirmed against the slapadd(8) man page (all options, ownership, indexing, limitations) and the Admin Guide Database Creation and Maintenance Tools chapter (offline method for many thousands of entries, fewer consistency checks). Removed the unconfirmed superior-first ordering requirement.
Method: documentation only; no commands were run.
