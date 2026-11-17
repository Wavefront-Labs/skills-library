---
id: computing-software.systems-network-administration.active-directory.windows-laps-policy-configuration
name: windows-laps-policy-configuration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, laps, laps-policy, post-authentication-actions, backupdirectory, password-encryption, administratoraccountname, invoke-lapspolicyprocessing, laps-event-log, gpo]
level: practitioner
status: docs-checked
description: "Configure Windows LAPS by GPO: backup directory, encryption and decryptors, complexity/length/age, managed account name, post-authentication actions, and diagnosis."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-event-log
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-concepts-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS policy configuration

GPO path: *Computer Configuration > Policies > Administrative Templates > System > LAPS*. The template is installed with
Windows as `%windir%\PolicyDefinitions\LAPS.admx`; Windows Update does not copy it to a GPO central store, so copy it there
yourself if you use one. Policy roots are queried in order (LAPS CSP, Group Policy, Local Configuration, legacy Microsoft
LAPS) and the first root with an explicitly defined setting becomes the active policy.

## Settings and documented defaults
| Setting (registry name) | Documented values and default |
|---|---|
| `BackupDirectory` | 0 disabled (default), 1 Entra ID, 2 Active Directory |
| `AdministratorAccountName` | blank = built-in administrator (found by RID); a custom name must already exist, LAPS does not create it; ignored when automatic account management is on |
| `PasswordAgeDays` | 1 to 365 (7 minimum with Entra ID), default 30 |
| `PasswordLength` | 8 to 64, default 14 |
| `PasswordComplexity` | 1 to 4 classic sets (default 4: large, small, numbers, special); 5 to 8 and `PassphraseLength` (default 6 words) need Windows 11 24H2 or Windows Server 2025 |
| `ADPasswordEncryptionEnabled` / `ADPasswordEncryptionPrincipal` | AD only; no default documented, so set it explicitly (DFL 2016 or later); default principal Domain Admins |
| `ADEncryptedPasswordHistorySize` | 0 to 12, default 0 |
| `PasswordExpirationProtectionEnabled` | AD only; default True: expiry cannot be set longer than policy allows |
| `PostAuthenticationActions` / `PostAuthenticationResetDelay` | actions 1 reset, 3 reset and sign out (default), 5 reset and reboot, 11 (24H2 and Server 2025 only) also terminates remaining processes; delay 0 to 24 hours, default 24, 0 disables the actions |
| `ADBackupDSRMPassword` | AD only; default 0; set on DC GPOs only |
| `AutomaticAccountManagement*` | automatic account creation and management; Windows 11 24H2 and Windows Server 2025 only; default name prefix `WLapsAdmin` |

**Post-authentication actions** rotate the password after someone has used it, once the grace period passes, so a
looked-up password is short-lived. They are not supported for the DSRM account.

## Force processing and check
```powershell
Invoke-LapsPolicyProcessing
Get-LapsDiagnostics -OutputFolder <OUTPUT_DIR>
Get-WinEvent -LogName 'Microsoft-Windows-LAPS/Operational' -MaxEvents 20 | Format-Table TimeCreated,Id,Message -Wrap
```
Events in the Operational log: 10003 starts a processing cycle and 10005 marks a failed cycle (with an error code);
10021 shows the policy configuration for Active Directory backup and 10022 for Entra ID; 10018 is a successful AD password
update, 10029 a successful Entra update, 10020 the managed-account update and 10031 a blocked outside change attempt.

## Gotchas
- Do not apply both legacy LAPS and Windows LAPS to the same account; Windows LAPS has a legacy-emulation mode, but plan a
  migration.
- The device must reach a writable DC to back up the password to AD.
- If a named custom account does not exist, no account is managed.

## Verify
- [ ] `Get-LapsADPassword -Identity SRV01 -AsPlainText` (as an authorized decryptor) returns a current password with expiry.
- [ ] After use, the password rotates after the grace period.

## Checked
Checked 2026-10-27 against Microsoft Learn (windowsserverdocs LAPS policy settings dated 2025-06-26, event log and
management PowerShell pages). Confirmed setting names, ranges, defaults, version gates, GPO path, template location and
event IDs. Corrected event meanings (10020 is the account update, 10021 and 10022 are policy-configuration events; 10017
and 10019 were not confirmed as failure events and were removed) and the table values that are not defaults
(the "typical" values were removed in favour of documented defaults).
Method: documentation only; no commands were run.
