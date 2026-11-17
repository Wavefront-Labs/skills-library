---
id: computing-software.systems-network-administration.patch-management.wsus-synchronisation-and-approvals
name: wsus-synchronisation-and-approvals
category: computing-software
field: systems-network-administration
product: patch-management
tags: [wsus, wsus-sync, wsus-approval, approve-wsusupdate, computer-groups, auto-approval-rules, windows-update-management, wsus-downstream]
level: practitioner
status: gated
description: "Run WSUS synchronisation and approvals: products and classifications, sync schedules, ring-based approvals with PowerShell, auto-approval rules and downstream replicas."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/manage/setting-up-update-synchronizations
  - https://learn.microsoft.com/en-us/powershell/module/updateservices/approve-wsusupdate
  - https://learn.microsoft.com/en-us/powershell/module/updateservices/get-wsusupdate
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/manage/updates-operations
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WSUS synchronisation and approvals

## Sync scope
Select only products you run and classifications you deploy (for example Security Updates, Critical Updates, Update Rollups, Definition Updates). Avoid "Drivers" and unused languages: they bloat SUSDB and content.
The subscription property names in this script (gated: unconfirmed, source is paywalled or blocked).
```powershell
$wsus = Get-WsusServer
Get-WsusClassification | Where-Object { $_.Classification.Title -in 'Security Updates','Critical Updates','Definition Updates','Update Rollups' } | Set-WsusClassification
$sub = $wsus.GetSubscription(); $sub.SynchronizeAutomatically = $true
$sub.SynchronizeAutomaticallyTimeOfDay = (New-TimeSpan -Hours 3); $sub.NumberOfSynchronizationsPerDay = 1; $sub.Save()
$sub.StartSynchronization(); $sub.GetSynchronizationProgress()
```

## Ring-based approvals
Computer groups: `Pilot`, `Broad`, `Tier0`. Approve after Patch Tuesday:
```powershell
Get-WsusUpdate -Classification Security -Approval Unapproved -Status FailedOrNeeded |
  Approve-WsusUpdate -Action Install -TargetGroupName 'Pilot'
# after pilot validation (e.g. +5 days)
Get-WsusUpdate -Approval Approved -Status FailedOrNeeded | Approve-WsusUpdate -Action Install -TargetGroupName 'Broad'
```
Set deadlines via the console (or `$update.Approve('Install', $group, $deadline)` in the API) where forced installs are needed.

## Auto-approval rules
Auto-approval rules are optional (the Options page of the WSUS console); avoid auto-approving security updates to production unless rings and a test window exist upstream.

## Downstream servers
A downstream server in replica mode inherits approvals and you cannot approve updates on it; an autonomous downstream approves independently. Sync downstreams after the upstream finishes. Depth limits for server chains (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Clients must be in groups via GPO targeting (client-side targeting) or console assignment; new clients start in Unassigned Computers until moved. Approvals for the All Computers group apply to every group.
- Superseded updates left approved slow scans; decline them in the cleanup routine.

## Verify
`$wsus.GetSubscription().GetLastSynchronizationInfo()` shows Succeeded, and the group compliance report shows pilot machines installed before broad approval.

## Checked

Checked 2026-10-27 against Microsoft Learn: WSUS update synchronisation, update operations (approvals), Approve-WsusUpdate, Get-WsusUpdate and the WSUS configuration page.
- `Approve-WsusUpdate -Update -Action -TargetGroupName` (no deadline parameter), `Get-WsusUpdate -Classification -Approval -Status`: confirmed.
- Synchronisation by product and classification, approval to All Computers and subgroups, deadlines set in the console, replica mode blocking local approval, client-side targeting versus console assignment: confirmed.
- Not confirmed from readable pages: the `Subscription` API property names used in the sync script and the downstream chain-depth limit; both are marked gated, so the skill is gated.
- Removed unconfirmed: the Servicing Stack classification note and the built-in Defender auto-approval rule claim.
Method: documentation only; no commands were run.
