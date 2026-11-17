---
id: computing-software.systems-network-administration.active-directory.sensitive-accounts-cannot-be-delegated
name: sensitive-accounts-cannot-be-delegated
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policies, account-not-delegated, sensitive-account, not-delegated, useraccountcontrol, unconstrained-delegation, kerberos-delegation, privileged-accounts]
level: practitioner
status: gated
description: "Set 'Account is sensitive and cannot be delegated' on privileged accounts, find accounts missing it, and understand how it blocks delegation-based credential theft."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-d--securing-built-in-administrator-accounts-in-active-directory
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adaccountcontrol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Account is sensitive and cannot be delegated"

## Why
If an admin authenticates to a server trusted for **unconstrained delegation**, their TGT
is stored on that server and can be stolen and reused. Constrained and resource-based delegation can impersonate them to target services. When the `NOT_DELEGATED` flag (userAccountControl 0x100000, 1048576) is set, the user's security context is not delegated to a service even if the service account is trusted for Kerberos delegation. The setting does not affect the account's ability to sign in or its permissions.

## Set it
```powershell
Get-ADGroupMember 'Domain Admins' -Recursive | ? objectClass -eq 'user' |
  Set-ADAccountControl -AccountNotDelegated $true
Set-ADUser adm-jsmith -AccountNotDelegated $true
```
GUI: ADUC > user > Account tab > Account options > *Account is sensitive and cannot be delegated*.

## Find privileged accounts missing it
```powershell
Get-ADUser -LDAPFilter '(&(adminCount=1)(!(userAccountControl:1.2.840.113556.1.4.803:=1048576)))' |
  Select SamAccountName,DistinguishedName
```
`adminCount=1` marks protected privileged accounts (gated: unconfirmed, source is paywalled or blocked); 1048576 is the NOT_DELEGATED bit. Include the built-in Administrator (RID 500) and break-glass accounts.

## Interplay
- Protected Users members cannot be delegated with Kerberos constrained or unconstrained delegation and have further restrictions; setting the flag as well covers accounts you cannot put in Protected Users.
- Do not set it on service accounts that legitimately need to be delegated (e.g. the
  identity users pass through to a back end); fix the delegation design instead.
- Also review computers trusted for unconstrained delegation (TRUSTED_FOR_DELEGATION, 0x80000, 524288):
```powershell
Get-ADComputer -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=524288)' | Select Name
```

## Verify
- [ ] The missing-flag query returns nothing for admin accounts.

## Checked
Checked 2026-10-27 against Microsoft Learn (userAccountControl flags article; Securing built-in administrator accounts, Appendix D; authentication policies overview for Protected Users; Set-ADAccountControl and Set-ADUser references, Windows Server 2025; Defender for Identity assessments).
- Confirmed: NOT_DELEGATED is 0x100000 (1048576) and TRUSTED_FOR_DELEGATION is 0x80000 (524288); NOT_DELEGATED meaning; the Appendix D recommendation to enable Account is sensitive and cannot be delegated; Set-ADAccountControl -AccountNotDelegated; Protected Users blocks delegation.
- Gated: adminCount=1 as the marker of privileged accounts.
- Removed: the claim that the KDC never issues forwardable tickets, the klist forwardable check and the only-DCs-should-have-it statement.

Method: documentation only; no commands were run.
