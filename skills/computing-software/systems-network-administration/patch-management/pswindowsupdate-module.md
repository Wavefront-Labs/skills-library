---
id: computing-software.systems-network-administration.patch-management.pswindowsupdate-module
name: pswindowsupdate-module
category: computing-software
field: systems-network-administration
product: patch-management
tags: [pswindowsupdate, windows-update-management, patch-deployment, powershell, remote-patching, windows]
level: practitioner
status: gated
description: "Patch Windows servers from PowerShell with PSWindowsUpdate: list, install and hide updates, run remotely via scheduled task, use WSUS or Microsoft Update, and collect history."
sources:
  - https://www.powershellgallery.com/packages/PSWindowsUpdate
  - https://github.com/mgajda83/PSWindowsUpdate
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/restart-computer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSWindowsUpdate module

Community module wrapping the Windows Update Agent API. Handy for small estates, DMZ hosts
without ConfigMgr, or scripted maintenance in an orchestration tool.

## Install
```powershell
Install-Module PSWindowsUpdate -Scope AllUsers
Import-Module PSWindowsUpdate
Get-Command -Module PSWindowsUpdate
```

## Local use
```powershell
Get-WindowsUpdate                                   # available from configured source (WSUS if GPO points to it)
Get-WindowsUpdate -MicrosoftUpdate                  # include Microsoft Update (Office, SQL...)
Install-WindowsUpdate -AcceptAll -Verbose
Install-WindowsUpdate -KBArticleID KB5044281 -AcceptAll -AutoReboot
Hide-WindowsUpdate -KBArticleID KB5099999 -Verbose      # alias of Get-WindowsUpdate -Hide
Get-WUHistory
Add-WUServiceManager -MicrosoftUpdate               # register the Microsoft Update service
```
`-IgnoreReboot`, `Get-WURebootStatus`, `-Category` and `-NotCategory` (gated: unconfirmed, source is paywalled or blocked); check `Get-Help` for the version you install.

## Remote
The module's README documents `-ComputerName` on `Get-WindowsUpdate`, and `-ScheduleJob` to schedule an install at a given time:
```powershell
Install-WindowsUpdate -MicrosoftUpdate -UpdateID <guid> -RevisionNumber <n> -ScheduleJob (Get-Date -Hour 18 -Minute 0 -Second 0) -AcceptAll -AutoReboot -Verbose
```
`-AutoReboot` restarts the server automatically if needed, so use it only inside a maintenance window. The `Invoke-WUJob`, `Get-WUJob` and `Enable-WURemoting` remoting helpers, and the Windows Update Agent restriction that blocks installs over plain remoting (error 0x80070005) (gated: unconfirmed, source is paywalled or blocked).
Read results afterwards and reboot in your window (`Restart-Computer -Wait -For PowerShell`).

## Pattern for a maintenance script
1. Pre-checks (backup done, cluster node drained).
2. Run the scheduled or remote install.
3. Wait for completion; reboot if the host reports a pending restart (see the `windows-pending-reboot-detection` skill).
4. Post-checks (services, build/UBR, app health).

## Gotchas
- It's not Microsoft-supported; pin the module version you tested.
- Security tooling may flag scheduled installs created remotely; agree an allow policy with your security team.
- Approvals/declines on WSUS still apply when the client uses WSUS.

## Verify
`Get-WUHistory` shows Succeeded for the cycle's updates; build/UBR matches the target;
no reboot pending after the window.

## Checked

Checked 2026-10-27 against the PSWindowsUpdate README (module project) and Microsoft Learn (Restart-Computer).
- Cmdlets `Get-WindowsUpdate`/`Install-WindowsUpdate` with `-MicrosoftUpdate`, `-KBArticleID`, `-Hide`, `-AcceptAll`, `-AutoReboot`, `-ScheduleJob`, `-ComputerName`, `Hide-WindowsUpdate`, `Add-WUServiceManager`, `Get-WUHistory`, `Get-WUSettings`/`Set-WUSettings`: confirmed in the README.
- `Restart-Computer -Wait -For PowerShell`: confirmed in the Microsoft cmdlet documentation.
- `Invoke-WUJob`, `Get-WUJob`, `Enable-WURemoting`, `Get-WURebootStatus`, `-IgnoreReboot`, `-Category` and the 0x80070005 remoting restriction are not in the README and are marked gated, so the skill is gated.
- Module is community-maintained, not a Microsoft product; pin the tested version.
Method: documentation only; no commands were run.
