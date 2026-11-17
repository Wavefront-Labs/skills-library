---
id: computing-software.systems-network-administration.active-directory.application-partitions-and-domain-naming-master
name: application-partitions-and-domain-naming-master
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo, application-partitions, domain-naming-master, ntdsutil, domaindnszones]
level: advanced
status: docs-checked
description: "Manage AD application partitions and the domain naming master: what needs the role, creating or removing partitions with ntdsutil, and DNS partitions."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/planning-operations-master-role-placement
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc730970(v=ws.11)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/active-directory-integrated-dns-zones
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application partitions and the domain naming master

The domain naming master adds and removes domains and other directory partitions (for example DNS application
partitions) to and from the forest. DCs in a site that cannot reach it cannot add or remove directory, DNS or custom
application partitions. Day to day it is idle.

## Built-in application partitions
Active Directory-integrated DNS uses two kinds of application directory partition:
- `DomainDnsZones`: a domain-wide partition for each domain in the forest.
- `ForestDnsZones`: one forest-wide partition.
Which DCs hold replicas follows your DNS design.

## List and inspect
```cmd
ntdsutil "partition management" connections "connect to server DC01" quit "list" quit quit
```
`list` shows the known naming contexts; `list nc replicas <partition DN>` shows the DCs in a partition's replica set.

## Create, add replicas, remove
```cmd
ntdsutil "partition management" connections "connect to server DC01" quit
  create nc DC=AppData,DC=ad,DC=example,DC=com DC01.ad.example.com
  add nc replica DC=AppData,DC=ad,DC=example,DC=com DC02.ad.example.com
  delete nc DC=AppData,DC=ad,DC=example,DC=com
```
`create nc <DN> <server>` creates an application directory partition (the three-argument form is for AD LDS),
`add nc replica <DN> <server>` adds a replica and `delete nc <DN>` removes the partition. Run `list` again to refresh.
Run these as an account permitted to change forest-wide partitions (Enterprise Admins in practice) and keep the domain
naming master online.

## Failure modes
- Domain naming master offline: adding or removing domains and partitions fails; transfer or seize the role (see
  manage-fsmo-roles in Microsoft's docs).
- Removing a replica, or demoting the last replica of a partition, needs a decision on whether the partition is still
  used; delete it only if no application depends on it.

## Verify
- [ ] `repadmin /showrepl` lists the application partition on each intended replica.

## Checked

Date: 2026-10-27. Documentation: Planning operations master role placement (updated 2025), Active Directory-integrated
DNS zones, ntdsutil `partition management` reference (Windows Server 2012 R2 archive page; no current-release page was
readable).
Confirmed: domain naming master role, DomainDnsZones and ForestDnsZones, `connections`/`connect to server`, `list`,
`list nc replicas`, `create nc`, `add nc replica`, `delete nc` syntax.
Removed unconfirmed claims: the crossRef/`msDS-NC-Replica-Locations` query, the Enterprise Admins requirement as a rule,
the `dnscmd /enlistdirectorypartition` cleanup, example error text and the TAPI remark, and `_msdcs` as the forest zone.

Method: documentation only; no commands were run.
