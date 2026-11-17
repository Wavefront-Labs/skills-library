---
id: computing-software.systems-network-administration.patch-management.stale-computer-object-reconciliation
name: stale-computer-object-reconciliation
category: computing-software
field: systems-network-administration
product: patch-management
tags: [stale-computer-objects, active-directory, agent-coverage, patch-management, inventory-reconciliation]
level: practitioner
status: docs-checked
description: "Reconcile AD and Entra computer objects against patch agent check-ins: find stale accounts, agentless live hosts and duplicates, then disable and delete on a schedule."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/devices/manage-stale-devices
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/search-adaccount
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adcomputer
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-lastlogontimestamp
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.identity.directorymanagement/get-mgdevice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reconciling stale directory objects with agent counts

**Goal:** the denominator in patch compliance is real. The directory lists more computers than the patch tool sees: find out which of the difference are dead and which are live but unmanaged.

## Pull the three lists
```powershell
# AD: enabled computers and last logon
$ad = Get-ADComputer -Filter 'Enabled -eq $true' -Properties lastLogonTimestamp,OperatingSystem |
  Select-Object Name, OperatingSystem, @{n='LastLogon';e={[datetime]::FromFileTime($_.lastLogonTimestamp)}}
# Inactive 90+ days
Search-ADAccount -AccountInactive -ComputersOnly -TimeSpan 90.00:00:00 | Select-Object Name, LastLogonDate
```
- `lastLogonTimestamp` is not real time: it is only updated when the stored value is older than `msDS-LogonTimeSyncInterval` (the schema page describes the initial value as 14 days minus a random percentage of 5 days). `Search-ADAccount -AccountInactive` works only when the domain is at Windows Server 2003 domain functional level or higher.
- Entra: `Get-MgDevice -All -Property DisplayName,ApproximateLastSignInDateTime,TrustType`. Entra evaluates `ApproximateLastSignInDateTime` only when it is more than 14 days (+/-5 day variance) behind, so do not treat a timestamp younger than 21 days as stale. Some active devices have a blank timestamp.
- Patch tool: export the clients with last check-in from whatever management tool you use.

## Join and classify
| Directory recent logon | Agent recent check-in | Meaning | Action |
|---|---|---|---|
| yes | yes | managed | none |
| yes | no | live but unmanaged or broken agent | fix agent, count as non-compliant |
| no | yes | renamed or re-imaged, stale directory duplicate | clean duplicate |
| no | no | dead | disable, then delete |

## Clean-up cadence (example values, set your own)
1. Disable after the inactivity timeframe you define (Microsoft's script example uses 90 days), keep disabled for a grace period, then delete (the example uses 120 days inactive and disabled). Disabling first matters because a deletion cannot be undone.
2. Before deleting an Entra device, back up any BitLocker recovery keys you need: BitLocker keys for Windows 10 or newer devices are stored on the device object and are deleted with it.
3. Retire MDM-controlled devices in the management system before disabling or deleting. Do not delete system-managed devices such as Autopilot (once deleted they cannot be reprovisioned); clean those up in their own admin portals.
4. Hybrid joined Windows 10 or newer devices: disable or delete in on-premises AD and let Microsoft Entra Connect synchronize. Deleting only in Entra re-syncs the device as a new object in Pending state.
5. Roles needed in Entra: Cloud Device Administrator or Intune Administrator. Disable with `Update-MgDevice` (`accountEnabled = $false`), delete with `Remove-MgDevice` (no warning and no recovery).

## Gotchas
- A device owner on long leave can look stale: factor that into the timeframe.
- Deleting an Entra or AD device object does not remove registration on the client; it only blocks use of the device identity.
- Devices that are routinely created and destroyed (for example VDI) should be reconciled separately.

## Verify
The compliance denominator matches the directory-active count, and "live but unmanaged" is a tracked, falling number (set your own tolerance).

## Checked
Date: 2026-11-07. Read in full: Manage stale devices in Microsoft Entra ID (activity timestamp 14 days +/-5 variance, 21-day guidance, disable before delete, BitLocker and Autopilot cautions, hybrid join handling, role list, Update-MgDevice/Remove-MgDevice flow, 90/120-day script examples), lastLogonTimestamp attribute page, Search-ADAccount (read the description and the AccountInactive/TimeSpan/ComputersOnly parameter text), Get-ADComputer and Get-MgDevice (searched for `-Filter`, `-Properties`, `-Property`, `-All`; not read end to end). Removed as unconfirmed: the ConfigMgr `v_CH_ClientSummary`, WSUS `Get-WsusComputer` and SSM export references, "accurate to 14 days" for AD (page gives an initial-update formula only), LAPS storage on the object, cluster name object and appliance exclusions, the 2 percent and 30-day thresholds, and the 4,200/3,600 example figures.
Method: documentation only; no commands were run.
