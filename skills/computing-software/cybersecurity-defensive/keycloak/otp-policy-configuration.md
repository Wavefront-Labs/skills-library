---
id: computing-software.cybersecurity-defensive.keycloak.otp-policy-configuration
name: otp-policy-configuration
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, otp, totp, hotp, otp-policy]
level: practitioner
status: docs-checked
description: "Choose TOTP or HOTP and set algorithm, digits, look-around window, period and reusable code in the Keycloak OTP policy."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/otp-policies.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# otp policy configuration
OTP policy lives under *Authentication* > *Policy* tab > *OTP Policy* tab. Keycloak builds the QR code on the OTP set-up page from it, and FreeOTP and Google Authenticator scan that code.

Type: **TOTP** (time based) hashes the current time and a shared secret; the server compares hashes within a window of time, so a code is valid only briefly. **HOTP** (counter based) uses a shared counter that the server increments on each successful OTP login, so valid OTPs change after a login and an OTP stays valid for an indeterminate time. The docs call TOTP more secure and HOTP more user-friendly (no time limit to type the code). HOTP needs a database update every time the counter increments, a performance drain under heavy load. TOTP does not remember used codes, so no database update is needed, but a TOTP can be reused inside its valid interval.

TOTP options:
- OTP hash algorithm: default SHA1; SHA256 and SHA512 are the more secure options.
- Number of digits: short is easier to type, longer is more secure.
- Look around window: number of intervals the server tries to match, to cover clock drift. Default 1. With a 30 second period, 1 accepts a 90 second window (period plus 30 s look ahead plus 30 s look behind); each increment adds 60 seconds.
- OTP token period: seconds the server matches a hash; a new TOTP is generated each interval.
- Reusable code: whether a token may be reused or the user must wait for the next one. Not reusable by default; an administrator must explicitly allow reuse.

HOTP options: OTP hash algorithm (default SHA1, SHA256 and SHA512), Number of digits, Look around window (previous and following intervals, covers the user's counter getting ahead of the server; default 1) and Initial counter.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/otp-policies.adoc: navigation, TOTP vs HOTP trade-offs, every option, the defaults and the 90 second window arithmetic. Removed: app-compatibility and large-window gotchas, "confirm in your version" hedge and the invented Verify step.
Method: documentation only; no commands were run.
