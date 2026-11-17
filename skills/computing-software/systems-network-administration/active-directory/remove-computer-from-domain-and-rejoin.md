---
id: computing-software.systems-network-administration.active-directory.remove-computer-from-domain-and-rejoin
name: remove-computer-from-domain-and-rejoin
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, remove-computer, add-computer, unjoin, rejoin]
level: intro
status: docs-checked
description: "Remove a Windows computer from the domain and rejoin it cleanly with Remove-Computer and Add-Computer, keeping the AD object, ACLs and local admin access."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/remove-computer
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/add-computer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remove a computer from the domain and rejoin

Usually the trust is broken (secure channel) and `Test-ComputerSecureChannel -Repair` fixes it without rejoin
(see computer-account-and-secure-channel). Rejoin only when repair fails.

## Before you start
- Know a **local administrator** password (or LAPS). After unjoining, domain accounts cannot log on.
- Cached domain credentials will not help on a workgroup machine.

## Unjoin
```powershell
Remove-Computer -UnjoinDomainCredential AD\joinadmin -WorkgroupName WORKGROUP -Restart -Force
```
`Remove-Computer` also disables the computer's domain account (it is not deleted). You must supply explicit
credentials to unjoin, even your own, and move the computer to a workgroup with `-WorkgroupName`; `-Force` only
suppresses the prompt.

## Rejoin keeping the same object
Optionally reset the account first (ADUC > right-click > Reset Account). Then on the machine:
```powershell
Add-Computer -DomainName ad.example.com -Credential AD\joinadmin -OUPath 'OU=Workstations,DC=ad,DC=example,DC=com' -Restart
```
Rejoining with the same name reuses the existing account. Since the October 11, 2022 updates (KB5020276) that is
blocked (`0xaac`) unless the joiner created the account, it was created by a member of an administrator group, or its
owner is listed in the Group Policy setting *Domain controller: Allow computer account reuse during domain join*. For an
existing account the joiner also needs Reset Password on it.

## Remote, one step
```powershell
Add-Computer -ComputerName PC042 -LocalCredential PC042\Administrator -DomainName ad.example.com -Credential AD\joinadmin -Restart -Force
```

## Verify
- [ ] `Test-ComputerSecureChannel` True; `nltest /sc_query:ad.example.com` success; user logon works.

## Checked
2026-10-27, against the Remove-Computer, Add-Computer and Test-ComputerSecureChannel cmdlet pages (Windows PowerShell 5.1) and the Learn domain-join articles. Confirmed: Remove-Computer -UnjoinDomainCredential -WorkgroupName -Restart -Force, that it disables the domain account and needs explicit credentials; Add-Computer -DomainName -Credential -OUPath -Restart, and -ComputerName with -LocalCredential for remote joins; the October 11, 2022 account-reuse conditions and the GPO name; the Reset Password requirement for existing objects. Removed as unconfirmed: the claim that -Force without credentials leaves the object enabled, and the statement about keeping group memberships and GPO targeting.

Method: documentation only; no commands were run.
