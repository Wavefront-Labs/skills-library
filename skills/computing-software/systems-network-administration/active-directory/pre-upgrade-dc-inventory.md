---
id: computing-software.systems-network-administration.active-directory.pre-upgrade-dc-inventory
name: pre-upgrade-dc-inventory
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, functional-level, dc-inventory, schema-version, dc-upgrade]
level: practitioner
status: docs-checked
description: "Inventory every DC's OS, build, roles, site and SYSVOL replication engine plus forest and domain levels and schema version before planning an AD upgrade."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/upgrade-domain-controllers
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/schema-updates
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dfsrmig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-upgrade DC inventory

You cannot raise levels or add a new OS version DC safely without knowing exactly what is there.

## One script, whole forest
```powershell
$forest = Get-ADForest
"Forest {0} mode {1} schema {2}" -f $forest.Name,$forest.ForestMode,
  (Get-ADObject (Get-ADRootDSE).schemaNamingContext -Properties objectVersion).objectVersion
foreach ($d in $forest.Domains) {
  $dom = Get-ADDomain $d
  "Domain $d mode $($dom.DomainMode)"
  Get-ADDomainController -Filter * -Server $d | Format-List *
}
```
`Format-List *` shows every property the module returns for each DC (OS, site, roles and so on); pipe to
`Export-Csv <PATH>` instead to keep the inventory with the change record.

## Schema version map (objectVersion)
47 = 2008 R2, 56 = 2012, 69 = 2012 R2, 87 = 2016, 88 = 2019, 91 = 2025 (the schema-updates article lists no new
schema file for 2022).

## Also check
- **SYSVOL replication engine**: on the PDC emulator `dfsrmig /getglobalstate` (and `/getmigrationstate` for every DC)
  should show the Eliminated state; FRS is listed as a removed feature that DFS Replication replaces.
- Old OS DCs that set the functional-level floor: Windows Server 2019 or later needs at least a Windows Server 2008
  forest level, and the supported levels today are Windows Server 2012 R2, 2016 and 2025 (2019 and 2022 use 2016).
- Orphaned DC objects (metadata of dead DCs) in Sites and Services: a server object with no NTDS Settings child is a
  leftover; see the demote-dc-and-metadata-cleanup skill.
- Applications bound to specific DC names or IPs (LDAP binds hardcoded in apps, DNS forwarders on appliances).
- Trusts and their partner domains' levels.
- Products that require a minimum or maximum forest level (check their vendor documentation).
- FSMO role holders: `Get-ADDomain | FL InfrastructureMaster, RIDMaster, PDCEmulator` and
  `Get-ADForest | FL DomainNamingMaster, SchemaMaster`.

## Output of the inventory
- Target functional level and which DCs must be demoted first.
- Order: schema update, add new DCs, move roles, demote old, raise levels.

## Verify
- [ ] Every DC listed, reachable, and replication healthy.
- [ ] FRS eliminated, schema version recorded, blockers listed with owners.

## Checked

Date: 2026-10-27. Documentation: Upgrade domain controllers, AD DS functional levels (updated 2025-10), Windows Server
Active Directory schema updates, dfsrmig reference, Features removed or no longer developed in Windows Server
(MicrosoftDocs/windowsserverdocs, main branch).
Confirmed: objectVersion table, supported functional levels and the 2008 floor for 2019+, `dfsrmig` switches and
Eliminated state, the FSMO queries, FRS removal note.
Removed unconfirmed claims: the nTDSDSA search example for orphaned DC objects, the statement that FRS blocks 2019+
DCs as worded, and the explicit `Get-ADDomainController` property list.

Method: documentation only; no commands were run.
