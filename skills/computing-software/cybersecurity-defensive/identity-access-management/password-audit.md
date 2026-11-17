---
id: computing-software.cybersecurity-defensive.identity-access-management.password-audit
name: password-audit
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [password-audit, dsinternals, ntds-dit-audit, weak-password-detection, hash-comparison, hibp, password-policy]
level: advanced
status: docs-checked
description: "Audit AD password quality offline with DSInternals: weak, duplicate, empty, LM, breached (HIBP) and never-expiring passwords, with safe handling of hashes."
sources: ["https://github.com/MichaelGrafnetter/DSInternals", "https://haveibeenpwned.com/Passwords", "https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader", "https://pages.nist.gov/800-63-4/sp800-63b.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing AD password hashes

Read-only quality assessment of existing passwords - authorised, documented, done by tier-0 staff on a
tier-0 system. Defensive purpose: find weak and breached passwords to force resets.

## Steps (DSInternals)
The Test-PasswordQuality cmdlet audits AD for weak, duplicate, default, non-expiring and empty
passwords. It takes its input from Get-ADReplAccount (online, over the MS-DRSR replication protocol,
including secret attributes) or Get-ADDBAccount (offline, from a copy of the ntds.dit database).
Both need the secrets property set requested.

```
# Online
Get-ADReplAccount -All -Server lon-dc1.contoso.com -Properties Secrets |
  Test-PasswordQuality -WeakPasswords 'Pa$$w0rd','April2019' `
    -WeakPasswordHashesSortedFile pwned-passwords-ntlm-ordered-by-hash-v8.txt

# Offline, from an IFM backup (boot key read from the SYSTEM hive)
$key = Get-BootKey -SystemHiveFilePath '<ifm>\registry\SYSTEM'
Get-ADDBAccount -All -DatabasePath '<ifm>\Active Directory\ntds.dit' -BootKey $key -Properties Secrets |
  Test-PasswordQuality -IncludeDisabledAccounts -WeakPasswordHashesSortedFilePath <hibp-ntlm-sorted-file>
```
- Disabled accounts are skipped unless `-IncludeDisabledAccounts` is given. `-SkipDuplicatePasswordTest`
  turns off the hash-to-hash comparison. `-WeakPasswordsFile` takes a file with one weak password per line.
- Leaked-password hashes come from HaveIBeenPwned, in the NTLM variant ordered by hash. The sorted
  single-file parameter suits v8 and earlier lists; a directory of files named by the first five
  characters of the hash (the later layout) uses `-WeakPasswordHashesSortedFilePath`. Hashes must be
  sorted because a binary search is used.
- Cross-forest duplicate discovery works by piping accounts from several forests into one call.
- The output is an object, so properties (for example the weak-password list) can be selected for scripted, regular audits.

## Getting the HIBP NTLM list
The official `haveibeenpwned-downloader` dotnet tool downloads the full Pwned Passwords corpus for
offline use. `--ntlm` (or `-n`) fetches NTLM hashes instead of SHA1, and `--single` writes one file
instead of a directory of range files. It verifies each range against the Content-MD5 header.

## Report categories (from the DSInternals sample report)
Reversible-encryption passwords, LM hashes present, no password set, passwords found in the
dictionary, groups of accounts sharing a password, user accounts using their SamAccountName as
password, computer accounts with default passwords, missing Kerberos AES keys, Kerberos
pre-authentication not required, DES-only accounts, Kerberoasting-susceptible accounts, administrative
accounts allowed to be delegated, passwords that never expire, accounts not required to have a
password, and smart-card-required accounts that have a password.

## Remediate
- Force a password change for weak, breached and duplicate findings; prioritise privileged and service accounts.
- Fix the flag-based findings in the report (password-not-required, pre-authentication not required,
  DES-only, never-expires) on the accounts concerned.
- Check new passwords against a blocklist continuously, as NIST SP 800-63B-4 requires of verifiers,
  so the findings do not return.

## Handling
- Results contain account names and hash relationships rather than plaintext, but the inputs (ntds.dit
  copies, boot key, hash dumps) are highly sensitive: restrict, encrypt and delete after remediation.
- Get written authorisation (works council or legal where required).

## Verify
- [ ] A re-run after remediation shows weak and duplicate counts reduced and privileged accounts clean.

## Checked
Method: docs-checked 2026-11-09 against the DSInternals PowerShell docs for Test-PasswordQuality, Get-ADReplAccount and Get-ADDBAccount (raw GitHub markdown, read in full or by grep), the PwnedPasswordsDownloader README (read in full), the HIBP Pwned Passwords page (download and k-anonymity sections) and NIST SP 800-63B-4 (blocklist requirement).
Removed as unconfirmed: the -NamingContext parameter and the DCSync-rights note, the Set-ADUser -PasswordNotRequired remediation command, the Entra Password Protection agent advice and the "never crack hashes" instruction, which the docs do not state.
