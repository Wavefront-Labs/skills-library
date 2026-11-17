---
id: computing-software.systems-network-administration.openldap.overlay-accesslog
name: overlay-accesslog
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, accesslog, logdb, logpurge, logops, overlay]
level: advanced
status: docs-checked
description: "Record LDAP operations in an OpenLDAP log database with the accesslog overlay: logdb, logops, logbase, logold, logoldattr, logpurge, logsuccess and the log DB setup."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-accesslog&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# accesslog overlay
Main database:
```
overlay accesslog
logdb cn=log
logops writes reads
logold (objectclass=person)
logpurge 2+00:00 1+00:00
```
Log database (must support ordered results, e.g. mdb):
```
database mdb
suffix cn=log
directory /path/to/openldap-log
index reqStart eq
access to * by dn.base="cn=admin,dc=example,dc=com" read
```
Directives:
- `logdb <suffix>`: where records go; entries are children of the suffix, created automatically.
- `logops`: abandon, add, bind, compare, delete, extended, modify, modrdn, search, unbind; aliases `writes`, `reads`, `session`, `all`.
- `logbase <ops> <baseDN>`: log those ops only under a subtree (`|` between ops).
- `logold <filter>`: log old contents of matching deleted/modified entries; `logoldattr <attrs>` adds specific old attributes (only with a matching logold).
- `logpurge <age> <interval>`: format `[ddd+]hh:mm[:ss]`; the example scans daily and deletes entries older than 2 days.
- `logsuccess TRUE|FALSE` (default FALSE): TRUE logs only successful (result 0) requests.

Gotchas: restrict ACLs on the log DB; unless global, only simple binds using DNs in the current database are logged; the audit schema may change and loads automatically.

## Checked

2026-11-04. Confirmed against slapo-accesslog(5): logdb requirements (ordered results, restrictive ACLs, suffix entry auto-created, children of suffix), logops types and aliases, logbase with | delimiter, logold, logoldattr, logpurge format and example, reqStart eq index advice, logsuccess default FALSE, audit schema loaded automatically and subject to change, simple bind logging limit unless global overlay, and the example. Replaced the example directory with a placeholder path and removed the replication remark, which that page does not state.

Method: documentation only; no commands were run.
