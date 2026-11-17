---
id: computing-software.cloud-infrastructure-engineering.openbao.token-ttl-and-accessors
name: token-ttl-and-accessors
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, ttl, max-ttl, accessor, token-renew]
level: practitioner
status: docs-checked
description: "How OpenBao token TTLs and max TTLs are computed, how renewal works, and what token accessors can and cannot do."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/tokens.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token TTLs and accessors

## TTL rules

- A non-root token's TTL runs from creation or last renewal, whichever is later. At expiry the token and its leases are revoked.
- Maximum TTL comes from the system max (32 days by default, configurable), any mount-tuned max TTL, and the auth method's suggestion, which cannot exceed the mount or system max. It is recomputed at each renewal, so it can change.
- An **explicit max TTL** is a hard limit, even for periodic tokens. A periodic token with one is revoked when it is reached.
- Token store roles: the role's current period applies at renewal time.
- OpenBao does not revoke a token before its returned TTL except by direct operator action.

```
bao token renew
```

## Accessors

An accessor references a token without being the token. With the right permissions it can: look up properties (not the ID), look up capabilities on a path, renew, or revoke. A common use is storing an accessor beside a job ID so the token and its leases can be revoked when the job finishes.

## Warnings

- Listing accessors (`auth/token/accessors`) is dangerous: they can be used to revoke all tokens.
- `auth/token/revoke-orphan` revokes a token and orphans its children instead of revoking the tree; use with caution.
- Audit logs that do not obfuscate accessors enable emergency revocation but also large-scale denial of service.

## Checked

2026-11-04. Read the OpenBao tokens concepts page in full. Confirmed: TTL since creation or last renewal, the 32 day system max and the three max TTL inputs, explicit max TTL as a hard limit, periodic role period at renewal time, `bao token renew`, the four accessor actions, the accessor workflow example and the accessor listing, revoke-orphan and audit obfuscation warnings. Removed: nothing.
Method: documentation only; no commands were run.
