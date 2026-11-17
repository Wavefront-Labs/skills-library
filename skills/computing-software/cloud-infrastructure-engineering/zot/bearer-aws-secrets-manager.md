---
id: computing-software.cloud-infrastructure-engineering.zot.bearer-aws-secrets-manager
name: bearer-aws-secrets-manager
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, aws-secrets-manager, jwt-keys, key-rotation, kid-header, bearer-auth]
level: advanced
status: docs-checked
description: "Load Zot bearer JWT verification keys from AWS Secrets Manager: config keys, secret format, supported key types, IAM action and safe rotation steps."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inside `http.auth.bearer`:

```json
"awsSecretsManager": { "region": "us-east-1", "secretName": "zot/jwt-verification-keys", "refreshInterval": "5m" }
```

- `region`: required. `secretName`: required (name or ARN). `refreshInterval`: optional, default `1m`.
- `cert` and `awsSecretsManager` are mutually exclusive; Zot refuses to start if both are set.
- The secret is a JSON object mapping `kid` values to either a PEM public key or a single-key JWKS string.
- Key types: Ed25519 (EdDSA), RSA (`RS*`/`PS*`), ECDSA (`ES*`).
- JWTs must include a `kid` header matching a key in the secret.
- Credentials use the default AWS chain (environment variables, shared credentials file, IAM roles, web identity/IRSA).
- Required IAM action: `secretsmanager:GetSecretValue` on the specific secret ARN.

Rotation:
1. Add the new key to the secret.
2. Switch the token issuer to the new key.
3. Wait for `refreshInterval`.
4. Remove the old key.

## Checked

2026-11-04. Read against the zot authn-authz article (AWS Secrets Manager section); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
