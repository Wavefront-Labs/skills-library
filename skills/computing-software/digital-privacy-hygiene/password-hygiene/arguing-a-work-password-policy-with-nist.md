---
id: computing-software.digital-privacy-hygiene.password-hygiene.arguing-a-work-password-policy-with-nist
name: arguing-a-work-password-policy-with-nist
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, password-policy, nist-800-63b, password-rotation, composition-rules]
level: practitioner
status: docs-checked
description: "Make the case to IT for a modern password policy using NIST SP 800-63B-4: length over complexity, no forced rotation, blocklists, paste and MFA."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.ncsc.gov.uk/collection/passwords/updating-your-approach"
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/misc/password-policy-recommendations"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Arguing a work password policy against NIST guidance

**Goal:** replace a 90-day, eight-character, must-include-symbol policy with one that actually reduces risk, with
citations IT and auditors accept.

## What NIST SP 800-63B-4 says about passwords
| Topic | Requirement (section 3.1.1) |
|---|---|
| Length | Verifiers SHALL require at least 15 characters when the password is a single-factor mechanism; passwords used only within multi-factor authentication MAY be shorter but SHALL be at least 8. Verifiers SHOULD permit at least 64 |
| Composition rules | SHALL NOT impose other composition rules (such as mixtures of character types) |
| Periodic rotation | SHALL NOT require periodic changes; SHALL force a change on evidence of compromise |
| Blocklist | SHALL compare against commonly used, expected or compromised passwords (the entire password, not substrings) and give a reason on rejection |
| Hints and security questions | SHALL NOT permit a hint accessible to an unauthenticated claimant; SHALL NOT prompt for knowledge-based questions |
| Password managers | SHALL allow password managers and autofill; SHOULD permit paste |
| Characters | SHOULD accept all printing ASCII and the space character, and Unicode (each code point counts as one character) |
| Rate limiting | SHALL implement; failed consecutive attempts on one authenticator limited to no more than 100 (an upper bound, lower limits allowed) |

Appendix A notes that extra length and complexity requirements increase frustration and workarounds, and that
blocklists, hashed storage, machine-generated passwords and rate limiting are more effective.

Other sources to quote:
- UK NCSC ("Don't enforce regular password expiry"): regular password changing harms rather than improves security;
  use MFA, monitor logins and lock inactive accounts instead; users must still change a password known or suspected to
  be compromised. It also prefers throttling over lockout, and if locking out suggests 5 to 10 attempts first.
- Microsoft 365 admin guidance: discourages expiry for cloud-only accounts (recommended setting: never expire),
  recommends a 14-character minimum, banning easy-to-guess passwords, enforcing MFA registration, and notes that
  length, special-character and change requirements lead to password normalisation.

## Making the case
1. Show the current policy line by line next to the NIST row it contradicts.
2. Explain the human cost with the NCSC point that users pick minor variations of the old password, and the Microsoft
   point that rules normalise passwords.
3. Propose the replacement: a long minimum length, a blocklist check on set and change (Microsoft offers Entra Password
   Protection), no expiry, MFA registration, password-manager and paste support.
4. Compliance: cite the exact requirement your auditor works from; this skill does not state what other frameworks
   permit.

## Gotchas
- SP 800-63 addresses digital authentication to systems over a network, with requirements aimed at federal use
  (agencies, FIPS 140). Elsewhere it is persuasive best practice: quote it as such.
- Keep a change trigger for real compromise (breach alert, leaked credentials).

## Checked
Confirmed 2026-11-08 against NIST SP 800-63B-4 (section 3.1.1 password requirements, rate limiting section 3.2.2,
Appendix A), the NCSC password guidance and the Microsoft 365 password policy recommendations. Removed: the "(2025)"
date, the PCI DSS 4.0 claim, the HIBP integration, the passkeys/SSO suggestion, and the statement that NIST is binding
only for US federal systems (replaced with what the page's scope says).
Method: docs-only read of cited pages, 2026-11-08
