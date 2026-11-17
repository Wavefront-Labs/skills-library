---
id: computing-software.systems-network-administration.active-directory.password-never-expires-and-weak-account-audit
name: password-never-expires-and-weak-account-audit
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, password-never-expires, pwdlastset, reversible-encryption]
level: practitioner
status: docs-checked
description: "Report accounts with password never expires, old pwdLastSet, reversible encryption, no pre-auth or PASSWD_NOTREQD, and remediate without outages."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/search-adaccount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing weak password settings on accounts

Domain password policy is meaningless for accounts that opt out via userAccountControl flags.

## Report
```powershell
# Password never expires (UAC 0x10000)
Search-ADAccount -PasswordNeverExpires -UsersOnly | Format-Table Name,SamAccountName
# Old passwords (> 1 year)
$cut = (Get-Date).AddDays(-365)
Get-ADUser -Filter 'Enabled -eq $true -and PasswordLastSet -lt $cut' -Properties PasswordLastSet | Select Name,PasswordLastSet
# Password not required (0x20), reversible encryption (0x80), no Kerberos pre-auth (0x400000), DES only (0x200000)
Get-ADUser -LDAPFilter '(|(userAccountControl:1.2.840.113556.1.4.803:=32)(userAccountControl:1.2.840.113556.1.4.803:=128)(userAccountControl:1.2.840.113556.1.4.803:=4194304)(userAccountControl:1.2.840.113556.1.4.803:=2097152))' -Properties userAccountControl
```
Review every account the last query returns; each of those flags weakens the account's authentication.

## Remediate by category
- **Service accounts**: move to gMSA; otherwise long random passwords, a rotation schedule and an owner field.
- **Humans with never-expires**: clear the flag; if you have moved to no-expiry policy (NIST style) do it via policy
  with banned-password protection and MFA, not per-account flags.
- **PASSWD_NOTREQD / reversible / no pre-auth / DES**: clear flags (`Set-ADAccountControl -PasswordNotRequired $false`,
  `-DoesNotRequirePreAuth $false`, `-AllowReversiblePasswordEncryption $false`, `-UseDESKeyOnly $false`).
- `Set-ADUser -ChangePasswordAtLogon $true` forces a change at next logon; avoid it on service accounts.

## Verify
- [ ] Monthly report trending down; exceptions documented with an owner and expiry.

## Checked
2026-10-27, against the userAccountControl article (SupportArticles-docs) and the Search-ADAccount, Set-ADAccountControl, Set-ADUser and Get-ADUser cmdlet pages. Confirmed: userAccountControl values 0x20 PASSWD_NOTREQD, 0x80 ENCRYPTED_TEXT_PWD_ALLOWED, 0x10000 DONT_EXPIRE_PASSWORD, 0x200000 USE_DES_KEY_ONLY, 0x400000 DONT_REQ_PREAUTH; Search-ADAccount -PasswordNeverExpires and -UsersOnly; Set-ADAccountControl -PasswordNotRequired, -DoesNotRequirePreAuth, -AllowReversiblePasswordEncryption, -UseDESKeyOnly; Set-ADUser -ChangePasswordAtLogon; the bitwise LDAP matching rule OID in Get-ADUser -LDAPFilter. The PasswordLastSet property is shown on the Get-ADComputer page and is queried the same way on users. Removed as unconfirmed: Get-ADUser -Filter on PasswordNeverExpires, the roasting remark, the 25-character figure and the reversible-encryption password-change note.

Method: documentation only; no commands were run.
