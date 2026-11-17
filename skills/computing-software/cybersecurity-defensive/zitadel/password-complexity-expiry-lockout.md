---
id: computing-software.cybersecurity-defensive.zitadel.password-complexity-expiry-lockout
name: password-complexity-expiry-lockout
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, password-policy, lockout, expiry, complexity]
level: practitioner
status: docs-checked
description: "Set ZITADEL password complexity, password expiry and lockout limits at instance or organization level."
sources:
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three separate policies shape password handling.

Password complexity properties: minimum length, has uppercase, has lowercase, has number, has symbol.

Password expiry properties: maximum validity in days and expiration warning after days. After expiration the user is prompted to change the password at the next authentication. ZITADEL does not warn or notify users about the expiry; read the setting and send the notification yourself.

Lockout has Maximum Password Attempts and Maximum OTP Attempts. When exceeded the account is locked and an administrator must unlock it in the Management Console. A value of 0 means the lockout does not trigger.

All three are found in default settings. Instance values are fallbacks, and an organization can override them. This matters for security: if instance administrators share an organization with organization administrators, those administrators can change complexity, expiry and lockout for the shared organization. The hardening guide therefore recommends a dedicated organization for instance administrators.

## Checked

2026-11-08. Read the default settings page in full; replaced invented advice with the listed properties, the no-notification note and the 0 lockout value.

Method: documentation only; no commands were run.
