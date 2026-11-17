---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-token-types-and-ttl
name: vault-token-types-and-ttl
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, token-types, batch-tokens, periodic-tokens]
level: practitioner
status: docs-checked
description: "Select service, batch or periodic Vault tokens, set TTLs and max TTLs, and understand revocation and orphan behaviour."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/tokens"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service tokens (`hvs.`) are stored, renewable and revocable. Batch tokens (`hvb.`) are lightweight, not stored, cannot be renewed or revoked individually, and cannot create children, which suits high-volume short jobs. Periodic tokens renew to a fixed period and can live indefinitely.

```sh
vault token create -policy=app -ttl=1h -explicit-max-ttl=24h
vault token create -policy=app -type=batch -ttl=10m
vault token create -policy=app -period=24h
vault token lookup -accessor <accessor>
vault token revoke -accessor <accessor>
```

Gotchas: revoking a parent revokes children and their leases; use orphan tokens when that is not wanted. The system max TTL defaults to 32 days. Tokens are opaque, so do not parse their contents. Use accessors for lookups and revocation to avoid handling the token value (batch tokens have no accessors). Root tokens can be set to never expire; the initial one should be revoked. A revoked or expired token gets a 403 with `invalid token` and `permission denied`.

## Checked

2026-11-03. Confirmed against the Vault tokens concepts page: `hvs.`/`hvb.` prefixes, opaque tokens, service vs batch comparison table, parent revocation and orphans, periodic tokens, explicit max TTL, 32-day system max TTL, root tokens, 403 error responses. Removed: an invented verify step and a generic tuning paragraph.

Method: documentation only; no commands were run.
