---
id: computing-software.cybersecurity-defensive.identity-access-management.mfa-registration
name: mfa-registration
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [mfa-registration, registration-campaign, temporary-access-pass, combined-registration, security-info-registration, mfa]
level: practitioner
status: docs-checked
description: "Secure MFA registration: Conditional Access on the registration action, Temporary Access Pass onboarding, registration campaigns, and detecting attacker-registered methods."
sources: ["https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-security-info-registration", "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass", "https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-registration-campaign", "https://www.cisa.gov/resources-tools/resources/implementing-phishing-resistant-mfa"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure MFA registration

The registration moment is the weakest point: whoever registers the first method owns the account.
Attackers with a phished password register their own authenticator ("MFA registration hijack").

## Controls
1. **Protect the registration action.** Entra Conditional Access with user action "Register security information": require trusted location or compliant device, or require MFA (which new users meet via TAP). Exclude nothing but break-glass.
2. **Onboard with Temporary Access Pass (TAP).** Help desk/HR issues a one-time or time-limited TAP after identity proofing; user signs in with TAP and registers a passkey/Authenticator. Create the TAP in the Entra admin center or through Microsoft Graph (`isUsableOnce`, `lifetimeInMinutes`).
3. **Registration campaign** (nudge) to move SMS users to Microsoft Authenticator/passkeys; set snooze limits.
4. **Detection:** alert on "User registered security info" from a new country/ASN, or within minutes of a risky sign-in, or methods added by admins outside the help desk process (audit log security info registration events).
5. Notify users by email when a method is added.

## Gotchas
- Allowing registration from anywhere with only a password means accounts never registered are trivially hijacked; find them with the authentication methods registration report and force onboarding.
- Users with existing MFA can register new methods after an MFA prompt - push fatigue or AiTM still lets attackers in; number matching and phishing-resistant methods reduce this.
- Combined registration may let users add phone numbers that become SSPR methods.

## Verify
- [ ] CA policy on "Register security information" enabled (not report-only).
- [ ] Registration report: % users with no method trending to zero.
- [ ] Alert rule for anomalous method registration tested.

## Checked

2026-10-28. Confirmed against the security info registration CA policy, Temporary Access Pass and registration campaign pages: 'Register security information' user action, TAP isUsableOnce and lifetimeInMinutes properties, registration campaign snooze settings. Removed: New-MgUserAuthenticationMethodTemporaryAccessPassMethod cmdlet name and audit activity display names (not found in the fetched pages).

Method: documentation only; no commands were run.
