---
id: computing-software.cloud-infrastructure-engineering.openbao.approle-auth
name: approle-auth
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, approle, secret-id, role-id, machine-auth]
level: practitioner
status: docs-checked
description: "Set up OpenBao AppRole for machines: role TTLs, RoleID and SecretID, pull vs push mode, wrapped SecretID delivery and lockout."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/auth/approle.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppRole auth

```
bao auth enable approle
bao write auth/approle/role/my-role \
    secret_id_ttl=10m \
    token_num_uses=10 \
    token_ttl=20m \
    token_max_ttl=30m \
    secret_id_num_uses=40
bao read auth/approle/role/my-role/role-id
bao write -f auth/approle/role/my-role/secret-id
```

## Settings

- `secret_id_ttl`, `secret_id_num_uses`: SecretID lifetime and login count
- `token_ttl`, `token_max_ttl`, `token_num_uses`: issued token limits
- `bind_secret_id`: default requires a SecretID; turning it off is advanced
- A token that must create child tokens needs `token_num_uses` set to 0.

## Pull vs push

- **Pull** (recommended): the role generates a random SecretID. The RoleID can be shared; keep the SecretID confidential to the final client.
- **Push**: a client supplies a custom SecretID, mainly for compatibility with the deprecated App-ID workflow. Less secure, since another system must know both IDs.

## Delivery

Deliver the SecretID by response wrapping: a trusted orchestrator hands the app a short-lived wrapping token so the app never sees the raw SecretID in transit (see response-wrapping).

## Lockout

User lockout is on by default (5 failures, 15 minutes); supported for userpass, ldap and approle only (see user-lockout).

## Checked

2026-11-04. Confirmed against the AppRole auth method page: the example commands and values, the token_num_uses 0 note for child tokens, bind_secret_id, pull and push modes, response wrapping and the lockout defaults. Nothing removed.

Method: documentation only; no commands were run.
