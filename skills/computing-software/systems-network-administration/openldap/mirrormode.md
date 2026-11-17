---
id: computing-software.systems-network-administration.openldap.mirrormode
name: mirrormode
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, mirrormode, mirror-mode, high-availability, failover, multiprovider, replication]
level: advanced
status: docs-checked
description: "Run OpenLDAP MirrorMode: two providers replicating each other while a front end sends writes to one node, with serverID, syncrepl and multiprovider on config."
sources:
  - https://www.openldap.org/doc/admin26/replication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MirrorMode
Two nodes replicate each other (multi-provider), but an external front end (load balancer or slapd in proxy mode) directs all writes to one node. The second takes writes only if the first fails.

Node 1 (slapd.conf):
```
serverID 1
syncrepl rid=001
        provider=ldap://ldap-sid2.example.com
        bindmethod=simple
        binddn="cn=mirrormode,dc=example,dc=com"
        credentials=mirrormode
        searchbase="dc=example,dc=com"
        type=refreshAndPersist
        retry="60 +"
multiprovider on
```
Node 2: same, with `serverID 2` and the provider pointing to node 1. Both need `overlay syncprov` on the database.

Checklist:
- Unique `serverID` per node; syncrepl bind identity with unrestricted read.
- Tightly synchronised clocks (NTP) on both nodes.
- An external front end must direct writes to one node and switch on failure: a hardware load balancer, dedicated proxy software, or a back-ldap proxy. A repaired node catches up by resyncing.

Gotchas: writes must go to only one node at a time, which is why this is not true multi-provider. Backups are managed slightly differently.

Verify: add an entry on node 1 and read it on node 2; compare `contextCSN` values.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide replication chapter (mirror mode description and arguments, mirror mode node 1 and 2 example with serverID, syncrepl and multiprovider, failover options, unrestricted read for the replicator, clock synchronisation note). Added bindmethod=simple to the example as in the guide. Removed the unsourced uri reordering, balancing and SASL/TLS advice.

Method: documentation only; no commands were run.

