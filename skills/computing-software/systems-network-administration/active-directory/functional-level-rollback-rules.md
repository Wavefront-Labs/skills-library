---
id: computing-software.systems-network-administration.active-directory.functional-level-rollback-rules
name: functional-level-rollback-rules
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, functional-level, functional-level-rollback, ad-recycle-bin, set-adforestmode]
level: advanced
status: docs-checked
description: "Know when a raised domain or forest functional level can be lowered, which features (Recycle Bin, PAM, 2025 level) block rollback, and how to plan for it."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/lower-domain-forest-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/32k-pages-optional-feature
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adforestmode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functional level rollback rules

Microsoft's current documentation says raising a functional level is no longer permanent: you can lower a domain or
forest to a supported earlier level, within limits.

## What can be lowered
- Lowest level you can roll back to: **Windows Server 2008** if the forest or domain contains Windows Server 2022 or
  earlier DCs; **Windows Server 2016** if it contains Windows Server 2025 DCs.
- Forest: no forest-level feature exclusive to the current level may be in use; you need access to the schema master.
- Domain: no domain-level feature exclusive to the current level may be in use; the target cannot be lower than the
  current forest level; you need connectivity to the PDC emulator.
- Permissions: Domain Admins (domain) or Enterprise Admins (forest), with RSAT and the AD module.

## Features that are one-way
| Feature | Effect |
|---|---|
| AD Recycle Bin | irreversible once enabled; needs forest and domain level 2008 R2 or higher |
| Database 32k pages optional feature | cannot be reverted to 8k page simulation mode; 8k-page backups become unusable except via a full authoritative forest recovery |

## Lower (when allowed)
```powershell
Set-ADForestMode -Identity <forest> -ForestMode Windows2016Forest
Get-ADForest | Select-Object ForestMode
Set-ADDomainMode -Identity <domain> -DomainMode Windows2016Domain
Get-ADDomain | Select-Object DomainMode
```
Values accepted by `-ForestMode` include Windows2008Forest, Windows2008R2Forest, Windows2012Forest, Windows2012R2Forest,
Windows2016Forest and Windows2025Forest. Lower the forest while the domain level is not below the target (a domain cannot
be set lower than the forest level).

## Planning rule
- Enable one-way optional features (Recycle Bin, 32k pages) as separate, planned changes after the level raise.
- Before enabling 32k pages, validate that your backup software handles the 32k page format.

## Verify
- [ ] The change record states which features are enabled and whether the raise can be reversed.
- [ ] `Get-ADForest` and `Get-ADDomain` show the intended modes after the change.

## Checked

Documentation: Microsoft Learn "Lower domain and forest functional levels" (updated 2026-07), "AD DS functional levels"
(2025-10), AD Recycle Bin, "Database 32k pages for Active Directory", and the Set-ADForestMode reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: rollback floors (2008 or 2016), prerequisites and permissions, Recycle Bin irreversibility and 2008 R2
prerequisite, 32k pages irreversibility, forest mode names. Wrong or removed: "you cannot go below 2008 R2 once at
2012+", "PAM feature irreversible", "2025 level moves DCs to 32k pages" (32k pages is a separate optional feature) and the
`Get-ADOptionalFeature` check.

Method: documentation only; no commands were run.
