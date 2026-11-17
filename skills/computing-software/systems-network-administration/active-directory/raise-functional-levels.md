---
id: computing-software.systems-network-administration.active-directory.raise-functional-levels
name: raise-functional-levels
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, functional-level, set-adforestmode, set-addomainmode, domain-functional-level, forest-functional-level, dc-upgrade, recycle-bin, rollback]
level: practitioner
status: docs-checked
description: "Raise domain and forest functional levels safely: inventory DC OS versions, what each level unlocks, Set-ADDomainMode/Set-ADForestMode, and rollback limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/raise-domain-forest-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adforestmode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raise domain and forest functional levels

**Goal:** unlock newer AD features once every DC runs a new enough OS, without surprises.

## What the levels gate
- Functional levels set which Windows Server versions may run as DCs in the domain or forest; they do not affect
  workstations or member servers. Domain level = oldest DC OS allowed in that domain; the forest level is the same
  across the forest.
- Documented levels: Windows Server 2012 R2 (DC-side Protected Users protections, authentication policies and silos),
  2016 (PAM with MIM, automatic NTLM secret rolling for smart-card-required accounts, PKInit freshness), and 2025 (the
  Database 32k pages optional feature becomes available). Windows Server 2019 and 2022 use the 2016 level; there is no
  2019 or 2022 level. 2016 level domains must use DFSR for SYSVOL.
- DC interoperability: a 2025 DC runs at 2025 or 2016 level; 2022/2019/2016 DCs run at 2016 or 2012 R2 level (not 2025);
  a 2012 R2 DC runs only at the 2012 R2 level (matrix on the functional levels page).

## Steps
1. Prerequisites from Microsoft: every DC in the domain (forest) runs at least the target OS; the forest and domain are
   operational and free from replication errors; identify GC and FSMO DCs and verify backups of them first; forest
   level changes need Enterprise Admins; RSAT with AD DS Tools or the AD PowerShell module.
```powershell
Get-ADDomainController -Filter * | Select Name,Site,OperatingSystem,IsReadOnly | Sort OperatingSystem
Get-ADForest | Select-Object ForestMode
Get-ADForest | Select-Object -ExpandProperty Domains | ForEach-Object { Get-ADDomain $_ } | Select-Object Name, DomainMode
```
2. Raise each domain, then the forest (the Active Directory Domains and Trusts console also works):
```powershell
Set-ADDomainMode -Identity ad.example.com -DomainMode Windows2016Domain
Set-ADForestMode -Identity ad.example.com -ForestMode Windows2016Forest
```
3. If every DC in every domain runs Windows Server 2025, raising the forest level to 2025 automatically raises all
   domain levels, so raising domains separately is unnecessary. To add a 2025 DC to an existing domain, the domain must
   already be at least at the 2016 level.

## Rollback
Microsoft's current documentation allows lowering a level within limits (see functional-level-rollback-rules). Optional
features such as AD Recycle Bin and Database 32k pages cannot be reverted once enabled.

## Gotchas
- A DC with an older OS anywhere (DR site, powered-off VM) blocks the raise; find it first.

## Verify
- [ ] `Get-ADDomain` and `Get-ADForest` show the new mode.
- [ ] Replication is still healthy afterwards.

## Checked

Documentation: Microsoft Learn "Raise domain and forest functional levels", "AD DS functional levels" (updated 2025-10) and the
Set-ADForestMode reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: prerequisites, the 2012 R2 / 2016 / 2025 feature lists, interoperability matrix, 2019/2022 using the 2016 level,
automatic domain raise with a 2025 forest raise, 2025 DC requires a 2016-level domain, cmdlet usage. Removed unconfirmed:
2008 R2 and 2012 level feature claims, "PAM cannot be disabled", the "2025 = newer Kerberos/LDAP behaviours" claim, the
rollback examples, third-party product caps and `repadmin /replsummary`.

Method: documentation only; no commands were run.
