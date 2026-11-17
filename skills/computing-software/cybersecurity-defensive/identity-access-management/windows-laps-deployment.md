---
id: computing-software.cybersecurity-defensive.identity-access-management.windows-laps-deployment
name: windows-laps-deployment
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [pam, laps, windows-laps, local-administrator, password-rotation, intune, active-directory]
level: practitioner
status: draft
description: "Deploy Windows LAPS to give every device a unique, rotated local admin password: AD or Entra backup, policy settings, permissions, retrieval auditing and legacy LAPS migration."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview", "https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings", "https://learn.microsoft.com/en-us/mem/intune/protect/windows-laps-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows LAPS

**Goal:** no two machines share a local administrator password, passwords rotate
automatically, and reading one is restricted and audited. Shared local admin passwords
are a classic lateral-movement path (pass-the-hash across the estate).

## Windows LAPS (built in since April 2023 updates)
Supports Windows 10/11 and Server 2019+ natively; backs up to **Active Directory** or
**Microsoft Entra ID**; supports password encryption in AD, password history, DSRM account
backup on DCs, and post-authentication actions.

## AD backup setup
```powershell
Update-LapsADSchema                       # once, Schema Admin
Set-LapsADComputerSelfPermission -Identity "OU=Workstations,DC=example,DC=com"
Set-LapsADReadPasswordPermission -Identity "OU=Workstations,DC=example,DC=com" -AllowedPrincipals "EXAMPLE\LAPS-Workstation-Readers"
```
GPO (Computer Configuration > Administrative Templates > System > LAPS):
- *Configure password backup directory*: Active Directory.
- *Password settings*: complexity large+small+numbers+specials, length 15+, age 30 days.
- *Enable password encryption* (domain functional level 2016+), authorised decryptors group.
- *Post-authentication actions*: reset password and log off after use, grace period hours.
- *Name of administrator account to manage* if not the built-in Administrator.

## Entra/Intune setup
Entra ID > Devices > Device settings: enable LAPS. Intune > Endpoint security > Account
protection > LAPS policy (backup directory Entra, rotation). Readers need
`microsoft.directory/deviceLocalCredentials/password/read` (e.g. Cloud Device Administrator)
scoped via administrative units.

## Retrieve
```powershell
Get-LapsADPassword -Identity WS-0142 -AsPlainText
Get-LapsAADPassword -DeviceIds <id> -IncludePasswords -AsPlainText   # Microsoft Graph module
Reset-LapsPassword                                                    # on the device, rotate now
```

## Audit and monitoring
- AD: enable auditing on the password attribute reads (`msLAPS-Password` /
  `msLAPS-EncryptedPassword`), events 4662; Entra: audit log "Recover device local administrator password".
- Alert on bulk reads and on reads by accounts outside the help desk/admin groups.
- Device event log: Applications and Services > Microsoft > Windows > LAPS > Operational.

## Migration from legacy LAPS
Legacy Microsoft LAPS (AdmPwd, `ms-Mcs-AdmPwd` attribute) and Windows LAPS can run side by
side only if they manage different accounts; disable legacy policy (or use emulation mode) as
you move OUs.

## Gotchas
- Delegated "All extended rights" on computer objects lets others read legacy LAPS passwords;
  review OU ACLs (`Find-LapsADExtendedRights`).
- Rotation fails silently on devices that cannot reach a DC or Entra; report password age.

## Verify
A sample of devices shows unique passwords with expiry dates within policy; a non-authorised
account cannot read them; retrieval creates audit events.
