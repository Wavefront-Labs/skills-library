---
id: computing-software.cybersecurity-defensive.identity-access-management.totp
name: totp
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [totp, push-notification-mfa, number-matching, microsoft-authenticator, oath-tokens, rfc-6238]
level: practitioner
status: docs-checked
description: "Manage TOTP and push authenticators: RFC 6238 validation rules, Entra number matching, OATH hardware token support and drift handling, and recovery gotchas."
sources: ["https://datatracker.ietf.org/doc/html/rfc6238", "https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-number-match", "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-oath-tokens"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TOTP and push authenticator management

## TOTP (RFC 6238)
- RFC 6238 recommends a default time step of 30 seconds, a balance between security and usability. A larger step widens the window in which a leaked code can be used.
- The validator should allow for transmission delay, but the RFC recommends at most one time step of delay.
- The verifier must not accept a second attempt of an OTP after the first one validated successfully: one-time use.
- The RFC defines TOTP on HMAC with SHA-1 as the hash by default.

## Microsoft Entra specifics
- Entra supports OATH TOTP only; it does not support OATH HOTP.
- Hardware OATH tokens (preview): SHA-1 and SHA-256 tokens refreshing every 30 or 60 seconds. Entra adjusts time drift at activation and at every sign-in (30 s tokens: +/- 1 day at activation, +/- 1 minute at authentication; 60 s tokens: +/- 2 days and +/- 2 minutes).
- Number matching is enabled for all Authenticator push notifications and users cannot opt out. It applies to MFA, SSPR and combined registration. Users whose default method is not Authenticator push see no change.
- Wearables (Apple Watch, Android wearables) do not support number matching; users approve on the phone.
- Older Authenticator versions without number matching cannot authenticate and must be upgraded.
- Hardware OATH token management in the preview refresh is via Microsoft Graph only; the page lists the Authentication Policy Administrator role for inventory tasks.

## Gotchas
- Users losing phones: recovery path is a help-desk identity check, not "read me your code".
- SMS fallback undermines app-based MFA; disable it (see sms-mfa-deprecation).

## Verify
- [ ] Number matching active for all push users.
- [ ] Verifier rejects a second use of an already-accepted code.

## Checked
2026-11-01. Confirmed against RFC 6238 (section 5.2 time step, delay, one-time use; HMAC-SHA-1), the Entra number matching page and the Entra OATH tokens page. Removed: Okta/Duo behaviour, denial-count limits, application name/location in prompts, fraud alert behaviour, CSV upload steps, encrypt-at-rest and QR enrolment advice, and the phishing-resistance claims (CISA fact sheet returned 403, not read).
Method: documentation only; no commands were run.
