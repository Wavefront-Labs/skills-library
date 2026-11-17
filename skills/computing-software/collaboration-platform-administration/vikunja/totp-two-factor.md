---
id: computing-software.collaboration-platform-administration.vikunja.totp-two-factor
name: totp-two-factor
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, totp-enroll, no-recovery-codes, totp-caldav, totp-reenroll]
level: intro
status: docs-checked
description: "Set up, use, disable and recover from TOTP two-factor authentication on local Vikunja accounts, including the CalDAV effect and lack of recovery codes."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/help/two-factor-authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TOTP applies to local accounts only. With LDAP or OIDC login, the provider manages second factors.

Enable: Settings, Two Factor Authentication, Enroll, scan the QR (or type the secret), enter a code, Confirm. All sessions are logged out afterwards. From 2.6.0 the QR and secret are shown only during setup, so add every authenticator before confirming.

Sign in: password, then the current six-digit code. A code works once; signing in twice inside one 30-second window means waiting for the next code.

CalDAV: the account password stops working. Use a dedicated CalDAV token or an API token with CalDAV access permission.

Disable: Settings, Two Factor Authentication, Disable, confirm with the password. To change authenticator, disable and enroll again; that makes a new secret.

Recovery: Vikunja has no recovery codes. With a signed-in session and the password, disable and re-enroll. Otherwise contact the administrator of your Vikunja instance.

## Checked

2026-11-04. Confirmed against the Vikunja Two-factor authentication help page (help/two-factor-authentication): local accounts only, enrol steps, session logout, 2.6.0 QR visibility, single-use codes in a 30-second window, the CalDAV effect and alternatives, disable and re-enrol, and no recovery codes. Removed: the claim about how admins can fix a lockout, which the page does not state.

Method: documentation only; no commands were run.
