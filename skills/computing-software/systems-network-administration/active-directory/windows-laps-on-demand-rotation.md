---
id: computing-software.systems-network-administration.active-directory.windows-laps-on-demand-rotation
name: windows-laps-on-demand-rotation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, reset-lapspassword, get-lapsadpassword, password-history, post-authentication-actions]
level: practitioner
status: docs-checked
description: "Rotate Windows LAPS passwords on demand with Reset-LapsPassword or expiry, read password history, and use post-authentication actions to rotate after use."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/laps/reset-lapspassword
  - https://learn.microsoft.com/en-us/powershell/module/laps/set-lapsadpasswordexpirationtime
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS on-demand rotation and history

## Read the current and previous passwords
```powershell
Get-LapsADPassword -Identity SRV01 -AsPlainText                 # current
Get-LapsADPassword -Identity SRV01 -AsPlainText -IncludeHistory # also earlier passwords
```
History is kept only for AD-stored passwords when encryption is enabled (`ADEncryptedPasswordHistorySize`, 0 to 12, default
0). It is useful when restoring a VM from a backup that still has an older password. For Entra-backed devices,
`Get-LapsAADPassword -DeviceIds <NAME_OR_ID> -IncludePasswords -IncludeHistory -AsPlainText` returns history from Entra.

## Rotate now
On the managed device (as local admin), for either backup directory:
```powershell
Reset-LapsPassword
```
From anywhere with rights to write the expiry attribute (Active Directory backup):
```powershell
Set-LapsADPasswordExpirationTime -Identity SRV01 -WhenEffective (Get-Date)
```
The new expiration time is not honoured until the target device next runs a LAPS policy processing cycle. To trigger one
on the device, run `Invoke-LapsPolicyProcessing`. In Intune the device action **Rotate local admin password** does the same
for Entra and AD-backed devices (it fails if the device has not yet backed up its password).

## Rotate automatically after use
Policy **PostAuthenticationActions** with **PostAuthenticationResetDelay** (hours, 0 to 24, default 24; 0 disables):
- 1 = reset password; 3 = reset and sign out (the default); 5 = reset and reboot; 11 = reset, sign out and terminate
  remaining processes (Windows 11 24H2 and Windows Server 2025 only).
After someone signs in with the managed account, the password is reset once the delay passes. Not supported for the DSRM
account.

## Troubleshoot rotation
- Event log: Applications and Services Logs > Microsoft > Windows > LAPS > Operational. 10018 = password updated in AD,
  10029 = in Entra, 10020 = managed account updated, 10043 = a post-authentication rotation failed (LAPS retries until it
  succeeds), 10005 = a processing cycle failed.
- The computer must be able to update its own password attributes: `Set-LapsADComputerSelfPermission -Identity <OU>` grants that on
  an OU.

## Verify
- [ ] `Get-LapsADPassword` shows a new `PasswordUpdateTime` after the reset.

## Checked
Checked 2026-10-27 against Microsoft Learn (windowsserverdocs LAPS policy settings dated 2025-06-26, event log, management
PowerShell and concepts pages; windows-powershell-docs LAPS module for Windows Server 2025; Intune Windows LAPS policy page).
Confirmed cmdlet names and parameters, the expiry-honoured-at-next-cycle behaviour, history range, post-authentication
values and defaults, and event IDs. Corrected the default rotation action (3, not 1), removed the unsourced "hourly"
processing interval, and the placement of 10018 as the only success signal.
Method: documentation only; no commands were run.
