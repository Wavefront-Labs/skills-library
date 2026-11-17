---
id: computing-software.devops-ci-cd.semaphore-ui.task-jwt-server-config
name: task-jwt-server-config
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [jwt, jwks, openbao, vault, task-token, semaphore-ui]
level: advanced
status: docs-checked
description: "Enable Semaphore-issued task JWTs and the JWKS endpoint so tasks can authenticate to Vault or OpenBao without stored secrets."
sources:
  - https://semaphoreui.com/docs/admin-guide/security/jwt
  - https://semaphoreui.com/docs/user-guide/task-templates/jwt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Issue short-lived task JWTs

Goal: let a running task prove its identity to an external system.

Semaphore mints a short-lived JWT per task, signed with an ECDSA P-256 key and exposed to the task process as the `SEMAPHORE_JWT` environment variable. External systems verify it against the JWKS endpoint, so no pre-shared secret is needed.

Disabled by default. Enable in `config.json`:

```json
{
  "jwt": {
    "enabled": true,
    "issuer": "https://semaphore.example.com",
    "default_ttl": "1h",
    "max_ttl": "24h"
  }
}
```

- `jwt.enabled` false (default): no tokens and the JWKS endpoint returns 404.
- `jwt.issuer`: value of the `iss` claim; use a stable URL, external systems use it as a trust anchor.
- `jwt.default_ttl` (default `1h`) applies when a template does not override it; `jwt.max_ttl` (default `24h`) is the ceiling. Go-style durations.

JWKS: `GET /.well-known/jwks.json` returns the public key (`kty` EC, `crv` P-256, `alg` ES256, `use` sig).

Set `access_key_encryption` before enabling JWTs: the signing key is encrypted with it, generated on first start, and cannot be re-encrypted afterwards. The private key is stored in the Semaphore database.

Rotate: remove the `jwt_signing_key` row from the `option` table and restart; a fresh pair is created. This invalidates all issued tokens, so do it when no task is using one.

Per template (user guide): in the JWT section tick JWT enabled, set Audience (the `aud` claim, up to 32 entries) and an optional TTL that must not exceed `jwt.max_ttl`. Tokens carry `iss`, `aud`, `sub` (`task:<id>`), `iat`/`nbf`/`exp`, `jti`, `project_id`, `template_id` and `user_id` (omitted for scheduled and integration runs). Restrict consuming roles by `project_id` or `template_id`.

## Checked

2026-11-07. Read in full: the Task JWT issuance admin page (admin-guide/security/jwt.md) and the Task JWTs user-guide page (user-guide/task-templates/jwt.md, including its OpenBao walk-through, which this skill does not reproduce). Confirmed: ECDSA P-256, SEMAPHORE_JWT, the four jwt.* options and defaults, JWKS path and key fields, the access_key_encryption warning, rotation by deleting the jwt_signing_key option row, per-template Audience and TTL, and the claims table. Removed: the curl Verify step.
Method: documentation only; no commands were run.
