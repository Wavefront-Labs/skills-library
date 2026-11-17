---
id: computing-software.systems-network-administration.active-directory.fsmo-role-placement
name: fsmo-role-placement
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, operations-masters, fsmo-placement, infrastructure-master, schema-master, domain-naming-master, pdc-emulator, rid-master, netdom-query-fsmo, global-catalog]
level: practitioner
status: docs-checked
description: "Place the five FSMO roles: which are forest vs domain wide, the infrastructure-master/GC rule, co-locating PDC and RID, and how to find current holders."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/manage-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/planning-operations-master-role-placement
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/managing-rid-issuance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSMO role placement

## The five roles
| Role | Scope | What it does |
|---|---|---|
| Schema master | forest | governs changes to the schema |
| Domain naming master | forest | adds and removes domain and application directory partitions |
| PDC emulator | domain | preferential replication of password changes, handles bad-password retries and account lockouts, preferred point of administration for Group Policy and DFS; the busiest role |
| RID master | domain | allocates RID pools to DCs (default block 500 RIDs); new security principals cannot be created once a DC's pool is exhausted and it cannot get more |
| Infrastructure master | domain | updates cross-domain object references and group-to-user references |

## Find holders
```powershell
Get-ADForest | Select SchemaMaster,DomainNamingMaster
Get-ADDomain | Select PDCEmulator,RIDMaster,InfrastructureMaster
```

## Placement guidelines (from Microsoft's docs)
1. Place the domain-level roles on a high-performance, reliable DC in a location with reliable networking. The PDC
   emulator creates the most overhead of all roles; adjust its workload if necessary.
2. Keep the three domain-level roles together on that DC; in the forest root domain, move them off the first DC to a
   high-performance one, and in other domains the guide says to leave them on the first DC.
3. Leave the forest-level roles on a DC in the forest root domain.
4. Configure another DC as the standby for the forest-level roles and another for the domain-level roles.
5. **Infrastructure master:** if all DCs in the domain are global catalogs, placement is insignificant (as it is in a
   single-domain forest). Otherwise the role must not sit on a global catalog server: there it stops updating
   cross-domain references. With the AD Recycle Bin feature enabled every DC updates its own cross-domain references.
6. Operations masters must be where network reliability is high and consistently available.

## Gotchas
- The PDC emulator of the forest root domain is the authoritative Windows Time source for the forest; moving the role
  moves that duty, so reconfigure time sync on the new holder (see the PDC time skill).

## Verify
- [ ] Holders are documented and queried from two DCs with matching answers.
- [ ] A standby DC is designated for the forest-level and for the domain-level roles.

## Checked

Documentation: Microsoft Learn "Understand FSMO roles" and "Planning operations master role placement", from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: role descriptions, placement guidelines (standby DCs, high-performance DC for domain roles, forest roles on the
forest root domain, infrastructure master and global catalog rule, Recycle Bin effect), PDC emulator of the forest root as
authoritative time source, RID block size default 500 (Managing RID Issuance). Removed unconfirmed claims: DFS-N modes,
"felt within hours", placement near users, the dcdiag test names and the initial-sync-after-offline gotcha.

Method: documentation only; no commands were run.
