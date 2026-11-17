---
id: computing-software.systems-network-administration.active-directory.fsmo-role-seizure
name: fsmo-role-seizure
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, operations-masters, fsmo-seize, ntdsutil-seize, dead-dc, disaster-recovery, rid-pool, force]
level: advanced
status: docs-checked
description: "Seize FSMO roles after a DC is permanently lost: when it is safe, -Force/ntdsutil seize, raising the RID pool, and why the old holder must never return."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-seizing-operations-master-role
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-raise-rid-pool
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserveroperationmasterrole
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Seize FSMO roles

**Use only when the current holder is permanently gone** (hardware dead, unrecoverable,
or you have decided it will never boot on the network again). Seizing while the old holder
lives creates two masters.

## Decide
- How urgent is each role? The PDC emulator has the highest day-to-day impact (password changes, lockouts, Group
  Policy administration); the others matter when you next need them.
- Can the old DC come back? If it can, fix it instead of seizing.

## Seize
Pick a healthy, fully replicated DC as the target.
```powershell
Move-ADDirectoryServerOperationMasterRole -Identity DC02 `
  -OperationMasterRole PDCEmulator,RIDMaster,InfrastructureMaster,SchemaMaster,DomainNamingMaster -Force
```
Per the cmdlet reference, run the cmdlet first as a transfer; to seize, run it a second time with the same parameters
plus `-Force`. The ntdsutil equivalent (run on the target DC) is interactive: `ntdsutil`, `roles`, `connections`,
`connect to server <FQDN of the target DC>`, `quit`, then one of `Seize naming master` (Enterprise Admins),
`Seize schema master` (Schema Admins), `Seize infrastructure master` (Domain Admins), plus the PDC and RID master
seize commands. After seizing the infrastructure master you may get an error later when you run `Adprep /Rodcprep`
(KB 949257).

## After a RID master seizure
Microsoft's forest recovery guide covers RID pools after a restore: the global RID space is the `rIDAvailablePool`
attribute of `CN=RID Manager$,CN=System,DC=<domain>`, and you raise it by increasing the low part of the value (the
guide's example adds 100,000 to the value). Follow "AD Forest Recovery - Raise the value of available RID pools" and
"Invalidating the RID pool" for the exact procedure; those pages are about recovery scenarios, so confirm they apply to
a plain seize in your case.

## Mandatory clean-up
1. Metadata cleanup of the dead DC (see the demotion skill).
2. **Never reconnect the old holder with its old AD database.** If it is repaired, wipe and reinstall it.
3. Reconfigure the PDC time source on the new PDC (the forest root PDC emulator is the forest's time source).

## Verify
- [ ] `Get-ADDomainController -Filter * | Select Name,OperationMasterRoles` shows the new holder from multiple DCs.
- [ ] `Dcdiag.exe /TEST:RidManager /v` reports the available RID pool for the domain (the Managing RID Issuance page
  uses this command).

## Checked

Documentation: Microsoft Learn "AD Forest Recovery - Seize an operations master role", "Raise the value of available RID
pools", Managing RID Issuance and the Move-ADDirectoryServerOperationMasterRole reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: transfer-then-`-Force` seizure semantics, ntdsutil roles/connections/seize command names with their
credential requirements, Rodcprep note (KB 949257), rIDAvailablePool location and the 100,000 example, `Dcdiag
/TEST:RidManager /v`. Removed unconfirmed `repadmin /showvector` target selection, the "seize within hours" timing and
the `netdom query fsmo` check; replaced the ADSIEdit pseudo-command with a pointer to the Microsoft procedures.

Method: documentation only; no commands were run.
