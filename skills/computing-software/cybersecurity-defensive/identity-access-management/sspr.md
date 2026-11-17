---
id: computing-software.cybersecurity-defensive.identity-access-management.sspr
name: sspr
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sspr, self-service-password-reset, password-writeback, authentication-methods, help-desk-reduction, account-recovery, password-policy]
level: practitioner
status: docs-checked
description: "Deploy self-service password reset securely: required methods, password writeback, registration, admin policy, abuse risks (SIM swap, help desk) and audit monitoring."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks", "https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback", "https://pages.nist.gov/800-63-4/sp800-63b.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-service password reset

## Entra SSPR configuration
- Enable for all users (or pilot group); **number of methods required = 2**.
- Methods: Microsoft Authenticator notification/code, email (personal); avoid security questions and SMS/voice where possible (SIM swap = password reset).
- Registration: require on sign-in (or via combined registration), and set how often users reconfirm their authentication info.
- Notifications: notify users on password reset; notify all admins when another admin resets.
- **Password writeback** (Entra Connect or Cloud Sync) for hybrid users so cloud resets update AD.
- Administrators use a separate, stricter policy automatically (two-gate policy).

## Integrations
- Windows sign-in screen "Reset password" link (configured through Intune or policy; see the SSPR Windows sign-in documentation) for remote users.
- Combine with Entra Password Protection so reset passwords are checked against banned lists.

## Risks
- Weak methods turn SSPR into an account takeover path; attackers register methods after phishing a password (protect registration - see mfa-registration).
- Help desk social engineering is the alternative path; strong caller verification (see mfa-reset-help-desk-verification).

## Monitoring
Audit logs: self-service password reset activity, password resets and security info registration events. Alert on resets followed by sign-ins from new countries, or bursts of resets.

## Verify
- [ ] Test reset from outside the network with two methods; writeback updates AD.
- [ ] No users rely on SMS-only for SSPR.

## Checked

2026-10-28. Confirmed against the SSPR how-it-works and policy pages: number of methods required (one or two), reconfirm authentication information setting, security questions only in the legacy SSPR policy, notify all admins when other admins reset, strong two-gate policy for admin roles. Removed: FIDO2 reset-method claim, 180-day reconfirm figure, AllowPasswordReset registry name, pwdLastSet, account-unlock claim, audit activity display names.

Method: documentation only; no commands were run.
