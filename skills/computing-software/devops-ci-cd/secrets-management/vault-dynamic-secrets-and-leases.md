---
id: computing-software.devops-ci-cd.secrets-management.vault-dynamic-secrets-and-leases
name: vault-dynamic-secrets-and-leases
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, vault, hashicorp-vault, openbao, dynamic-secrets, leases, lease-renewal, lease-revocation, ttl, max-ttl, database-secrets-engine, postgresql, mysql, creation-statements, revocation-statements, static-roles, rotate-root, aws-secrets-engine, assumed-role, vault-agent, auto-auth, vault-agent-injector, vault-secrets-operator, vaultdynamicsecret, kubernetes-auth, object-ownership]
level: advanced
status: gated
description: "Issue per-workload, short-lived credentials from Vault/OpenBao: database and AWS engines, TTL and lease sizing, renewal via Vault Agent or VSO, revocation, and the Postgres object-ownership trap."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/databases", "https://developer.hashicorp.com/vault/docs/concepts/lease", "https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent", "https://developer.hashicorp.com/vault/docs/platform/k8s/vso", "https://openbao.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault dynamic secrets and leases

**Goal:** every workload gets its own database/cloud credential, created on demand, valid
for hours, revoked automatically — so there is nothing long-lived to rotate or leak.

Commands use the `vault` CLI; OpenBao's `bao` CLI is compatible for these paths
(*verify per release*). Sections 1-3 were run on Vault 2.2.0 dev mode with PostgreSQL 17.10; sections 4-6 (Agent, Kubernetes, AWS, operations) are unrun (gated: unconfirmed, no cluster or cloud account). Static secrets and rotation patterns:
`computing-software.devops-ci-cd.secrets-management.secret-rotation-and-lifecycle`.

## 1. Database secrets engine (PostgreSQL example)
```bash
vault secrets enable database
vault write database/config/orders \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@<db-host>:5432/orders" \
  username="vault_admin" password="<BOOTSTRAP_PASSWORD>" \
  allowed_roles="orders-app"
vault write -force database/rotate-root/orders   # now only Vault knows the admin password (run: the bootstrap password was rejected afterwards)

vault write database/roles/orders-app db_name=orders \
  default_ttl=1h max_ttl=24h \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' IN ROLE orders_rw;"
vault read database/creds/orders-app     # → username, password, lease_id, lease_duration
```
- PostgreSQL 16+: `IN ROLE orders_rw` fails with `permission denied to grant role "orders_rw"` unless the admin role holds it with admin option:
  `GRANT orders_rw TO vault_admin WITH ADMIN OPTION;` (and the admin role needs `CREATEROLE`). Run: after that grant, `vault read database/creds/orders-app`
  returned a username like `v-token-orders-a-...`, lease 1h renewable, role `VALID UNTIL` set.
- Grant privileges via a **group role** (`IN ROLE orders_rw`), not per-table grants in
  `creation_statements` — simpler and survives schema changes.
- `rotate-root` means a lost Vault = lost admin access; keep a break-glass path.

## 2. The object-ownership trap
Objects created by a dynamic user (tables via migrations, temp objects) are owned by that
user. Run on PG 17.10: with the default revocation statements the lease revoke printed "queued successfully" but the role stayed and Vault logged
`permission denied for table <t>` and retried with backoff (the admin role cannot clean up objects it has no rights on). Fixes:
- Run migrations as a **static** owner role, not a dynamic one; or
- In `creation_statements`, `IN ROLE orders_rw, orders_owner` plus `ALTER ROLE "{{name}}" SET role = orders_owner;` so objects are
  owned by the shared role (run: `ALTER ROLE ... SET role` alone did NOT work, the table stayed owned by the dynamic user; with membership the table was owned by
  `orders_owner`; the admin role needed `GRANT orders_owner TO vault_admin WITH ADMIN OPTION`); and/or
- Custom `revocation_statements`: `REASSIGN OWNED BY "{{name}}" TO orders_owner;
  DROP OWNED BY "{{name}}"; DROP ROLE IF EXISTS "{{name}}";` (run: failed with `permission denied to reassign objects` until the creation statements also ran
  `GRANT "{{name}}" TO vault_admin;` with `vault_admin` a member of `orders_owner`; then the role was dropped and the table moved to `orders_owner`).
Also: dropping a role with open sessions fails; terminate them (`pg_terminate_backend`)
in revocation if you need hard cutoff (*test against your PG version*).

## 3. Leases and TTL sizing
Every dynamic secret has a **lease**: `default_ttl` (initial), renewable up to `max_ttl`.
- `vault lease renew <lease_id>`; `vault lease revoke <lease_id>` (lookup then shows `ttl 0s`);
  incident lever (accepted, "queued successfully"): `vault lease revoke -prefix database/creds/orders-app` kills every
  credential of that role at once.
- **TTL too short** → apps hammer Vault and fail when Vault blips.
  **Too long** → credentials outlive pods (orphans) and blast radius grows.
  Starting point: `default_ttl` ≈ a few × the renewal interval, `max_ttl` ≈ a working day.
- **Lease explosion:** a credential per request or per short-lived job, with long TTLs,
  creates hundreds of thousands of leases and slows Vault and the DB (role churn). Cache
  per process; set TTLs close to job duration; revoke on exit.
- Connection pools: set max connection lifetime below credential TTL so pools reconnect
  with fresh credentials before the role expires.

## 4. Getting credentials into workloads
- **Vault Agent** (sidecar or daemon): `auto_auth` (Kubernetes, AWS IAM, AppRole), renews
  leases, renders files via templates, can run a command on change
  (`exec`/template `command` to reload the app).
- **Kubernetes:** Vault Agent Injector (pod annotations
  `vault.hashicorp.com/agent-inject-secret-db: database/creds/orders-app`) or the
  **Vault Secrets Operator** `VaultDynamicSecret` CR, which syncs into a Kubernetes Secret
  and can trigger rollout restarts on renewal/rotation.
- Auth: Kubernetes auth bound to **service account + namespace**; never a shared token.
- App-native: SDKs can read and renew directly — more control, more code.

## 5. Other engines worth knowing
- **AWS:** `credential_type=assumed_role` (STS, short-lived, no IAM user churn) is
  preferable to `iam_user` (real IAM users, eventual-consistency delays of seconds before
  usable, IAM limits). `federation_token` for narrower sessions.
- **Static roles** (`database/static-roles/...`): Vault rotates an existing account's
  password on a schedule — for legacy apps that can't handle changing usernames.
- PKI engine for short-lived TLS certs follows the same lease thinking.

## 6. Operating it
- Audit device enabled (who read which creds) — required for incident forensics.
- Monitor: lease count by mount, revocation failures, DB role count.
- Plan for Vault unavailability: existing creds keep working until TTL; Vault HA +
  performance standbys; apps should back off, not crash-loop.

## Verify
- [ ] Two pods of the same app hold different DB usernames (`SELECT usename FROM pg_stat_activity`).
- [ ] Killing a pod leads to its credential being revoked or expiring within TTL; no orphan roles accumulate.
- [ ] `revoke -prefix` was rehearsed and the app recovered by fetching new creds.
- [ ] Revocation succeeds for users that ran migrations (ownership handled).
- [ ] Lease count is stable over a week, not growing.
