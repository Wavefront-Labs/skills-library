---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-lease-renew-revoke
name: vault-lease-renew-revoke
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, lease-management, lease-id, revoke-prefix]
level: practitioner
status: docs-checked
description: "Manage dynamic secret leases with vault lease renew, revoke and revoke -prefix, and recover quickly from leaked credentials."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/lease"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic secrets carry a `lease_id`; when it expires or is revoked, the credential is invalidated at the backend.

```sh
vault read database/creds/app           # returns lease_id
vault lease renew -increment=1h database/creds/app/<id>
vault lease lookup database/creds/app/<id>
vault lease revoke database/creds/app/<id>
vault lease revoke -prefix database/creds/app
```

Revoking a token revokes every lease created with it.

Gotchas: `-increment` is a request; the backend may cap it, so read the response. KV enforces no TTLs; its `lease_duration` is only a hint for how often consumers should check back. Prefix revocation is the incident response tool for a leaked role: it immediately invalidates all credentials under it, so applications must handle re-authentication and re-fetch.

## Checked

2026-11-03. Confirmed against the Vault lease concepts page (`lease_id`, renew with `-increment` as an advisory request from now, prefix revocation e.g. `vault lease revoke -prefix aws/`), the Vault tokens page (revoking a token revokes its leases) and the KV v1 page (`lease_duration` is a hint). Removed: database load advice, an invented verify step and a logging tip.

Method: documentation only; no commands were run.
