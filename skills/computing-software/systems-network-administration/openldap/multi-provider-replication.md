---
id: computing-software.systems-network-administration.openldap.multi-provider-replication
name: multi-provider-replication
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, multi-provider, olcmultiprovider, serverid, olcserverid, replication, entrycsn]
level: sme
status: docs-checked
description: "Configure OpenLDAP N-way multi-provider replication: unique serverID, syncprov, olcSyncRepl, olcMultiProvider TRUE, URL matching, NTP, and slapadd -S for SIDs."
sources:
  - https://www.openldap.org/doc/admin26/replication.html
  - https://www.openldap.org/software/man.cgi?query=slapadd&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# multi-provider replication
Any provider accepts writes and propagates them to the others. Good for high availability; not for load balancing, and network partitions can break consistency and make reconciliation hard.

Per server:
1. A unique server ID: slapd.conf `serverID 1`, or cn=config `olcServerID: 1 ldap://host1:389`. It is part of entryCSN/contextCSN. SID 000 is invalid for multi-provider.
2. Load syncprov and add the overlay to each database (`olcOverlay: syncprov`, classes `olcOverlayConfig`, `olcSyncProvConfig`).
3. A syncrepl stanza per peer, and `olcMultiProvider: TRUE`:
```
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcSyncRepl
olcSyncRepl: rid=004 provider=ldap://host2 binddn="cn=sync,dc=example,dc=com"
  bindmethod=simple credentials=secret searchbase="dc=example,dc=com"
  type=refreshAndPersist retry="5 5 300 5" timeout=1
-
add: olcMultiProvider
olcMultiProvider: TRUE
```
4. Synchronise clocks (NTP).

Gotchas:
- URLs in `olcSyncRepl` must exactly match the URLs slapd listens on, or a server may replicate from itself.
- Loading LDIF without CSNs: use `slapadd -S <SID>` to assign a valid SID.
- Use `slapadd -w` only to seed a fresh provider.
- Prefer one writer at a time (see MirrorMode) if you cannot tolerate conflicts.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide replication chapter (N-way multi-provider arguments for and against, olcServerID with URL, syncprov overlay classes, olcSyncRepl and olcMultiProvider example values, NTP note, URL-match note, SID 000 note) and slapadd(8) (-S SID, -w for a fresh seed provider).

Method: documentation only; no commands were run.

