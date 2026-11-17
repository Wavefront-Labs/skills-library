---
id: computing-software.it-support-helpdesk.intune-mdm.windows-laps-local-admin-password
name: windows-laps-local-admin-password
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, windows-laps, laps, local-admin-password, account-protection, password-rotation, entra-id, intune]
level: practitioner
status: docs-checked
description: "Run Windows LAPS from Intune: account protection policy, Entra or AD backup, roles to view and rotate passwords, manual rotation rules, policy conflicts and FAQ limits."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/windows-laps-overview"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/windows-laps-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-laps-local-admin-password

Windows LAPS is built into Windows (April 11, 2023 updates and later; the legacy Microsoft LAPS MSI is deprecated and newer
OS versions block its installer). Intune manages it through the Windows LAPS CSP, which overrides GPO and legacy LAPS
configuration. LAPS manages one local admin account per device.

## Prerequisites
- Device join: Entra joined or hybrid joined can back up to Entra ID; domain joined can back up to AD. Hybrid joined can use
  either, never both. Workplace-joined devices are not supported. A directory type that the join type cannot use is accepted
  by the device without error but does not work.
- Entra joined: enable LAPS in the Entra admin center, Identity > Devices > Overview > Device settings > Enable Local
  Administrator Password Solution (LAPS) = Yes (as Cloud Device Administrator). Hybrid joined does not need this.
- Supported OS builds include Windows 11 22H2 (22621.1555+, KB5025239), 21H2 (22000.1817+, KB5025224), Windows 10 22H2, 21H2,
  20H2 (build x.2846+, KB5025221) and Windows 10 Enterprise LTSC 2019 and later. Windows 10 is past end of support.
- Licensing: Intune Plan 1 and Entra ID Free are enough.
- A disabled device in Entra is not rotated or backed up. If a device is deleted in Entra, its stored password is lost and
  cannot be recovered.

## Policy
Intune admin center > Endpoint security > Account protection > Create Policy > Platform Windows, Profile **Local admin
password solution (Windows LAPS)**. Needs rights from the Security baselines category (built-in role Endpoint Security Manager).
- **Backup Directory**: Entra ID, Active Directory, or no backup; the choice decides which other settings appear.
- **Administrator Account Name**: blank manages the built-in admin account (by RID, whatever it is named). A name that does not
  exist on the device means no account is managed, with no error (on manual mode or Windows 11 23H2 and earlier).
- Policies do not create accounts or passwords. Automatic account management (Windows 11 24H2 and later) can enable or
  disable the account, randomise its name, and create a custom account.
- Other settings: password complexity and length, password age (PasswordAgeDays), post-authentication actions (reset the
  password, log off, or both then power down) and the delay before they run.
- Assign to device groups, not user groups: user-group policy follows the user and can change which account is managed.
- Changing the account in policy leaves the old account unmanaged, and its details disappear from Intune and the directory.

## Conflicts
- Two policies setting different values: on a device with working policy, the last-set values remain and both policies show
  conflict; on a device with no LAPS policy, nothing is sent and both show conflict. Remove assignments or align settings.
- Two policies naming different accounts conflict.

## View and rotate
- Devices > All devices > device > Monitor > **Local admin password**: account name, SID, password (Show, Copy), last and next
  rotation in UTC. The password is viewable only for Entra backup, not AD.
- Viewing the password triggers an audit event. Entra roles: Cloud Device Administrator and Intune Administrator can recover
  passwords. The permission `microsoft.directory/deviceLocalCredentials/password/read` reads passwords and
  `.../standard/read` reads metadata only. The metadata roles are Security Reader, Cloud Device Administrator, Intune
  Administrator, Helpdesk Administrator and Security Administrator.
- The Local admin password button is greyed out without the Intune permission Remote tasks: Rotate Local Admin Password.
- **Rotate local admin password** (ellipsis menu on the device): needs Managed devices: Read, Organization: Read and Remote
  tasks: Rotate Local Admin Password. No built-in Intune role or the Intune Administrator role includes the rotate permission;
  make a custom role. One device at a time, no bulk action. An Entra joined device must be online; a device that never backed
  up the account fails. Each manual or scheduled rotation logs an audit event, and a manual rotation resets the PasswordAgeDays clock.
- Device actions status on the device Overview shows pending, complete or failed.

## Desk procedure
Verify the requester and ticket, share the password only with the engineer on the device, never paste it into the ticket,
and rotate it after use.

## Verify
After the device checks in, Intune shows the account with last and next rotation dates, and the password works.

## Checked
Date: 2026-11-08. Read in full: "Microsoft Intune support for Windows LAPS" and "Deploy Windows LAPS policy with Microsoft
Intune" (both updated 2026-04-15) and "What is Windows LAPS?" (2026-09-16). Removed as unconfirmed: typical value table
(30 days, Entra minimum 7, length 14, 24 hour delay), the Entra tenant "Device settings" wording for Entra (page uses its own path),
Get-LapsAADPassword, Invoke-LapsPolicyProcessing and Get-LapsDiagnostics commands, LAPS event IDs and event log path, the
"password missing" cause, and the restored-from-backup note. Corrected: Intune Administrator does not include the rotate permission.
Method: documentation only; no commands were run.
