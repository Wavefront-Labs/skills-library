---
id: computing-software.systems-network-administration.openldap.mdb-backend-setup
name: mdb-backend-setup
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, mdb, maxsize, olcdbmaxsize, directory, maxreaders, lmdb]
level: practitioner
status: docs-checked
description: "Configure an OpenLDAP MDB database: directory, maxsize (default 10 MiB), maxreaders, maxentrysize, mode, rtxnsize, searchstack, multival and the idlexp backend setting."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapd-mdb&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/slapdconfig.html
  - https://www.openldap.org/doc/admin26/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MDB backend setup
```
database  mdb
directory /usr/local/var/openldap-data
suffix    "dc=example,dc=com"
rootdn    "cn=mdb,dc=example,dc=com"
rootpw    mdb
maxsize   1073741824
```
cn=config names: `olcDbDirectory`, `olcDbMaxSize`, and so on. The object classes are `olcDatabaseConfig` plus `olcMdbConfig`.

Directive defaults:
- `directory`: `/usr/local/var/openldap-data`; each database needs its own directory.
- `maxsize`: 10485760 (10 MiB). The memory map is allocated at startup, so the database cannot grow beyond it; raise it later if needed. Set it as large as anticipated growth requires, since growing it later may not be practical under heavy load.
- `maxreaders`: 126 (slapcat counts as one reader).
- `maxentrysize`: 0 (unlimited); larger entries get LDAP_ADMINLIMIT_EXCEEDED.
- `mode`: 0600 for new files.
- `rtxnsize`: 10000 entries per read transaction in large searches.
- `searchstack`: 16, each level of an individual per-thread stack uses 512 KB on 32-bit and 1024 KB on 64-bit.
- `multival <attrs> <hi>,<lo>`: move big value sets to a separate table.
- Backend-level `idlexp` (16 to 30, default 16).

Gotcha: layout is hierarchical, which gives constant-time subtree renames.

## Checked

2026-11-04. Confirmed against slapd-mdb(5), the Administrator's Guide slapd.conf and slapd.d chapters, and the backends chapter: directory default, maxsize 10485760 with the memory map allocated at startup, maxreaders 126, maxentrysize 0 and LDAP_ADMINLIMIT_EXCEEDED, mode 0600, rtxnsize 10000, searchstack 16, multival hi/lo, idlexp 16-30, olcDbDirectory, olcDbMaxSize and the olcDatabaseConfig plus olcMdbConfig object classes, hierarchical layout with constant-time subtree renames. Removed the unconfirmed writable-directory remark and the namingContexts verify command, and corrected the searchstack memory figure.

Method: documentation only; no commands were run.
