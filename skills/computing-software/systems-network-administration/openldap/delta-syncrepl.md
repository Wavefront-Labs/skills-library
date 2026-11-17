---
id: computing-software.systems-network-administration.openldap.delta-syncrepl
name: delta-syncrepl
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, delta-syncrepl, delta-syncrepl-accesslog, logbase, syncdata, accesslog, replication]
level: sme
status: docs-checked
description: "Set up OpenLDAP delta-syncrepl using an accesslog database: provider overlays, logpurge, reloadhint, consumer logbase, logfilter and syncdata=accesslog."
sources:
  - https://www.openldap.org/doc/admin26/replication.html
  - https://www.openldap.org/software/man.cgi?query=slapo-syncprov&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# delta-syncrepl
Replicates only changes read from an accesslog, instead of whole entries.

Provider:
1. Load `accesslog.la` and `syncprov.la`.
2. Create the log database (`database mdb`, `suffix cn=accesslog`) with `index reqStart eq`, and put `overlay syncprov` on it with `syncprov-nopresent TRUE`.
3. On the main database: `overlay accesslog`, `logdb cn=accesslog`, `logops writes`, `logsuccess TRUE`, `logpurge 07+00:00 01+00:00` (scan daily, remove entries older than 7 days), and `overlay syncprov` with `syncprov-reloadhint TRUE`.

Consumer:
```
syncrepl rid=0
        provider=ldap://ldapprovider.example.com:389
        logbase="cn=accesslog"
        logfilter="(&(objectClass=auditWriteObject)(reqResult=0))"
        type=refreshAndPersist
        retry="60 +"
        syncdata=accesslog
```
Constraints:
- Partial (fractional or sparse) replication is incompatible with delta-syncrepl.
- The replicator needs unrestricted read access to both databases.
- The accesslog database is unique to a provider and should never be replicated.
- Back up and restore both databases together with slapcat/slapadd.

## Checked

2026-11-04. Confirmed against the Administrator's Guide replication chapter (18.2.1 and 18.3.2) and slapo-syncprov(5): provider modules, accesslog database with syncprov-nopresent and syncprov-reloadhint TRUE, reqStart eq index, main database accesslog with logdb, logops writes, logsuccess TRUE, logpurge 07+00:00 01+00:00 meaning daily scan and 7-day retention, consumer syncrepl with logbase, logfilter, refreshAndPersist, retry and syncdata=accesslog, incompatibility with partial replication, unrestricted read access for the replicator, backup of both databases with slapcat and slapadd. Removed the contextCSN verify command, which the pages do not give.

Method: documentation only; no commands were run.
