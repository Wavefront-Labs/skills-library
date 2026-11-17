---
id: computing-software.systems-network-administration.active-directory.fsmo-role-transfer
name: fsmo-role-transfer
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, operations-masters, fsmo-transfer, move-addirectoryserveroperationmasterrole, ntdsutil, planned-maintenance, pdc-emulator, schema-master]
level: practitioner
status: docs-checked
description: "Gracefully transfer FSMO roles with Move-ADDirectoryServerOperationMasterRole before maintenance or DC retirement, including required rights and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/manage-fsmo-roles
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserveroperationmasterrole
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer FSMO roles (planned)

**Goal:** move one or more roles while both the old and new holder are online and replicating.
A transfer is clean: the old holder hands over its current state.

## Before
- Your AD domain must be operational and free from replication errors (Microsoft's prerequisite).
- Rights: Schema Admins for the schema master (and Enterprise Admins as well, per the guide), Enterprise Admins for the
  domain naming master, Domain Admins for the PDC emulator, RID master and infrastructure master.

## Transfer
```powershell
Move-ADDirectoryServerOperationMasterRole -Identity DC02 `
  -OperationMasterRole PDCEmulator,RIDMaster,InfrastructureMaster
Move-ADDirectoryServerOperationMasterRole -Identity DC02 -OperationMasterRole SchemaMaster,DomainNamingMaster
```
Run from a computer with the AD DS RSAT installed; the cmdlet prompts for confirmation. To confirm a role moved:
```powershell
Get-ADDomainController -Identity DC02 | Select-Object OperationMasterRoles
```

## After
1. Confirm the new holder from two DCs.
2. If the PDC emulator moved in the forest root domain, the new holder becomes the forest's authoritative time source:
   configure its time source and take the old holder out of that role (see the PDC time skill).
3. Update monitoring that targets the PDC by name.

## Gotchas
- If the current holder has failed, the same cmdlet with `-Force` seizes the role (see fsmo-role-seizure); only do that
  if the old holder is truly gone, otherwise fix connectivity first.

## Verify
- [ ] `Get-ADDomainController -Filter *` run against two DCs agrees on the holders.

## Checked

Documentation: Microsoft Learn "Transfer FSMO roles" (prerequisites and role steps) and the
Move-ADDirectoryServerOperationMasterRole reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: cmdlet and role names, per-role group membership requirements, replication-error-free prerequisite, the
verification command, and that `-Force` seizes. Removed unconfirmed: numeric role values, the ntdsutil transfer syntax,
`repadmin` checks, the `w32tm` commands, event 1458, dcdiag test names and the exact error text.

Method: documentation only; no commands were run.
