---
id: computing-software.cybersecurity-defensive.zitadel.multifactor-options-and-force-mfa
name: multifactor-options-and-force-mfa
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, mfa, totp, u2f, otp, second-factor]
level: practitioner
status: docs-checked
description: "Choose which ZITADEL second factors and multifactors are allowed and require users to register one with Force MFA."
sources:
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the login settings you decide which factors users may use.

Multifactors: U2F with PIN, such as FaceID, Windows Hello, fingerprint or hardware tokens like a Yubikey. This is also what passkeys rely on.

Second factors (2FA):

- TOTP, from authenticator apps such as Google or Microsoft Authenticator or Authy
- U2F, such as FaceID, Windows Hello, fingerprint or hardware tokens
- One-time password by email
- One-time password by SMS

The option "Force MFA" makes users register and use a multifactor method; make sure you have added the methods you want to allow first. "Force MFA for local authenticated users" enforces the rule only for local authentication, not for users authenticated through an identity provider. Email OTP and SMS OTP presumably depend on a working SMTP or SMS provider.

The TOTP issuer name shown in authenticator apps defaults to ZITADEL. Self-hosted, set the environment variable `ZITADEL_SYSTEMDEFAULTS_MULTIFACTORS_OTP_ISSUER`; the page says the Helm value `SystemDefaults.Multifactors.Issuer` does not work. On ZITADEL Cloud it is not configurable.

For administrators, apply stricter settings in the dedicated instance-administrator organization, since login settings can be overridden per organization. Lockout settings, which cap failed password or OTP attempts, complement MFA and are also part of default settings.

## Checked

2026-11-08. Read the default settings page in full; removed a TOTP storage claim from another page, added the Force MFA local variant and TOTP issuer note.

Method: documentation only; no commands were run.
