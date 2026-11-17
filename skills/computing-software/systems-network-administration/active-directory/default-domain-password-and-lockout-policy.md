---
id: computing-software.systems-network-administration.active-directory.default-domain-password-and-lockout-policy
name: default-domain-password-and-lockout-policy
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, default-domain-password-policy, account-lockout-policy, default-domain-policy, set-addefaultdomainpasswordpolicy, nist-800-63b, minimum-password-length, lockout-threshold]
level: practitioner
status: docs-checked
description: "Set the domain-wide password and lockout policy correctly: only via the Default Domain Policy, modern length-over-rotation values, and lockout tuned against spraying."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-addefaultdomainpasswordpolicy
  - https://learn.microsoft.com/en-us/microsoft-365/admin/misc/password-policy-recommendations
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/account-lockout-threshold
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/account-lockout-duration
  - https://pages.nist.gov/800-63-4/sp800-63b.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default domain password and lockout policy

## Where it lives
Domain account policies (password, lockout, Kerberos) are the **Account Policies** section of the **Default Domain
Policy** GPO. For different values for particular users or groups, use fine-grained password policies (password
settings objects, PSOs), which apply to the groups or users listed under Directly Applies To and have a Precedence.

## Read and set
```powershell
Get-ADDefaultDomainPasswordPolicy
Set-ADDefaultDomainPasswordPolicy -Identity ad.example.com `
  -MinPasswordLength 14 -ComplexityEnabled $true -PasswordHistoryCount 24 `
  -MaxPasswordAge 0.00:00:00 -MinPasswordAge 1.00:00:00 `
  -LockoutThreshold 10 -LockoutDuration 00:15:00 -LockoutObservationWindow 00:15:00
```
Setting `-MaxPasswordAge` to 0 converts it to "never" (stored as -9223372036854775808). Keep the Default Domain Policy
GPO and any scripted values identical, and re-read the policy after each change. The values above are examples to
adapt, not mandated settings.

## Current guidance
- **Length over complexity.** NIST SP 800-63B (rev 4) requires a minimum of 15 characters for passwords used as
  the only factor and says verifiers must not impose composition rules. Microsoft 365 guidance recommends a minimum
  of 14 characters.
- **No forced periodic expiry.** NIST says verifiers must not require periodic password changes but must force a
  change on evidence of compromise; Microsoft's guidance discourages expiration policies for cloud-only accounts and
  recommends passwords that never expire, paired with Entra Password Protection to remove bad passwords. Some
  regulations still demand rotation; document the exception. (Microsoft's older security-policy reference for
  Maximum password age still suggests 30 to 90 days, so state which standard you follow.)
- **Lockout.** The threshold is a balance between operational efficiency and security: a threshold that is set
  creates a denial-of-service exposure, and 0 disables lockout. Microsoft advises a lockout duration of about 15
  minutes and its security baselines use 15 for the reset-counter window.

## Gotchas
- Service accounts under the default policy with no expiry need a PSO or gMSA rather than
  "password never expires" flags scattered around.

## Verify
- [ ] `Get-ADDefaultDomainPasswordPolicy` matches the GPO and the documented standard.
- [ ] `gpresult /scope computer /v` on a DC shows the Default Domain Policy as the winning account policy.

## Checked
2026-10-27. Documentation: Microsoft Learn `Set-ADDefaultDomainPasswordPolicy`, Microsoft 365 password policy
recommendations, security-policy references (account lockout threshold and duration, reset counter, maximum password age,
minimum password length) and NIST SP 800-63B-4. Confirmed: cmdlet parameters and the `-MaxPasswordAge 0` behaviour; NIST
15-character single-factor minimum, no composition rules, no periodic change unless compromised; Microsoft 365 14-character
recommendation and no-expiry recommendation for cloud-only accounts; lockout duration about 15 minutes, reset-counter 15 in
baselines, and the lockout denial-of-service trade-off; fine-grained policy fields (Precedence, Directly Applies To).
Removed as unconfirmed: the domain-root-only GPO rule, the 2022 relaxed-length setting and GPO-UI cap, the threshold of
10 as a recommendation (kept only as an example value), minimum-age rationale and the min-length-change-at-next-change note.
Method: documentation only; no commands were run.
