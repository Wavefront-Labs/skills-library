---
id: computing-software.systems-network-administration.openldap.slapindex-rebuild
name: slapindex-rebuild
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slapindex, reindex, rebuild-indexes, mdb, indexing]
level: practitioner
status: docs-checked
description: "Rebuild OpenLDAP indexes offline with slapindex after changing index directives: whole database or chosen attributes, -q, -t truncate for mdb, -b and -n selection."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapindex&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/dbtools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapindex rebuild
```
slapindex -F /usr/local/etc/openldap/slapd.d -b "dc=example,dc=com"
slapindex -F /usr/local/etc/openldap/slapd.d uid
slapindex -q -t -n 1
```
Options:
- `-b suffix` or `-n dbnum` select the database (not together; `-n 0` is the config database); default is the first database that supports the operation.
- `[attr ...]` regenerates only those attributes' indexes; with none, all indexes are rebuilt from the data.
- `-q` quick mode, fewer integrity checks; an interruption most likely leaves the database unusable.
- `-t` truncate: empty the index database first (back-mdb only).
- `-c` continue (ignore errors) mode; `-g` skip subordinate databases (they are reindexed by default).

Rules:
- Stop slapd, or at least do not run it read-write.
- Files created belong to the user running slapindex; use slapd's user or fix ownership.
- When to run: after modifying index lines in slapd.conf.

Verify: start slapd and run the indexed search, then check the log for `index_param failed (18)` warnings.

## Checked
2026-11-08: confirmed against the slapindex(8) man page (options, ownership, limitations) and the Admin Guide Database Creation and Maintenance Tools chapter (slapindex use after modifying slapd.conf, attribute list). Removed the idlexp and cn=config background-rebuild claims (not on the cited pages) and the "hides errors" wording.
Method: documentation only; no commands were run.
