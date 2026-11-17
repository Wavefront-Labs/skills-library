---
id: computing-software.systems-network-administration.active-directory.user-offboarding-runbook
name: user-offboarding-runbook
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, user-offboarding, account-deprovisioning, leaver, disable-adaccount, revoke-sessions, entra-id, mailbox-handover, group-removal]
level: practitioner
status: docs-checked
description: "Leaver runbook for hybrid AD: disable, reset password, revoke Entra sessions, record and strip groups, move to a disabled OU, mailbox/OneDrive handover, delete later."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/disable-adaccount
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-scheduler
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User offboarding (leaver) runbook

**Goal:** access stops at the agreed moment, nothing the business needs is lost, and the
action is auditable and reversible for a period.

## At the leave time (urgent leavers: immediately)
```powershell
$u = Get-ADUser jsmith -Properties MemberOf,Manager,Description
# 1. Record state for reversal and audit
$u | Select SamAccountName,DistinguishedName,MemberOf,Manager | Export-Clixml ".\leaver-$($u.SamAccountName).xml"
# 2. Disable, then reset the password twice (Microsoft's guidance for leavers; mitigates pass-the-hash)
Disable-ADAccount $u
1..2 | ForEach-Object {
  Set-ADAccountPassword $u -Reset -NewPassword (ConvertTo-SecureString ([guid]::NewGuid().ToString()+'!Aa1') -AsPlainText -Force) }
# 3. Strip groups except Domain Users (keeps primary group)
$u.MemberOf | ForEach-Object { Remove-ADGroupMember $_ -Members $u -Confirm:$false }
# 4. Stamp and move
Set-ADUser $u -Description "Leaver $(Get-Date -f yyyy-MM-dd) CHG1234"
Move-ADObject $u -TargetPath 'OU=Leavers,DC=ad,DC=example,DC=com'
```

## Cloud side (hybrid)
Disabling in AD reaches Entra at the next sync cycle (default every 30 minutes). For urgent leavers:
- Trigger a delta sync (`Start-ADSyncSyncCycle -PolicyType Delta` on the Connect server).
- Revoke refresh tokens: `Revoke-MgUserSignInSession -UserId <user>` (Microsoft Graph PowerShell), and block
  sign-in on the cloud account directly (`Update-MgUser -UserId <user> -AccountEnabled:$false`) if needed.
- Disable the user's registered devices and remove MFA methods per policy; wipe or retire company data on mobile devices.
Microsoft Entra cannot directly revoke a session token issued by an application, so access tokens already issued can
remain usable until they expire.

## Data handover
- Convert the mailbox to shared or grant the manager access; set auto-reply.
- OneDrive: grant the manager access according to your retention settings.
- Home drive/profile share: move to an archive location with manager access.

## Later (30-90 days)
Delete the account after your retention period, having checked what the sync will do in Entra ID before deleting or
moving the object out of sync scope.

## Gotchas
- Kerberos tickets already issued stay valid until they expire (the Kerberos user-ticket lifetime policy recommends 10
  hours); for hostile leavers also log off sessions (`quser`/`logoff` on RDS) and disable VPN certificates.
- Shared/service credentials the person knew must be rotated.
- Do not delete immediately; the AD Recycle Bin restores the object but not data in other systems.

## Verify
- [ ] `Get-ADUser jsmith -Properties Enabled,MemberOf` shows disabled, only Domain Users.
- [ ] Entra sign-in logs show failures after the leave time.

## Checked
2026-10-27. Documentation: Microsoft Learn "Revoke user access in Microsoft Entra ID" (hybrid steps), `Disable-ADAccount`
reference, the Entra Connect Sync scheduler article and the Kerberos user-ticket lifetime policy page. Confirmed: disable the
AD account and reset the password twice (reason: pass-the-hash risk), `Revoke-MgUserSignInSession`, `Update-MgUser
-AccountEnabled:$false`, disabling registered devices, default sync cycle of 30 minutes and `Start-ADSyncSyncCycle -PolicyType
Delta`, application session tokens cannot be revoked directly, Kerberos user ticket lifetime recommendation of 10 hours.
Corrected: the draft reset the password once; Microsoft's guidance is twice. Removed as unconfirmed: the Exchange hide-from-
address-list attribute, the OneDrive 30-day retention default and the 30-day Entra soft-delete statements.
Method: documentation only; no commands were run.
