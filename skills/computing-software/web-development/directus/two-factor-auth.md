---
id: computing-software.web-development.directus.two-factor-auth
name: two-factor-auth
category: computing-software
field: web-development
product: directus
tags: [two-factor-auth, tfa-generate, require-2fa, otp-enable]
level: practitioner
status: docs-checked
description: "Set up Directus two-factor authentication via the tfa generate, enable and disable endpoints and enforce it with a policy's Require 2FA toggle."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/5.2fa.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enforce: turn on **Require 2FA** on a policy. It applies if any of the user's policies has it. With an IP allowlist, 2FA is required only from allowed IPs. Users without 2FA are sent to set it up after login, including after SSO.

API steps (as the logged-in user):
1. `POST /users/me/tfa/generate` with `{ "password": "..." }`. The response has `secret` and `otpauth_url` (renderable as a QR code).
2. Save the secret in an authenticator app.
3. `POST /users/me/tfa/enable` with `{ "otp": "123456", "secret": "<secret>" }`.
4. From now on, include `otp` when logging in via the Studio or API.

Disable: `POST /users/me/tfa/disable` with `{ "otp": "123456" }`.

Gotcha: you need an authenticator app or a password manager with OTP support.

## Checked

2026-11-04: Require 2FA policy behaviour, IP allowlist and SSO redirect notes, the generate, enable and disable endpoints with their bodies, and the authenticator app requirement confirmed against the Directus Two-Factor Authentication page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
