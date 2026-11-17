---
id: computing-software.devops-ci-cd.verdaccio.legacy-token-signature-and-env-key
name: legacy-token-signature-and-env-key
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [legacy-token, aes-256-ctr, token-encryption, legacy-signature, verdaccio-legacy-encryption-key, aes]
level: advanced
status: docs-checked
description: "How legacy bearer tokens are encrypted and the VERDACCIO_LEGACY_ALGORITHM and VERDACCIO_LEGACY_ENCRYPTION_KEY variables for keeping old tokens working."
sources:
  - https://verdaccio.org/docs/env/
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Legacy tokens (pre-JWT npm bearer tokens, handled by `@verdaccio/signature`) use AES with `aes-256-ctr` and the server secret. They are not designed to expire. The legacy signature applies to the API only; the web UI uses JWT.

Environment variables:
- `VERDACCIO_LEGACY_ALGORITHM`: cipher name; default `aes-256-ctr`. Any value must be supported by your Node.js/OpenSSL build (`crypto.getCiphers()`). Unrelated to storage encryption.
- `VERDACCIO_LEGACY_ENCRYPTION_KEY`: overrides the key for legacy tokens only. Must be exactly 32 characters (256 bits) or encryption fails with `Invalid secret key length`. When unset, the 32-character secret in `.verdaccio-db.json` is used.

Use case: keep decrypting tokens issued under a previous secret after the stored secret changed.

```yaml
security:
  api:
    legacy: true   # default
```
Gotchas:
- The same key also protects two-factor records (rotating it locks enrolled users out, see two-factor-ci-and-lockout).

## Checked

2026-11-04. Confirmed against the Environment Variables, Configuration, Two-Factor Authentication and Best Practices pages (aes-256-ctr default, legacy tokens never expire, API-only legacy signature, both variables, 32-character key error, security.api.legacy default, two-factor records and secret rotation). Removed: the unsupported strict-length-on-every-version note and the closing Verify tip.
Method: documentation only; no commands were run.
