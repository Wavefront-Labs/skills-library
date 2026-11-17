---
id: computing-software.systems-network-administration.openldap.slapcat-backup
name: slapcat-backup
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slapcat, backup, mdb-copy, ldif-export, migration]
level: practitioner
status: docs-checked
description: "Back up OpenLDAP with slapcat and mdb_copy: -n, -b, -l, -H, -g, -c options, config database -n 0, live-export caveats and the migration sequence."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapcat&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/maintenance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapcat backup
```
slapcat -F /usr/local/etc/openldap/slapd.d -n 1 -l data.ldif
slapcat -F /usr/local/etc/openldap/slapd.d -n 0 -l config.ldif
slapcat -b "dc=example,dc=com" -l example.ldif
```
Options: `-b suffix` or `-n dbnum` (mutually exclusive; `-n 0` is the config database); `-l file` (else stdout); `-f`/`-F` config; `-g` skip subordinate databases; `-H 'ldap:///???(filter)'` limit by DN/scope/filter (replaces deprecated `-a`/`-s`); `-c` continue on errors; `-o ldif_wrap={no|n}`.

Example excluding a subtree: `slapcat -H 'ldap:///???(!(entryDN:dnSubtreeMatch:=ou=People,dc=example,dc=com))'`.

Facts:
- It can run while slapd is up (mdb and null are always safe), but a live dump may be inconsistent if applications are mid-transaction.
- `mdb_copy` can copy a live LMDB database; with `writemap` it stores the actual size, not sparse.
- Output order is database order, not superior-first, and dynamically generated attributes are excluded: it is meant for `slapadd`, not `ldapadd`.

Migration: stop slapd, `slapcat`, clear the data directory, perform the software and configuration upgrades, `slapadd`, start. This does not cover complicated deployments such as N-Way Multi-Provider.

## Checked
2026-11-08: confirmed against the slapcat(8) man page (options, ordering, dynamically generated attributes, mdb always safe) and the Admin Guide Maintenance chapter (mdb_copy, writemap, live slapcat inconsistency, migration steps). Removed the unconfirmed delta-syncrepl backup claim.
Method: documentation only; no commands were run.
