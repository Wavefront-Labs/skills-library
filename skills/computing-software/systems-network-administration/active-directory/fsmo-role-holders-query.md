---
id: computing-software.systems-network-administration.active-directory.fsmo-role-holders-query
name: fsmo-role-holders-query
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo, fsmo-role-holders-query, netdom, get-adforest, get-addomain]
level: intro
status: docs-checked
description: "Find the five FSMO role holders quickly with netdom query fsmo, Get-ADForest and Get-ADDomain, and spot roles held by a dead or demoted DC."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/manage-fsmo-roles
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adforest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query FSMO role holders

## One-liners
```powershell
Get-ADForest | Select SchemaMaster,DomainNamingMaster
Get-ADDomain | Select PDCEmulator,RIDMaster,InfrastructureMaster
# every domain in the forest
(Get-ADForest).Domains | % { Get-ADDomain $_ | Select DNSRoot,PDCEmulator,RIDMaster,InfrastructureMaster }
# which roles does each DC hold (the method Microsoft's transfer guide uses)
Get-ADDomainController -Filter * | Select Name,OperationMasterRoles
Get-ADDomainController DC01 | Select -Expand OperationMasterRoles
```

## Read the answer carefully
- Forest-wide roles (schema master, domain naming master) show once; domain roles show per domain.
- A holder that no longer resolves or no longer exists means the DC was removed without transferring roles: seize
  the roles (see fsmo-role-seizure) and clean up the DC's metadata.
- Right after a transfer, confirm from at least two DCs (`-Server` on the cmdlets) that they agree.

## Verify
- [ ] All five holders resolve, are online and agree when queried through two DCs.

## Checked

Documentation: Microsoft Learn "Transfer FSMO roles" and "Understand FSMO roles" pages and the Get-ADForest,
Get-ADDomain and Get-ADDomainController cmdlet references, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: the `OperationMasterRoles` loop over `Get-ADDomainController -Filter *`, the SchemaMaster/DomainNamingMaster
properties of Get-ADForest and PDCEmulator/RIDMaster/InfrastructureMaster of Get-ADDomain. Removed unconfirmed
`netdom query fsmo`, `dsquery server -hasfsmo`, `repadmin /showattr`, the application-partition infrastructure role owner
note and the `adprep /rodcprep` claim (the docs only mention an Adprep /Rodcprep error after seizing the infrastructure
master, KB 949257).

Method: documentation only; no commands were run.
