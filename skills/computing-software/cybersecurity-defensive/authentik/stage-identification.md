---
id: computing-software.cybersecurity-defensive.authentik.stage-identification
name: stage-identification
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, identification-stage, user-fields, passkey-autofill, sources, pretend-user-exists]
level: practitioner
status: docs-checked
description: "Configure the authentik Identification stage: user fields, embedded password and CAPTCHA, sources, remember me, pretend user exists, and WebAuthn passkey autofill."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/identification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: the first step of most login and recovery flows, where the user identifies themselves.

## Options
- **User Fields**: Username, Email, UPN (matches the `upn` attribute, commonly filled by an LDAP source). With none selected the stage is a source-only entry point; if exactly one source exists and no **Passwordless flow** is set, authentik can redirect to it automatically.
- **Password stage** and **Captcha stage**: render inline in the identification step. Do not also bind the same stage separately in the flow. Configure the CAPTCHA for invisible/background use so it renders inside the form.
- **WebAuthn Authenticator Validation Stage**: used for passkey autofill.
- **Case-insensitive matching**: match identifiers regardless of case.
- **Show matched user**, **Pretend user exists** (continue for an unknown identifier if the format is valid; Password and Email stages handle the synthetic user), **Enable remember me on this device** (user can pick **Not you?**).
- **Enrollment flow**, **Recovery flow**, **Passwordless flow**: links below the form.
- **Sources** (OAuth or SAML), **Show source labels**; sources marked **Promoted** show as full-width buttons.

## Passkey autofill (WebAuthn conditional UI)
1. Create or edit an Authenticator Validation stage allowing the **WebAuthn** device class.
2. Set the Identification stage's **WebAuthn Authenticator Validation Stage** to it.
3. Users need an enrolled discoverable credential (resident key) created for the same hostname.

Requirements: HTTPS (except localhost), a browser supporting conditional mediation. Troubleshooting: the prompt normally appears when the username field is focused; the login page must not be in an iframe; if it falls back to password, check the validation stage allows WebAuthn and the user has a valid authenticator. In the default authentication flow an expression policy skips MFA after passkey login; adjust it if you still want a second factor.

## CAPTCHA gotcha
A passkey login completes the stage straight after the WebAuthn check and does not run a CAPTCHA configured on the stage, even an interactive one. Use reverse-proxy rate limiting for resource-consumption concerns.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/identification/.
Removed as not confirmed by that page: case-collision and unique-username policy claim.
Method: documentation only; no commands were run.
