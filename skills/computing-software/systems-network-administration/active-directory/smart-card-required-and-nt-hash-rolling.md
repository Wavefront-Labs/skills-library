---
id: computing-software.systems-network-administration.active-directory.smart-card-required-and-nt-hash-rolling
name: smart-card-required-and-nt-hash-rolling
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policies, smartcard-required, smartcardlogonrequired, nt-hash-rolling, pass-the-hash]
level: advanced
status: docs-checked
description: "Enforce smart card required for interactive logon on admin accounts and enable automatic NT hash rolling so the random password does not become a permanent pass-the-hash."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/whats-new-in-credential-protection
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-addomain
  - https://learn.microsoft.com/en-us/windows/security/identity-protection/smart-cards/smart-card-group-policy-and-registry-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart card required and NT hash rolling

Setting **Smart card is required for interactive logon** (`SMARTCARD_REQUIRED`, userAccountControl 0x40000)
makes Windows reset the account's password to a 120-character random value that no user knows. Windows Server 2016
added rolling of expiring NTLM secrets for such accounts.

## Enforce on accounts
```powershell
Set-ADUser da-jsmith -SmartcardLogonRequired $true
Get-ADUser -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=262144)' | Select Name
```

## Roll the hash
Requires the Windows Server 2016 domain functional level. New domains have it enabled by default; for existing
domains, enable it in Active Directory Administrative Center (right-click the domain > Properties > *Enable rolling of
expiring NTLM secrets during sign on for users who are required to use Windows Hello for Business or smart card for
interactive logon*) or with:
```powershell
Set-ADDomain -Identity <DOMAIN> -PublicKeyRequiredPasswordRolling $True
```
This sets the domain attribute **msDS-ExpirePasswordsOnSmartCardOnlyAccounts**. Warning from the documentation: adding
a DC that was enabled before the November 8, 2016 update to a domain that supports rolling can cause the DC to crash.

## Make it workable
- Users need smart cards or Windows Hello for Business credentials; test enrolment first.
- Services and scheduled tasks running as that account will break (no password). Use separate service accounts.
- Pair with Protected Users or an authentication silo for admin accounts.

## Verify
- [ ] Admin accounts flagged; logon with password fails, smart card succeeds.
- [ ] `msDS-ExpirePasswordsOnSmartCardOnlyAccounts` is TRUE on the domain object.

## Checked
2026-10-27, against the Learn pages "What's new in credential protection" (rolling public-key-only users' NTLM secrets), the Set-ADDomain and Set-ADUser cmdlet pages, windowsserverdocs Domain-Wide Updates and Implementing Least-Privilege Administrative Models, and the userAccountControl article. Confirmed: SMARTCARD_REQUIRED 0x40000 (262144); Set-ADUser -SmartcardLogonRequired; the 120-character random password; rolling requires the Windows Server 2016 DFL, is on by default in new domains and is configured in ADAC for existing ones; Set-ADDomain -PublicKeyRequiredPasswordRolling sets msDS-ExpirePasswordsOnSmartCardOnlyAccounts; the pre-November 2016 DC warning. Removed as unconfirmed: the maximum-password-age rotation rule, toggling the flag on older levels, the NTLM re-authentication remark and the pwdLastSet check.

Method: documentation only; no commands were run.
