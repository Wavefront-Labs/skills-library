---
id: computing-software.rpa-and-low-code.n8n.require-two-factor-auth
name: require-two-factor-auth
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, 2fa, mfa, authenticator, recovery-codes, n8n-mfa-enabled]
level: intro
status: docs-checked
description: "Enable two-factor authentication on an n8n account with an authenticator app, save recovery codes, and disable it instance-wide with N8N_MFA_ENABLED."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/verify-user-identity/require-two-factor-auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add an authenticator-app second factor to n8n accounts. You need an authenticator app on your phone.

## Enable
1. **Settings > Personal**, select **Enable 2FA**; a modal shows a QR code.
2. Scan it with the authenticator app.
3. Enter the code in **Code from authenticator app**, select **Continue**.
4. n8n shows recovery codes. Save them: they are the only way back in if you lose the authenticator.

## Disable instance-wide (self-hosted)
Set `N8N_MFA_ENABLED` to `false` to disable 2FA for all users. n8n ignores this if existing users already have 2FA enabled.

Related: identity can also be verified through LDAP, SAML or OIDC.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Require two-factor authentication" page (docs.n8n.io, read in full).
Removed as not on that page: the claim about log streaming audit events covering 2FA and MFA changes.
