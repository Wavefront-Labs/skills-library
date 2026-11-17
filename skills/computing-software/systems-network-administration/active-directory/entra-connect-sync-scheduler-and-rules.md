---
id: computing-software.systems-network-administration.active-directory.entra-connect-sync-scheduler-and-rules
name: entra-connect-sync-scheduler-and-rules
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, entra-connect-sync, start-adsyncsynccycle, get-adsyncscheduler, sync-rules-editor, attribute-filtering, scoping-filter, precedence, adsync, full-sync]
level: advanced
status: docs-checked
description: "Operate Entra Connect Sync: scheduler, delta vs initial cycles, custom sync rules (scoping, transformations, precedence) without editing defaults, and previewing changes."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-scheduler
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-change-the-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect Sync: scheduler and sync rules

## Scheduler
```powershell
Import-Module ADSync
Get-ADSyncScheduler                          # interval, next run, StagingModeEnabled, NextSyncCyclePolicyType
Start-ADSyncSyncCycle -PolicyType Delta
Start-ADSyncSyncCycle -PolicyType Initial    # full import and sync; reprocesses new or changed rules
Set-ADSyncScheduler -SyncCycleEnabled $false # pause before maintenance; re-enable afterwards
```
The default cycle is every 30 minutes (`CustomizedSyncCycleInterval` changes it). A delta sync must run at least every 7
days, and a delta after a full sync within 7 days of the full sync completing. Scheduler settings are stored in Entra, so a
change on the primary also affects the staging server (except staging mode). Do not set `IsStagingModeEnabled` or
`SchedulerSuspended` by PowerShell. Runs show in **Synchronization Service Manager** > Operations.

## Change behaviour with custom rules (Synchronization Rules Editor)
Microsoft's guidance is to add rules rather than modify the out-of-box ones (modified standard rules are discouraged and
placed unreliably after a settings import). Steps:
1. Disable the scheduler.
2. Create a new rule with **Join** link type and a precedence number unique in the system; **lower value = higher
   precedence**. Out-of-box rules start at 100, and 0 to 99 is reserved for custom rules.
3. Examples from Microsoft:
   - *Filter objects:* inbound rule from AD with a scoping filter such as `extensionAttribute15 EQUAL NoSync` and a
     Constant transformation setting `cloudFiltered` to `True`.
   - *Attribute transformation:* an inbound Expression flow, for example
     `IIF(IsNullOrEmpty([description]),NULL,Left(Trim(Item([description],1)),448))`.
4. Preview one object: Synchronization Service Manager > Connectors > the AD connector > **Search Connector Space**, select
   the object > **Preview**, then **Commit Preview**; **Metaverse Search** shows the resulting metaverse attributes.
5. Run an Initial cycle (full sync) and check pending exports before they go out. Re-enable the scheduler.
If you run out of the 1-99 range, the documented method moves a rule ahead of an out-of-box rule with `PrecedenceBefore`.

## OU and attribute filtering
Change domain and OU scope in the wizard (Customize synchronization options > Domain and OU filtering). Attribute
filtering uses **Microsoft Entra app and attribute filtering** and **Directory extension attribute sync**.

## Gotchas
- A filtering change that removes many objects is stopped by accidental delete prevention (default threshold 500).
  Investigate first. If intended, run `Disable-ADSyncExportDeletionThreshold -AADUserName "<UPN>"`, export, then
  re-enable with `Enable-ADSyncExportDeletionThreshold`.
- Domain/OU filter and sync rule changes need an Initial (full) cycle to take effect.
- Prefer testing on the staging server.

## Verify
- [ ] Preview shows the expected attribute value for test objects.
- [ ] After the full sync, export counts match expectations with no unexpected deletes.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect scheduler, change-the-configuration, filtering, import
and export and accidental deletes pages. Confirmed cmdlets, the 30-minute default, the 7-day rule, precedence ranges
(custom 0 to 99, out-of-box from 100), the `cloudFiltered` filter pattern and the preview steps. Fixed the example value
`NOSYNC` to the documented `NoSync`, and added the `-AADUserName` form of the deletion-threshold cmdlets.
Method: documentation only; no commands were run.
