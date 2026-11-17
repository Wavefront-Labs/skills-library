---
id: computing-software.cybersecurity-defensive.authelia.webauthn-passkeys-and-selection
name: webauthn-passkeys-and-selection
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, webauthn, passkeys, fido2, security-key, user-verification, attestation]
level: advanced
status: docs-checked
description: "Configure Authelia WebAuthn registration and login, passkey login, attestation conveyance, authenticator selection criteria and what remains experimental."
sources:
  - https://www.authelia.com/configuration/second-factor/webauthn/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
webauthn:
  disable: false
  enable_passkey_login: false
  display_name: 'Authelia'
  attestation_conveyance_preference: 'indirect'
  timeout: '60 seconds'
  selection_criteria:
    attachment: ''
    discoverability: 'preferred'
    user_verification: 'preferred'
```

- `enable_passkey_login` allows a Passkey instead of a username and password. It counts as one factor only, so a request needing multi-factor still prompts for the password by default. It also depends on remembered sessions.
- `attestation_conveyance_preference` is `none`, `indirect` (the client may anonymise through a third-party CA) or `direct` (attestation signed by the authenticator). Conveyance lets the server see the AAGUID, which identifies the authenticator model.
- `selection_criteria.attachment`: empty lets the user choose; `cross-platform` means roaming keys; `platform` means built-in authenticators such as Windows Hello.
- `discoverability` and `user_verification` take `discouraged`, `preferred` or `required` (default `preferred`). Required discoverability may error if the authenticator is not discoverable; required user verification fails if the authenticator does not support it.
- `experimental_enable_passkey_uv_two_factors` and `experimental_enable_passkey_upgrade` are explicitly unsupported and expected to be replaced or removed.

Check: register a platform authenticator, sign out, and sign in with the passkey option.

## Checked

2026-11-08. Read the full Authelia WebAuthn page. Confirmed enable_passkey_login (single factor, password prompt), the attestation conveyance values, selection_criteria options and defaults, and the two unsupported experimental options. Tightened the discoverability and user_verification wording to match the page.

Method: documentation only; no commands were run.
