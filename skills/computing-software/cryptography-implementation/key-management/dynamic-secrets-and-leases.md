---
id: computing-software.cryptography-implementation.key-management.dynamic-secrets-and-leases
name: dynamic-secrets-and-leases
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, secrets-managers, dynamic-secrets, vault-leases, hashicorp-vault, database-credentials, credential-rotation, openbao]
level: practitioner
status: docs-checked
description: "Replace static database and cloud credentials with Vault dynamic secrets: engine config, root rotation, TTLs, lease renewal and revocation, app reloads."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/databases", "https://developer.hashicorp.com/vault/docs/concepts/lease", "https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent/template"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic secrets and leases

Dynamic secrets are created on request, unique per client, and revoked
when their lease ends. A leaked credential is short-lived and traceable to
one consumer.

## Database engine

```bash
vault secrets enable database
vault write database/config/orders-pg plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/orders" \
  allowed_roles=orders-app username=vault_admin password="$BOOTSTRAP_PW"
vault write -f database/rotate-root/orders-pg      # now only Vault knows it

vault write database/roles/orders-app db_name=orders-pg default_ttl=1h max_ttl=24h \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
vault read database/creds/orders-app
```

The AWS secrets engine works the same way: revoking a lease deletes the access keys at AWS.

## Leases

- Every dynamic secret read returns a `lease_id`, a `lease_duration` (seconds) and a renewable flag.
- Lease IDs are prefixed with the path the secret came from, so a prefix can be revoked as a tree.
- `vault lease renew <lease_id>` asks for more time (`-increment` is measured from now, not from the end of the
  current TTL); the backend may ignore or cap the request, so inspect the returned lease. Then request a new secret.
- `vault lease revoke -prefix database/creds/orders-app` kills every
  credential from that role (incident response).

## Application side

- Use Vault Agent templates (or another Vault-aware injector) to fetch and
  renew; the app must reload credentials (connection pool reconnects with
  new creds before the old lease expires).
- Choose `default_ttl` longer than your longest transaction and pool
  connection lifetime; set pool max lifetime below the TTL.
- Plan for Vault outage: TTLs long enough to ride out a short outage.

## Pitfalls

- Forgetting `rotate-root`: the bootstrap password stays valid.
- Roles with `GRANT ALL`; grant least privilege in `creation_statements`.
- Huge numbers of DB roles from short TTLs without revocation statements (the role can carry custom revocation
  statements).

## Checked

2026-11-01. Confirmed against the Vault database secrets engine page (rotate-root recommended so the bootstrap
user is no longer accessible; role TTL and max TTL; creation, revocation and renew statements) and the lease page
(lease_id, increment semantics, backend may ignore the increment, prefix revocation, AWS keys deleted on revoke).
Removed: the list of other engines and the claim that renewal stops at `max_ttl`.

Method: documentation only; no commands were run.

## Verify

- [ ] Root credential rotated; nobody knows it.
- [ ] Revoking a lease drops the DB login within seconds.
- [ ] App survives credential rotation in a soak test.
