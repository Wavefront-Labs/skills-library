---
id: computing-software.systems-network-administration.home-assistant.mfa-totp
name: mfa-totp
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [totp, auth-mfa-modules, authenticator]
level: practitioner
status: docs-checked
description: "Enable TOTP multi-factor authentication in Home Assistant with auth_mfa_modules, enrol an authenticator app, and know it works with any auth provider."
sources:
  - https://www.home-assistant.io/docs/authentication/multi-factor-auth/
  - https://www.home-assistant.io/docs/authentication/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: require a six-digit one-time code after the password.

MFA can be combined with any authentication provider, except that it does not take part in login when the trusted networks provider is used. If several MFA modules are enabled, you pick one at login.

Enable the module in configuration.yaml:

```yaml
homeassistant:
  auth_mfa_modules:
    - type: totp
```

If no `auth_mfa_modules` section exists, a TOTP module named Authenticator app is loaded automatically.

Enrol an account:

1. Restart Home Assistant.
2. Open User profile > Security.
3. In Multi-factor authentication modules, select Enable. A new secret key is generated.
4. In your phone authenticator app (Google Authenticator or Authy are recommended), scan the QR code or type the key.
5. The app shows a new six-digit code about every thirty seconds. Enter one under the QR code in the Code field.

Home Assistant and the app are now in sync.

Treat the secret key like a password and never expose it. TOTP works because Home Assistant knows the secret and can compute the expected code.

Turn MFA off for your account from the same Security page.

## Checked

2026-11-04. Confirmed against the Multi-factor authentication page and the Authentication providers page (trusted_networks exception). Nothing removed.

Method: documentation only; no commands were run.
