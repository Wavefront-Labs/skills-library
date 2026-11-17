---
id: computing-software.devops-ci-cd.secrets-management.database-password-rotation-without-downtime
name: database-password-rotation-without-downtime
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, database-password-rotation, secret-rotation, dual-secret]
level: advanced
status: docs-checked
description: "Rotate database passwords without outages: Vault dynamic and static roles, AWS rotation stages and cloned users, root credential pitfalls."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html", "https://developer.hashicorp.com/vault/docs/secrets/databases", "https://www.postgresql.org/docs/current/sql-alterrole.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database password rotation without downtime

Changing a password in place breaks every connection that re-authenticates before it receives the new value. Prefer dynamic credentials, or an arrangement in which the old credential stays valid until consumers have the new one.

## Dynamic credentials (Vault database secrets engine)
- Dynamic roles generate credentials per request from `creation_statements`, with a lease. Role defaults: TTL 1 hour and max TTL 24 hours. Every service gets unique credentials, so questionable access can be traced to a service instance by SQL username. Vault's revocation system makes users invalid within a reasonable time of lease expiry.
- Configure a role: `vault write database/roles/my-role db_name=my-database creation_statements="..." default_ttl="1h" max_ttl="24h"`, then `vault read database/creds/my-role` returns `username`, `password`, `lease_id`, `lease_duration` and `lease_renewable`. `{{username}}` and `{{password}}` are filled in by the plugin; `{{expiration}}` is supported by some plugins only.
- As of Vault 1.6 all database plugins support dynamic and static roles; all except MongoDB Atlas support rotating the root user's credentials.

## Static roles
A static role maps one Vault role to one existing database user. Vault stores and automatically rotates that user's password on a rotation period (default 24 hours) or schedule, and returns the current password when asked. Onboarding a user rotates its password immediately, unless `skip_import_rotation` (or the config-level `skip_static_role_import_rotation`) is set. Anyone with the Vault policy can access that database account. A static role has one valid password at a time, so consumers must re-fetch.

## Root credential pitfall
Create a dedicated database user for Vault and rotate it with `vault write -force database/rotate-root/my-database` so nobody else holds it. Never assign the root credentials Vault uses in `config/` to a static role: Vault does not distinguish them, and after rotation the dynamic and static users managed by that configuration will fail.

## AWS Secrets Manager rotation
The Lambda rotation function stores a new value as `AWSPENDING`, sets it in the database, tests it, then moves `AWSCURRENT` to it, leaving the previous version as `AWSPREVIOUS`. For RDS MySQL the alternating-users strategy creates a cloned user (name suffix `_clone`, so keep the original name to 26 characters or less on MySQL 5.7+). Cloned users copy the first user's runtime configuration parameters; changing granted attributes needs code changes in `set_secret`. Before changing a credential, the function must check `AWSCURRENT` is valid and that `AWSCURRENT` and `AWSPENDING` target the same user and host. Stage details are in `computing-software.devops-ci-cd.secrets-management.secret-rotation-and-lifecycle`.

## Changing a PostgreSQL password
`ALTER ROLE name WITH PASSWORD '...'` sets a new password; `VALID UNTIL 'timestamp'` sets a password expiry (`'infinity'` means never).

## Verify
- [ ] After rotation, applications authenticate with the new credential and logs show no auth errors.
- [ ] Vault `rotate-root` has been run for the Vault management user and that user is not in a static role.

## Checked
Method: docs-checked 2026-11-09 against the Vault database secrets engine page (read to the capabilities table), the AWS Lambda rotation functions page (four steps and tips), and the PostgreSQL ALTER ROLE page (password and VALID UNTIL syntax). The AWS alternating-users page returned no content.
Removed as unconfirmed: the generic two-user (`app_a` / `app_b`) procedure and the claim that AWS implements exactly it, the PostgreSQL `CREATE ROLE ... VALID UNTIL` Vault statement example, Vault Agent lease renewal and reconnect behaviour, HikariCP `maxLifetime`, ESO plus Reloader advice, and the `pg_stat_activity` verification check.
