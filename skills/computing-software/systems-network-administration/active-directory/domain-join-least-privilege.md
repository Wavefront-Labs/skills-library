---
id: computing-software.systems-network-administration.active-directory.domain-join-least-privilege
name: domain-join-least-privilege
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, add-computer, domain-join-ou, join-account-delegation, machineaccountquota, ms-ds-machineaccountquota, redircmp, computer-account]
level: practitioner
status: docs-checked
description: "Join servers straight into the right OU with Add-Computer -OUPath using a delegated join account, set MachineAccountQuota to 0, and redirect the default Computers container."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/add-computer
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/default-workstation-numbers-join-domain
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/active-directory-domain-join-permissions
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/failure-when-you-use-an-existing-computer-account-to-join-a-domain
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain join with least privilege

## Join into the target OU
```powershell
Add-Computer -DomainName ad.example.com -OUPath 'OU=Servers,OU=Tier1,DC=ad,DC=example,DC=com' `
  -NewName APP08 -Credential (Get-Credential AD\svc-join) -Restart
```
Joining into the right OU means the correct GPOs (security baseline, LAPS) apply at first
boot instead of after someone moves the object.

## A dedicated join account
1. Create `svc-join` (or a group `DL-Delegation-DomainJoin`) with no other rights.
2. Delegate on the target OUs: create and delete computer objects, plus on computer objects the rights Microsoft
   lists for domain join: Reset password, Validated write to DNS host name, Validated write to service principal
   name and Write account restrictions (needed to update `userAccountControl`).
3. Store the credential in your deployment tool's vault, rotate it.

## Shut the default door
- By default authenticated users can join up to 10 computers to the domain (`ms-DS-MachineAccountQuota` = 10), which
  lets any user create computer accounts. Set it to 0 once joins go through the delegated account.
```powershell
Set-ADDomain -Identity ad.example.com -Replace @{'ms-DS-MachineAccountQuota'=0}
```
- Redirect the default computers container (this affects joins that do not specify an OU, such as the Domain Join
  UI), so they land in an OU with GPOs rather than `CN=Computers`, which cannot have GPOs linked:
```cmd
redircmp "OU=Staging,DC=ad,DC=example,DC=com"
```

## Rejoining an existing name
Updates released on and after 11 October 2022 (KB5020276, domain join hardening) block a join from reusing an existing
computer account unless: the joining user created the existing account; it was created by a member of Domain Admins,
Enterprise Admins or the built-in Administrators; or the account's owner is in the **Domain controller: Allow
computer account reuse during domain join** policy (needs updates from 14 March 2023 on all members and DCs).
Otherwise delete the stale object first, or join with the account that created it. The failure reads "Re-using the
account was blocked by security policy" (error 0xaac, NERR_AccountReuseBlockedByPolicy).

## Verify
- [ ] `Get-ADObject (Get-ADDomain).DistinguishedName -Properties ms-DS-MachineAccountQuota` shows 0.
- [ ] New server object appears in the target OU and `gpresult /r /scope computer` lists the expected GPOs after reboot.

## Checked
2026-10-27. Documentation: Microsoft Learn domain join permissions, the default-workstation-numbers article, the
existing-computer-account reuse article (updated 12 Feb 2026), Add-Computer and Set-ADDomain reference. Confirmed:
`Add-Computer -OUPath/-NewName/-Credential/-Restart`; the default of 10 machine accounts for authenticated users and the
`ms-DS-MachineAccountQuota` attribute; `Set-ADDomain -Replace`; the four computer-object rights for a join account
(Reset password, validated writes to DNS host name and SPN, write account restrictions); the October 2022 reuse hardening,
its three exceptions and the March 2023 policy requirement; redircmp affects the Domain Join UI and other earlier-version
APIs. Corrected: `Get-ADDomain` has no `-Properties` parameter, so the verify step now uses `Get-ADObject`; the claim that
Domain Admins ownership allows reuse was replaced with the documented conditions. Removed as unconfirmed: the RBCD and
relay-attack remark.
Method: documentation only; no commands were run.
