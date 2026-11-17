---
id: computing-software.systems-network-administration.active-directory.fine-grained-password-policies
name: fine-grained-password-policies
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, fine-grained-password-policy, pso, new-adfinegrainedpasswordpolicy, add-adfinegrainedpasswordpolicysubject, get-aduserresultantpasswordpolicy, msds-resultantpso, precedence, service-accounts, resultant-password-policy]
level: practitioner
status: docs-checked
description: "Apply different password/lockout rules to admins or service accounts with PSOs: create, assign to groups, precedence, and checking the resultant policy per user."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/fine-grained-password-policies
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-adfinegrainedpasswordpolicy
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-aduserresultantpasswordpolicy
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fine-grained password policies (PSOs)

**Use for:** longer passwords for admins, very long passwords for legacy service accounts
that cannot be gMSAs, or a stricter lockout for a sensitive group, within one domain.

## Create and assign
```powershell
New-ADFineGrainedPasswordPolicy -Name 'PSO-Admins' -Precedence 10 `
  -MinPasswordLength 20 -ComplexityEnabled $true -PasswordHistoryCount 24 `
  -MaxPasswordAge 365.00:00:00 -MinPasswordAge 1.00:00:00 `
  -LockoutThreshold 5 -LockoutDuration 00:30:00 -LockoutObservationWindow 00:30:00 `
  -ReversibleEncryptionEnabled $false -ProtectedFromAccidentalDeletion $true
Add-ADFineGrainedPasswordPolicySubject 'PSO-Admins' -Subjects 'GG-Tier0-Admins','GG-Tier1-Admins'

New-ADFineGrainedPasswordPolicy -Name 'PSO-ServiceAccounts' -Precedence 20 -MinPasswordLength 30 `
  -MaxPasswordAge 0 -LockoutThreshold 0 -ComplexityEnabled $true -PasswordHistoryCount 5 -MinPasswordAge 0
Add-ADFineGrainedPasswordPolicySubject 'PSO-ServiceAccounts' -Subjects 'GG-Legacy-ServiceAccounts'
```
Microsoft's ADAC page lists a domain functional level of Windows Server 2012 or higher and Domain Admins membership as
prerequisites. In ADAC the policies are under System > Password Settings Container. Only global security groups and user
objects can have a policy applied.

## Precedence rules
The resultant PSO (`msDS-ResultantPSO`) is chosen as follows (Get-ADUserResultantPasswordPolicy reference):
1. If only one PSO is associated with the user, it is the RSoP.
2. If several are associated, the PSO applied **directly to the user** wins; if several apply directly, the one with the
   lowest `msDS-PasswordSettingsPrecedence` value wins (and a warning is logged in the AD event log).
3. If none applies directly, the PSOs of the user's global security groups are compared and the lowest precedence value
   wins. A lower `Precedence` number means higher priority.
PSOs apply only to **global security groups** and users.

## Check what applies
```powershell
Get-ADUserResultantPasswordPolicy jsmith
```

## Gotchas
- A lockout threshold of 0 means the policy does not throttle guessing; monitor failed logons for those accounts.
  (Check how your DCs interpret 0 for the other values before relying on it.)

## Verify
- [ ] `Get-ADUserResultantPasswordPolicy` returns the expected PSO for an admin and a service account.

## Checked

Documentation: Microsoft Learn "Configure fine grained password policies" (ADAC page) and the
New-ADFineGrainedPasswordPolicy, Add-ADFineGrainedPasswordPolicySubject and Get-ADUserResultantPasswordPolicy references,
from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: cmdlet and parameter names used (including `-Precedence`, `-ProtectedFromAccidentalDeletion`,
`-LockoutObservationWindow`, TimeSpan parameters, `-Subjects`), global-security-group restriction, precedence and direct
assignment rules, Password Settings Container location. Wrong: the domain functional level (the current page states
Windows Server 2012 or higher, not 2008). Removed unconfirmed: "ties: lowest GUID", the msDS-ResultantPSO and
`Get-ADFineGrainedPasswordPolicy` verification lines, the "no PSO means default policy" paraphrase and the helpdesk and
password-change remarks.

Method: documentation only; no commands were run.
