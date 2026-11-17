---
id: computing-software.it-support-helpdesk.desktop-support.aduc-tasks-and-password-expiry
name: aduc-tasks-and-password-expiry
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, active-directory-users-computers, password-expiry, aduc, account-management, fine-grained-password-policy]
level: practitioner
status: docs-checked
description: "Get the Active Directory Users and Computers tools onto a help desk PC via RSAT and find which password policy, including fine-grained policy, applies to a user."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/remote-server-administration-tools"
  - "https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-aduser"
  - "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/fine-grained-password-policies"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aduc-tasks-and-password-expiry

## Get the tools (RSAT)
- RSAT installs only on Professional or Enterprise editions of the Windows client, not Home. Do not use cracked
  installers (a licence violation).
- Windows 10 version 1809 and later: RSAT is part of the OS. Settings > Apps (System on 22H2 or later) > Optional
  features > Add a feature, search "Remote".
- The AD DS and AD LDS tools include Active Directory Administrative Center, Active Directory Users and Computers,
  Domains and Trusts, Sites and Services, ADSI Edit and the Active Directory module for Windows PowerShell.
- On Windows 11 25H2 Arm64 the Control Panel "Turn Windows features on or off" route exposes only some RSAT tools
  (AD DS and LDS, AD CS, Server Manager, Group Policy Management, DNS, DHCP).
- Do desk tasks only with the rights your delegation grants.

## Which password policy applies to a user
- Fine-grained password policies are Password Settings objects held in the System > Password Settings Container,
  managed in Active Directory Administrative Center (New > Password Settings; Name and Precedence are required).
- To see the effective policy for one user: ADAC "View Resultant Password Settings", or
  `Get-ADUserResultantPasswordPolicy -Identity <user>`.
- If no fine-grained policy applies, the domain-level password policy governs.
- `Get-ADUser -Identity <user> -Properties *` shows the account's attributes for expiry checks.

## Pitfalls
- Resetting a password without identity verification.
- "Password never expires" set as a quick fix and left on.

## Verify
The user signs in with the new password on all devices (including phone mail), and changes stayed within delegated rights.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the RSAT, Get-ADUser and fine-grained password policy pages. Removed because the pages do not state
them: the RSAT capability name, dsa.msc, the table of reset/unlock/group cmdlets, sync timing to Entra, expiry
attribute query, NIST/Microsoft guidance, cached credential behaviour and Entra expiry defaults.
