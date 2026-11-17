---
id: computing-software.systems-network-administration.active-directory.cloud-sync-accidental-deletion-prevention
name: cloud-sync-accidental-deletion-prevention
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, accidental-deletes-prevention, entra-connect, sync-errors]
level: practitioner
status: docs-checked
description: "Configure accidental deletion thresholds in Cloud Sync and Connect Sync, and handle a triggered threshold without blindly allowing the deletes."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-accidental-deletes
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-prevent-accidental-deletes
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-troubleshoot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accidental deletion prevention

An OU moved out of scope or a filter typo can delete thousands of cloud accounts (and their mailboxes and Teams
memberships) in one cycle. Both sync engines can stop that.

## Cloud Sync
Select the configuration > **Properties** > pencil next to **Basics**: set **Notification email**, tick **Prevent
accidental deletions** and enter the **Accidental deletion threshold** (number of objects). The Microsoft page does not
state a default threshold, so size it to your normal churn. For group provisioning to Entra ID the threshold only
protects the group objects, not their members; configure it on synced users too.

When the threshold is exceeded the configuration shows **Delete threshold exceeded** and the job is put in
quarantine with a notification email. From the status, **View provisioning log** lists the `StagedDelete` entries.
- Expected (real cleanup)? Right-click the status > **Allow deletes**, which deletes the objects that triggered the
  threshold.
- Not expected? Fix the cause (for example re-add the OU that left scope), then run **Restart sync** on the
  configuration. Do not allow.

If Connect Sync and Cloud Sync both export to the tenant, an export error about the deletion threshold comes from the
Entra directory setting that Connect manages, not from the Cloud Sync feature. See the Connect section below, or use
`Disable-AADCloudSyncToolsDirSyncAccidentalDeletionPrevention -tenantId <TENANT_ID>` from the AADCloudSyncTools
module once the deletes are confirmed as expected.

## Connect Sync
The feature is on by default with a threshold of 500 deletes. The cmdlets take the sync administrator's UPN:
```powershell
Get-ADSyncExportDeletionThreshold -AADUserName "<UserPrincipalName>"
Enable-ADSyncExportDeletionThreshold -DeletionThreshold 500 -AADUserName "<UserPrincipalName>"
```
When triggered, the Export step in Synchronization Service Manager shows `stopped-deletion-threshold-exceeded`.
To see what is pending: Synchronization Service > Connectors > the Windows Azure Active Directory connector > **Search
Connector Space** > Scope **Pending Export** with **Delete** ticked.
- Unexpected deletes usually mean an OU or filtering change; fix the scope and run a full cycle
  (`Start-ADSyncSyncCycle -PolicyType Initial`).
- All deletes expected (Global Administrator or Hybrid Identity Administrator needed):
  `Disable-ADSyncExportDeletionThreshold -AADUserName "<UserPrincipalName>"`, run **Export** on the Entra connector,
  then re-enable with `Enable-ADSyncExportDeletionThreshold` straight away. Deletions may be permanent.
- If big deletions are routine, raise the threshold instead of disabling the feature.

## Verify
- [ ] Threshold enabled on every sync engine, sized to normal daily churn.
- [ ] Runbook names who may approve allowing deletes.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Cloud Sync accidental deletes (page dated 2025-04-09) and Connect
Sync prevent accidental deletes, plus the Cloud Sync troubleshooting page (2026-08-21). Confirmed the Cloud Sync
properties, Allow deletes and Restart sync flow, the Connect default of 500, the `-AADUserName` cmdlet form,
the run-profile status and Search Connector Space procedure. Removed the `csexport` deletes command, the
30-day recovery claim and an unsourced Cloud Sync default threshold.
Method: documentation only; no commands were run.
