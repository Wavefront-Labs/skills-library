---
id: computing-software.systems-network-administration.samba.idmap-tdb-nss
name: idmap-tdb-nss
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-tdb-nss, idmap-tdb, idmap-nss, idmap, use-upn]
level: practitioner
status: docs-checked
description: "Configure the idmap tdb default backend and the nss backend, including range, use_upn default, and pairing nss for local accounts with tdb for the rest."
sources:
  - https://www.samba.org/samba/docs/current/man-html/idmap_tdb.8.html
  - https://www.samba.org/samba/docs/current/man-html/idmap_nss.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap tdb and nss
tdb: the default winbindd backend for SID/uid/gid mapping tables, and the usual writable backend for the default domain `*`. Its only option is `range = low - high` (the page's example says the range is used for uid and gid allocation).
```
[global]
idmap config * : backend = tdb
idmap config * : range = 1000000-2000000
```
(`backend = tdb` is redundant as it is the default.) It is an allocating backend: it allocates new user and group IDs to create new mappings.

nss: maps Unix users and groups to Windows accounts using IDs from NSS.
- `range = low - high`: IDs returned by NSS modules outside it are ignored.
- `use_upn`: default `no`; yes parses NSS names so that namespace becomes authoritative instead of the IDMAP domain name.

Example for a local-account domain `SAMBA` with tdb for everything else:
```
idmap config * : backend = tdb
idmap config * : range = 1000000-1999999
idmap config SAMBA : backend = nss
idmap config SAMBA : range = 1000-999999
```

## Checked
2026-11-04: tdb and nss options, the use_upn default and both examples compared with the idmap_tdb and idmap_nss man pages. Removed: an unstated claim that no range default exists, first-come/local-database wording and a generic disjoint-ranges line.
Method: documentation only; no commands were run.
