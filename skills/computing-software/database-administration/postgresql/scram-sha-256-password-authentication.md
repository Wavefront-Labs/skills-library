---
id: computing-software.database-administration.postgresql.scram-sha-256-password-authentication
name: scram-sha-256-password-authentication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, client-authentication, pg-hba-conf, scram-sha-256, password-encryption, md5-migration, password-authentication, security, md5-to-scram]
level: practitioner
status: verified
description: "Move a PostgreSQL cluster from md5 to SCRAM-SHA-256 password authentication: re-hash passwords, update pg_hba.conf, and handle old drivers that cannot do SCRAM."
sources:
  - https://www.postgresql.org/docs/current/auth-password.html
  - https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
  - https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SCRAM-SHA-256 password authentication

**Goal:** every password is stored and checked with SCRAM; `md5` (deprecated and
being removed) is gone from pg_hba.conf.

## How it fits together
- `password_encryption` decides how **new** passwords are hashed when set
  (`ALTER ROLE ... PASSWORD`). Default `scram-sha-256` since PG14.
- The pg_hba.conf method decides how the client proves it knows it:
  `scram-sha-256` requires a SCRAM verifier; `md5` accepts either an md5 hash or
  (transparently) a SCRAM verifier; `password` sends cleartext — never use.

## Migration procedure
1. Find roles still hashed with md5:
   ```sql
   SELECT rolname FROM pg_authid
   WHERE rolcanlogin AND rolpassword LIKE 'md5%';
   ```
2. Confirm `SHOW password_encryption;` = `scram-sha-256` (set in postgresql.conf + reload if not).
3. Re-set each password (the cleartext must be supplied again; hashes cannot be
   converted). Use psql's `\password <role>` so the cleartext is hashed client-side
   and never appears in logs or `pg_stat_statements`.
4. While both exist, keep `md5` in pg_hba.conf (it accepts SCRAM too).
5. When the query in step 1 returns nothing, change pg_hba.conf lines to
   `scram-sha-256`, then `SELECT pg_reload_conf();`.
   ```
   hostssl  all  all  10.0.0.0/8  scram-sha-256
   ```

## Old clients
SCRAM needs libpq 10 or newer (PostgreSQL 10 introduced it) or a driver that implements SCRAM itself.
An old libpq fails with `authentication method 10 not supported` (older point releases print
`SCRAM authentication requires libpq version 10 or above`). Check each driver's own documentation for its
minimum version, and inventory clients from `pg_stat_activity.application_name`, `usename` and connection logs before step 5.

## Gotchas
- `ALTER ROLE x PASSWORD 'secret'` in plain SQL lands in the server log if
  `log_statement=ddl/all`. Use `\password` or pre-hashed verifiers.
- Poolers: PgBouncer authenticates users from `auth_file` or, for users not listed there, through
  `auth_user` and `auth_query` (see the PgBouncer config docs); check that your pooler version and file hold
  SCRAM secrets before step 5.
- Channel binding (`channel_binding=require` in the client connstring) protects
  against MITM on TLS connections; use it with hostssl.

## Verify
- Step 1 query returns zero rows.
- `grep -nE '^[[:space:]]*[^#[:space:]].*[[:space:]]md5([[:space:]]|$)' pg_hba.conf` returns nothing.
- `SELECT * FROM pg_hba_file_rules WHERE error IS NOT NULL;` is empty after reload.
- Log in with a migrated role from each application host.

## Checked
- PostgreSQL 18.6: `password_encryption` default is `scram-sha-256`; with `SET password_encryption='md5'` role creation printed `WARNING: setting an MD5-encrypted password` / `MD5 password support is deprecated and will be removed in a future release`; `pg_authid` showed `md5...` vs `SCRAM-SHA-256$...` prefixes; the step-1 query `rolcanlogin AND rolpassword LIKE 'md5%'` listed the md5 roles and after `ALTER ROLE ... PASSWORD` under scram it no longer listed that role; a `scram-sha-256` pg_hba line refused a role holding an md5 verifier (`password authentication failed`, log detail `User "scramuser" does not have a valid SCRAM secret.`); an `md5` pg_hba line accepted a role holding a SCRAM verifier; the grep in Verify was run against a pg_hba.conf containing an md5 line (the original `\s`/`\b` form did not match in this grep, so it was replaced with POSIX classes, which matched line 3 and returned nothing for an md5-free file).
- Docs/source: release notes 14 (default `password_encryption` changed to scram-sha-256) and 18 (md5 deprecation), auth-password page (md5 less secure; scram not supported by older client libraries), libpq `fe-auth.c` on REL9_6_STABLE and REL_18_STABLE (the `authentication method %u not supported` and `SCRAM authentication requires libpq version 10 or above` strings), PgBouncer config page (`auth_user`/`auth_query`).
- Removed per-driver and PgBouncer version numbers that could not be confirmed.
