---
id: computing-software.systems-network-administration.patch-management.windows-pending-reboot-detection
name: windows-pending-reboot-detection
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reboot-management, pending-reboot, pending-reboot-detection, rebootpending, pendingfilerenameoperations, ccm-client-utilities, windows-update, powershell, patch-management]
level: practitioner
status: gated
description: "Detect pending reboots on Windows reliably: CBS RebootPending, WU RebootRequired, PendingFileRenameOperations, ConfigMgr client SDK, and reboot orchestration that respects them."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/develop/reference/core/clients/sdk/determineifrebootpending-method-in-class-ccm_clientutilities
  - https://learn.microsoft.com/en-us/windows/win32/api/wuapi/nf-wuapi-isysteminformation-get_rebootrequired
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/restart-computer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting pending reboots on Windows

**Goal:** know which servers still need a reboot to finish patching (and therefore are
still vulnerable) and reboot them in their window.

## Signals
| Source | Location | Meaning |
|---|---|---|
| Windows Update Agent API | `Microsoft.Update.SystemInfo` object, `RebootRequired` property | Whether a restart is required to complete installation or uninstallation of updates (documented, read-only) |
| Component Based Servicing | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending` (key exists) (gated: unconfirmed, source is paywalled or blocked) | Servicing stack/LCU pending |
| Windows Update | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired` (key exists) (gated: unconfirmed, source is paywalled or blocked) | WU agent installed updates needing reboot |
| Pending file renames | `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager` value `PendingFileRenameOperations` (gated: unconfirmed, source is paywalled or blocked) | Files to replace at boot (also set by many installers, noisy) |
| ConfigMgr client | `Invoke-CimMethod -Namespace root\ccm\ClientSDK -ClassName CCM_ClientUtilities -MethodName DetermineIfRebootPending` | Returns `RebootPending`, `IsHardRebootPending`, `InGracePeriod`, `DisableHideTime`, `RebootDeadline` |

## Check script
```powershell
function Test-PendingReboot {
  $cbs = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
  $wu  = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
  $pfr = $null -ne (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -EA SilentlyContinue)
  [pscustomobject]@{ Computer=$env:COMPUTERNAME; CBS=$cbs; WindowsUpdate=$wu; FileRename=$pfr; Pending=($cbs -or $wu) }
}
Invoke-Command -ComputerName (Get-Content servers.txt) -ScriptBlock ${function:Test-PendingReboot} |
  Where Pending | Sort Computer
```
Prefer the Windows Update Agent `RebootRequired` property or the ConfigMgr client method where available; report file renames separately (many are harmless).

## Orchestrate reboots
- Reboot within the maintenance window, cluster-aware (CAU for failover clusters, drain
  RDS/IIS behind load balancers first).
- `Restart-Computer -ComputerName $s -Wait -For PowerShell -Timeout 1800 -Force` then rerun
  the check and a service health test.
- Track "patched but not rebooted" as **not remediated** in compliance reports.

## Gotchas
- Uptime alone is not a signal; a server rebooted last week may have installed updates
  since.
- Some update sequences need more than one reboot; check again after each one.

## Verify
After the window, the report shows zero servers with CBS/WU pending; `Get-HotFix` or the
build number (`[Environment]::OSVersion` / UBR registry value) shows the new patch level.

## Checked

Checked 2026-10-27 against Microsoft Learn: ISystemInformation RebootRequired (Windows Update Agent API), CCM_ClientUtilities DetermineIfRebootPending and Restart-Computer.
- `ISystemInformation::get_RebootRequired` meaning, and the `DetermineIfRebootPending` output fields: confirmed.
- `Restart-Computer -Wait -For PowerShell -Timeout`: confirmed in the cmdlet documentation.
- The three registry detection signals are widely used but not described on a readable Microsoft page, so they are marked gated and the skill is gated; the unsupported computer-rename row and the "SSU then LCU" claim were removed or softened.
Method: documentation only; no commands were run.
