---
id: computing-software.cybersecurity-defensive.identity-access-management.gpo-security-review
name: gpo-security-review
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [gpo-security-review, group-policy, gpo-permissions, sysvol-review, gpp-passwords, active-directory-security, gpo-delegation]
level: advanced
status: gated
description: "Review Group Policy for security: who can edit and link GPOs, GPP cpassword leftovers, scripts in SYSVOL, dangerous settings, unlinked/empty GPOs and change monitoring."
sources: ["https://learn.microsoft.com/en-us/powershell/module/grouppolicy/", "https://learn.microsoft.com/en-us/security-updates/securitybulletins/2014/ms14-025", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPO security review

A user who can edit a GPO linked to computers can run code as SYSTEM on all of them.

## 1. Permissions (gated: unconfirmed, source is paywalled or blocked)
```
Get-GPO -All | ForEach-Object {
  $g = $_; Get-GPPermission -Guid $g.Id -All |
  Where-Object { $_.Permission -in 'GpoEdit','GpoEditDeleteModifySecurity' -and
                 $_.Trustee.Name -notin 'Domain Admins','Enterprise Admins','SYSTEM' } |
  Select-Object @{n='GPO';e={$g.DisplayName}}, @{n='Trustee';e={$_.Trustee.Name}}, Permission }
```
Also check: link permissions on OUs (permission to write the GPO link attribute), who can create GPOs (Group Policy Creator Owners
membership), and the SYSVOL folder ACLs (`\\domain\SYSVOL\domain\Policies\{GUID}`) matching the GPO.
BloodHound shows GPO edit rights as attack paths.

## 2. Secrets
- Group Policy Preferences `cpassword` (MS14-025):
  `findstr /S /I cpassword \\<domain>\SYSVOL\<domain>\Policies\*.xml` (gated: unconfirmed, source is paywalled or blocked) - delete those preference items and rotate the passwords.
- Credentials in logon scripts (`net use ... /user:`), batch and PowerShell files in SYSVOL/NETLOGON.

## 3. Settings to scrutinise
- Restricted groups / local group membership adding broad groups to local Administrators.
- Scheduled tasks and startup scripts pointing to writable UNC paths.
- User rights assignments (debug, backup and similar powerful privileges) granted widely.
- Settings that weaken security (disabling Defender, firewall, LSA protection, enabling WDigest).
- Compare to baselines with Policy Analyzer (Security Compliance Toolkit).

## 4. Hygiene
Unlinked GPOs, empty GPOs, disabled links, GPOs with "Authenticated Users" read removed (break processing
see the Group Policy security filtering guidance), enforced links surprising inheritance. Back up with `Backup-GPO -All -Path <dir>`.

## 5. Monitor
Events 5136 (and related directory object events) on `groupPolicyContainer` objects (directory service changes auditing) and SYSVOL
file changes; alert on edits outside change windows.

## Verify
- [ ] No non-admin trustee with edit rights on GPOs linked to tier 0/1 OUs.
- [ ] No cpassword in SYSVOL.

## Checked

2026-10-28. Confirmed against MS14-025 (Group Policy Preferences password distribution), the GroupPolicy module page (Backup-GPO) and the Security Compliance Toolkit page (Policy Analyzer); the Group Policy Creator Owners group appears in the MS-PAC well-known SID list. Gated: Get-GPPermission permission names, cpassword search command. Removed: MS16-072 reference, gPLink attribute name, 5137/5141 event ids, named user rights.

Method: documentation only; no commands were run.
