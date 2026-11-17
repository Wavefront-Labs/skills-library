---
id: computing-software.systems-network-administration.windows-server.adfs-extranet-smart-lockout
name: adfs-extranet-smart-lockout
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ad-fs, extranet-smart-lockout, account-lockout, web-application-proxy, password-spray]
level: advanced
status: docs-checked
description: "Protect AD FS from password spray with Extranet Smart Lockout: log-only rollout, thresholds below AD lockout, familiar locations and resetting lockouts."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/configure-ad-fs-extranet-smart-lockout-protection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS Extranet Smart Lockout

Extranet sign-ins via WAP can lock AD accounts (denial of service) or be sprayed. ESL (2016+, 2019 best) locks the
**extranet** attempts from unfamiliar locations while users at familiar IPs keep working.

## Rollout
```powershell
# 1. Log-only first: learns familiar locations without blocking
Set-AdfsProperties -EnableExtranetLockout $true -ExtranetLockoutThreshold 15 -ExtranetObservationWindow (New-TimeSpan -Minutes 30) -ExtranetLockoutMode AdfsSmartLockoutLogOnly
Restart-Service adfssrv     # on all farm nodes
# 2. After a couple of weeks, enforce
Set-AdfsProperties -ExtranetLockoutMode AdfsSmartLockoutEnforce
```
- Set the AD FS threshold below the AD **Account Lockout Threshold** (the docs suggest half, for example 10 against 20).
- Familiar locations: IPs from which the user signed in successfully; up to 20 per user, oldest dropped first.
- Requires the 2016 farm behavior level (with the June 2018 updates) or AD FS 2019+, and the `AdfsArtifactStore.AccountActivity`
  table: grant the service account the right to create it with `Update-AdfsArtifactDatabasePermission -Credential $cred`.
- AD FS 2019 adds separate thresholds for familiar and unfamiliar locations, and `Set-AdfsProperties -ExtranetLockoutMode 3`
  to run smart lockout in log-only mode while keeping the 2012 R2 soft lockout enforced.

## Help desk
```powershell
Get-AdfsAccountActivity jdoe@example.com      # familiar/unfamiliar bad password counts and IPs
Reset-AdfsAccountLockout jdoe@example.com -Location Unknown     # or -Location Familiar
Set-AdfsAccountActivity jdoe@example.com -AdditionalFamiliarIps '203.0.113.20'
```

## Monitoring
Security log on AD FS servers: event **1203** (each bad password attempt) and **1210** (user locked out).
Alert on spikes of 1210 across many users = spray in progress.

## Also
Enable Entra ID Connect Health for AD FS for risky IP reports, and move apps to Entra ID where possible.

## Verify
- [ ] ExtranetLockoutMode Enforce; test account locks on extranet only after the threshold while internal sign-in works.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main (AD FS content, ms.date 2023-2024; AD FS in Windows Server 2016-2025).
Confirmed from Configure-AD-FS-Extranet-Smart-Lockout-Protection (ms.date 2023-06-16): Set-AdfsProperties parameters and mode names,
restart of adfssrv on all nodes, 20 familiar IP limit, half-of-AD threshold advice, artifact store permission cmdlet, the three account-activity cmdlets and their
-Location values, and events 1203 and 1210. Removed event 411 (not listed for smart lockout) and the -Identity and -UserPrincipalName parameter spellings (the page uses positional UPN).
Method: documentation only; no commands were run.
