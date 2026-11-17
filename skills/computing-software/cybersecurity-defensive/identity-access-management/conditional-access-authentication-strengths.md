---
id: computing-software.cybersecurity-defensive.identity-access-management.conditional-access-authentication-strengths
name: conditional-access-authentication-strengths
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [mfa, authentication-strength, conditional-access, phishing-resistant-mfa, entra-id, fido2, admin-protection]
level: practitioner
status: gated
description: "Require specific MFA methods with Entra authentication strengths: built-in and custom strengths, phishing-resistant MFA for admins, registration, and rollout without lockouts."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths", "https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-admin-phish-resistant-mfa", "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional Access authentication strengths

"Require MFA" accepts any registered method, including SMS and push that AiTM phishing kits defeat.
Authentication strengths let a policy demand specific methods.

## Built-in strengths
- **Multifactor authentication strength**: any MFA combination.
- **Passwordless MFA strength**: passwordless methods only (see the concept page for the exact list).
- **Phishing-resistant MFA strength**: phishing-resistant methods only; excludes push, OTP and SMS (see the concept page for the exact list).
Custom strengths: pick allowed combinations, and for FIDO2 restrict by AAGUID (specific key models).

## Policies
1. Admins: target directory roles (Global Admin, Privileged Role Admin, Security Admin, Exchange Admin...)
   -> all cloud apps -> Grant: Require authentication strength "Phishing-resistant MFA".
2. All users: "Multifactor authentication" strength baseline.
3. Sensitive apps (finance, HR, source code): phishing-resistant.
4. Security info registration: require a strong method or Temporary Access Pass to register new methods,
   so an attacker with a password cannot register their own authenticator.

## Rollout
- Report-only first; review the report-only results to see who would fail.
- Ensure users have registered qualifying methods: Authentication methods > User registration details;
  issue keys and Temporary Access Passes for bootstrap.
- Keep two break-glass accounts excluded (with FIDO2 keys stored securely) and monitored.
- External/guest users: authentication strength for B2B users depends on cross-tenant MFA trust settings.

## Interactions (gated: unconfirmed, source is paywalled or blocked)
- Authentication strength plus "Require MFA" in the same policy: use one or the other.
- Sign-in frequency and CAE still apply; users must re-auth with the strong method.
- Methods must also be enabled in Authentication methods policy, or users cannot satisfy the strength.

## Gotchas
- Mobile apps and older clients may not support FIDO2 in some flows; test Outlook, Teams, VPN, SSH tools.
- Certificate-based auth must be configured as multifactor (affinity bindings and policy rules) to count.
- Locking admins into keys without spare keys causes outages: issue two keys per admin.

## Verify
Sign in as a test admin with push MFA: blocked with "authentication strength" message; with a FIDO2 key:
allowed. Sign-in logs show "Authentication strength" requirement satisfied by the expected method.

## Checked

2026-10-28. Confirmed against the authentication strengths concept page and the phishing-resistant MFA CA policy page: three built-in strengths (Multifactor, Passwordless MFA, Phishing-resistant MFA), custom strengths with AAGUID restrictions, requiring a strength for admin roles. Gated: the interactions section (strength combined with Require MFA, methods enabled in the policy). Removed: exact method membership lists, Conditional Access insights workbook.

Method: documentation only; no commands were run.
