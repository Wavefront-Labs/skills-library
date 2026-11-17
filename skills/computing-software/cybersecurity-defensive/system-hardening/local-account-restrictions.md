---
id: computing-software.cybersecurity-defensive.system-hardening.local-account-restrictions
name: local-account-restrictions
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [local-account-restrictions, pass-the-hash, laps, localaccounttokenfilterpolicy, windows-hardening, lateral-movement]
level: practitioner
status: docs-checked
description: "Stop local admin accounts being used for lateral movement: deny network and RDP logon for local accounts, UAC remote token filtering, and unique passwords with LAPS."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/securing-privileged-access/securing-privileged-access-reference-material", "https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/user-account-control-and-remote-restriction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local account network logon restrictions

If every workstation shares the same local administrator password (common with imaged machines), one stolen
hash gives admin on all of them via pass-the-hash. Three controls together break this.

## 1. Deny network and RDP logon to local accounts
Use User Rights Assignment (*Computer Configuration > Windows Settings > Security Settings > Local Policies > User Rights Assignment*) to deny network logon (*Deny access to this computer from the network*) and Remote Desktop logon (*Deny log on through Remote Desktop Services*) to local accounts. Windows exposes well-known groups for local accounts and local administrators in the account picker; check the exact names on your Windows build before rollout. Do not apply this on domain controllers.

## 2. UAC remote restrictions (token filtering)
A member of the local Administrators group who connects remotely with a local (SAM) account does not get a full administrator token. Ensure `LocalAccountTokenFilterPolicy` under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System` is 0 or absent: 0 (the default) builds a filtered token, 1 builds an elevated token and removes the protection.

## 3. Unique passwords: Windows LAPS
Native Windows LAPS manages the local administrator password per device and backs it up to Active Directory or Microsoft Entra ID; it is the supported replacement for the deprecated legacy Microsoft LAPS. Configure it with Group Policy or Intune. Restrict who can read passwords (`Set-LapsADReadPasswordPermission`) and audit retrievals.

## Detect
- Network or Remote Desktop logons with a local account name from another host.
- Bursts of local administrator logon failures across many hosts.
- LAPS password reads (directory audit logs).

## Gotchas
- Some legacy management tools rely on local admin over the network; move them to domain service accounts with
  least privilege.
- Remote helpdesk tools may break; test.
- Do not deny network logon to local accounts on standalone (workgroup) servers managed only that way without an
  alternative.

## Verify
A remote administrative connection with a local account is refused; `Get-LapsADPassword` works for authorised admins only; the registry shows `LocalAccountTokenFilterPolicy` absent or 0.

## Checked

2026-10-28. Confirmed against: Microsoft Learn 'User Account Control and remote restrictions' (LocalAccountTokenFilterPolicy values and behaviour); Windows LAPS overview (native LAPS, AD and Entra ID backup, legacy LAPS deprecated); Windows LAPS PowerShell reference (Get-LapsADPassword, Set-LapsADReadPasswordPermission).

Removed as unconfirmed: well-known SIDs and the exact deny group names, FilterAdministratorToken and Admin Approval Mode paragraph, LAPS build date and example values, event ids.

Method: documentation only; no commands were run.
