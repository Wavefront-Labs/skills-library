---
id: computing-software.cloud-infrastructure-engineering.openbao.token-types
name: token-types
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, token, service-token, batch-token, orphan]
level: practitioner
status: docs-checked
description: "Choose between OpenBao service, batch, root, periodic and orphan tokens, their prefixes, and how each is created."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/tokens.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token types

- **Service**: all features (renewal, revocation, child tokens); heavyweight to create and track.
- **Batch**: encrypted blobs needing no disk storage, so lightweight, but lacking most service-token features.
- **Root**: carries the `root` policy, can do anything, may never expire. Created only from the initial token at `bao operator init`, from another root token (an expiring root cannot make a non-expiring one), or with `bao operator generate-root` and a quorum of unseal key holders.
- **Periodic**: made by `root`/`sudo` users, token store roles, or auth methods such as AppRole. Each renewal resets the TTL to the period, so it lives while renewed.
- **Orphan**: no parent, so revoking another token does not revoke it. Create via `auth/token/create-orphan`, `auth/token/create` with `no_parent` set to `true`, token store roles, or logging in with a non-`token` auth method.

## Prefixes

`s.` service, `b.` batch, `r.` recovery; body is 24+ Base62 characters (`[sbr]\.[a-zA-Z0-9]{24,}`).

## Gotchas

- Token structure is volatile and opaque; do not write scripts that parse tokens.
- Guard root tokens, use them only for minimal setup or emergencies, and revoke them right after.
- The token store (`token` auth backend) cannot be disabled and has no login capability.

## Checked

2026-11-04. Read the OpenBao tokens concepts page in full. Confirmed: service and batch descriptions, the three ways to create root tokens, periodic token creation routes, orphan token routes, prefixes and the body regexp, the opaque structure warning and the token store notes. Removed: nothing.
Method: documentation only; no commands were run.
