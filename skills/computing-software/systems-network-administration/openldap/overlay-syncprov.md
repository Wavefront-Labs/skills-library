---
id: computing-software.systems-network-administration.openldap.overlay-syncprov
name: overlay-syncprov
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, syncprov, sessionlog, contextcsn, overlay, replication-provider]
level: practitioner
status: docs-checked
description: "Make an OpenLDAP database a replication provider with the syncprov overlay: checkpoint, sessionlog, sessionlog-source, nopresent, reloadhint and needed indexes."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-syncprov&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/replication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# syncprov overlay
```
overlay syncprov
syncprov-checkpoint 100 10
syncprov-sessionlog 100
```
cn=config form: entry `olcOverlay=syncprov,olcDatabase={1}mdb,cn=config` with objectClasses `olcOverlayConfig` and `olcSyncProvConfig`.

Directives:
- `syncprov-checkpoint <ops> <minutes>`: write contextCSN to the database after that many writes or minutes (disabled by default). contextCSN is held in memory and written at shutdown, so checkpoints shorten recovery after a crash.
- `syncprov-sessionlog <ops>`: in-memory log of the last writes, excluding Adds; lost on restart.
- `syncprov-sessionlog-source <suffix>`: use an accesslog database as the session log (persistent). Do not combine with `syncprov-sessionlog`.
- `syncprov-nopresent TRUE|FALSE` (default FALSE): TRUE only on an accesslog database.
- `syncprov-reloadhint TRUE|FALSE` (default FALSE): must be TRUE for delta-syncrepl with accesslog.

Indexes: `index entryUUID eq` (recommended with sessionlog) and `index entryCSN eq` where inequality indexing exists.

Gotchas: needs a backend that provides entryCSN and entryUUID; the accesslog database must never be replicated.

## Checked

2026-11-09. Confirmed against slapo-syncprov(5) (checkpoint, sessionlog excluding Adds, sessionlog-source, nopresent, reloadhint and their defaults, contextCSN in memory, entryCSN index advice, entryCSN and entryUUID requirement) and the Admin Guide replication chapter (checkpoint behaviour, entryUUID eq index, accesslog never replicated, olcOverlayConfig and olcSyncProvConfig entry). Softened "needed" to "recommended" for the entryUUID index.

Method: documentation only; no commands were run.

