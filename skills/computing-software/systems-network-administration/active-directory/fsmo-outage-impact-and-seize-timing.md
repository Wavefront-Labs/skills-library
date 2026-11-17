---
id: computing-software.systems-network-administration.active-directory.fsmo-outage-impact-and-seize-timing
name: fsmo-outage-impact-and-seize-timing
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, fsmo-outage-impact, fsmo-seize, incident-response]
level: advanced
status: docs-checked
description: "What stops working when each FSMO role holder is down, how long each can be tolerated, and the decision rule for transfer, wait or seize."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/manage-fsmo-roles
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/managing-rid-issuance
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserveroperationmasterrole
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSMO outage impact and when to seize

When a role holder dies, the right move depends on which role it held. Panic seizing is how you end up with two
RID masters.

## Impact table
| Role | Scope | Function lost when down |
|---|---|---|
| PDC emulator | domain | preferential password-change replication and bad-password retry source, account lockout processing, preferred point of administration for Group Policy and DFS, the forest root one is the forest time source |
| RID master | domain | DCs can keep creating objects only until their current RID pool is exhausted (blocks are 500 RIDs by default) |
| Infrastructure master | domain | cross-domain object and group-to-user references are not updated (insignificant if all DCs are GCs or the forest has one domain) |
| Schema master | forest | schema changes |
| Domain naming master | forest | adding and removing domain and application partitions |

## Decision rule
1. Is the holder coming back soon (reboot, network blip, repair)? **Wait.**
2. Is it coming back but you need the role now (planned work)? Bring it up and **transfer**.
3. Is it gone for good (destroyed, being rebuilt, restoring it would mean an old backup)? **Seize** to a healthy,
   fully replicated DC, then do metadata cleanup. The old holder must never come back online.

## Before seizing, pick the target well
Choose a healthy DC that is free from replication errors and has replicated recently with the failed holder, so it
has the latest data (especially for the RID master).

## Seize
```powershell
Move-ADDirectoryServerOperationMasterRole -Identity <target> -OperationMasterRole RIDMaster,PDCEmulator -Force
```

## After
- [ ] Metadata cleanup of the dead DC (see Microsoft's metadata cleanup procedure).
- [ ] For a RID master seize: check the available RID pool with `Dcdiag.exe /TEST:RidManager /v` and follow the
  forest recovery guide's RID pool steps if they apply.
- [ ] Time configuration moved with the PDC role if it was the forest root PDC emulator.

## Checked

Documentation: Microsoft Learn "Understand FSMO roles", Managing RID Issuance, "Transfer FSMO roles" and the
Move-ADDirectoryServerOperationMasterRole reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: role functions, RID block default 500, infrastructure master/GC rule, `-Force` seizure. Removed unconfirmed
outage-tolerance durations, "request at 50%", `repadmin` target-selection commands and ntdsutil/dcdiag specifics.

Method: documentation only; no commands were run.
