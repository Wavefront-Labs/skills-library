---
id: computing-software.systems-network-administration.active-directory.windows-laps-backup-to-entra-id
name: windows-laps-backup-to-entra-id
category: computing-software
field: systems-network-administration
product: active-directory
tags: [windows-laps, laps-entra-id, intune, entra-id-join, laps-policy]
level: practitioner
status: docs-checked
description: "Back up Windows LAPS passwords to Microsoft Entra ID with Intune or CSP policy, grant read roles, retrieve and rotate, and know the server limits."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/devices/howto-manage-local-admin-passwords
  - https://learn.microsoft.com/en-us/intune/intune-service/protect/windows-laps-policy
  - https://learn.microsoft.com/en-us/powershell/module/laps/get-lapsaadpassword
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS backup to Microsoft Entra ID

## Where it applies
- Microsoft Entra joined and Microsoft Entra hybrid joined devices only; Entra registered devices are not supported.
  Windows Server 2019 and 2022 need the April 2023 updates or later (see the Microsoft list of required updates).
- One backup directory per device: `BackupDirectory` 1 backs up to Entra only, 2 to Active Directory only, 0 disables backup.
  The directory type in the policy must match the device's join type.
- LAPS in Entra is available with Entra ID Free or higher; related features such as administrative units, Conditional
  Access and Intune have their own licensing.

## Turn it on
1. Entra admin center > Devices > Device settings: set **Enable Local Administrator Password Solution (LAPS)** to Yes
   and Save (needs at least Cloud Device Administrator).
2. Client policy with `BackupDirectory` = Entra ID. With Intune: Endpoint security > Account protection > **Create
   Policy** > the *Local admin password solution (Windows LAPS)* profile, choose the Backup Directory, then set password age
   days, complexity, length, post-authentication actions, and **Administrator Account Name** (Intune applies to one
   account per device; if the named account is not on the device, no account is managed). Without Intune use the LAPS CSP
   or Group Policy on hybrid joined devices; the Group Policy registry root is
   `HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\LAPS`.

## Who can read
Roles holding `microsoft.directory/deviceLocalCredentials/password/read`: built-in **Cloud Device Administrator** and
**Intune Administrator**, or a custom role (optionally scoped to an administrative unit). The metadata permission
`.../standard/read` is also held by Helpdesk Administrator, Security Reader and Security Administrator. Password reads
are audited in Entra, and Conditional Access can be scoped to the built-in roles.

## Retrieve and rotate
```powershell
Connect-MgGraph -Scopes DeviceLocalCredential.Read.All
Get-LapsAADPassword -DeviceIds <DEVICE_NAME_OR_ID> -IncludePasswords -AsPlainText
```
`-DeviceIds` accepts a device name or ID; `-IncludeHistory` adds previous passwords. Querying metadata only needs
`DeviceLocalCredential.ReadBasic.All`. In Intune, the device remote task **Rotate local admin password** rotates a password
outside the policy schedule; it fails for a device that has not yet backed up its account and password.

## Gotchas
- Only one account is managed per device; changing the policy's account name stops managing the old account.
- Password Age Days minimum is 7 when the backup directory is Entra ID (1 for Active Directory), maximum 365, default 30.
- Backing up DSRM passwords to Entra is not supported.
- Do not target one device with conflicting AD and Entra policies; keep a single policy source.

## Verify
- [ ] The device shows local administrator password recovery in the Entra portal.
- [ ] LAPS Operational log (Applications and Services Logs > Microsoft > Windows > LAPS > Operational) shows event 10029
  for a successful Entra password update.

## Checked
Checked 2026-10-27 against Microsoft Learn: entra-docs (manage local admin passwords, dated current), windowsserverdocs
(LAPS policy settings dated 2025-06-26, event log), Intune Windows LAPS policy page and the LAPS PowerShell reference
(Windows Server 2025). Confirmed backup directory values, roles and permissions, cmdlet parameters and Graph scopes, the
7-day Entra minimum, the Intune policy path and rotate action, and event 10029. Corrected the tenant switch label, the
unsupported-device scope, and removed the "last applied directory wins" and "event 10025+" claims.
Method: documentation only; no commands were run.
