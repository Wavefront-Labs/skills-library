---
id: computing-software.database-administration.postgresql.pgbouncer-authentication-auth-query
name: pgbouncer-authentication-auth-query
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-connection-pooling, pgbouncer, pgbouncer-auth-query, auth-user, userlist-txt, auth-type, scram-sha-256, security-definer]
level: practitioner
status: docs-checked
description: "Authenticate PgBouncer clients with userlist.txt or auth_query against pg_authid via a SECURITY DEFINER function, with SCRAM end to end."
sources:
  - https://www.pgbouncer.org/config.html#authentication-settings
  - https://www.pgbouncer.org/config.html#auth_query
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PgBouncer authentication: auth_file and auth_query

**Goal:** clients authenticate to PgBouncer with their own PostgreSQL credentials without hand-maintaining a password file.

## Static: auth_file
```ini
[pgbouncer]
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
```
`userlist.txt` lines: `"app" "SCRAM-SHA-256$4096:...$...:..."` — copy the verifier from `SELECT rolname, rolpassword FROM pg_authid WHERE rolname='app';`. With a SCRAM verifier PgBouncer can authenticate the client and then log into the server as that user (SCRAM pass-through) because it keeps the client's proof keys.

## Dynamic: auth_query
```sql
-- on every database PgBouncer connects to (or the auth_dbname)
CREATE ROLE pgbouncer_auth LOGIN PASSWORD '...';
CREATE SCHEMA pgbouncer AUTHORIZATION pgbouncer_auth;
CREATE FUNCTION pgbouncer.get_auth(p_usename text) RETURNS TABLE(usename name, passwd text)
LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog AS
$$ SELECT rolname, rolpassword FROM pg_authid WHERE rolname = p_usename AND rolcanlogin $$;
REVOKE ALL ON FUNCTION pgbouncer.get_auth(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION pgbouncer.get_auth(text) TO pgbouncer_auth;
```
(the function owner must be a superuser to read `pg_authid`).
```ini
auth_type = scram-sha-256
auth_user = pgbouncer_auth           ; its own password lives in auth_file
auth_file = /etc/pgbouncer/userlist.txt
auth_query = SELECT usename, passwd FROM pgbouncer.get_auth($1)
auth_dbname = postgres                ; run auth_query in one fixed database (added in PgBouncer 1.19.0)
```

## Other auth_type values
The config page lists `hba`, `cert`, `trust`, `md5`, `ldap`, `pam`, `any` and `plain` as further `auth_type` values; read its auth_type section for exact semantics and the default. Never use `trust` in production.

## Gotchas
- Do not grant the auth user superuser or broad read roles; only EXECUTE on the function.
- `SET search_path` on the function closes the classic SECURITY DEFINER hijack.
- After password changes PgBouncer re-queries on next login; existing server connections stay up.
- TLS: set `client_tls_sslmode` and `server_tls_sslmode` separately; see the TLS settings section of the config page for defaults and which modes verify certificates.
- `auth_user` is only consulted for users missing from `auth_file`.

## Verify
`psql "host=pgb port=6432 user=app dbname=app"` succeeds with the role's normal password; a role without LOGIN is rejected.

## Checked

2026-10-28. Confirmed against the PgBouncer config page (auth_type values, auth_user, auth_dbname, auth_query) and changelog (auth_dbname added in 1.19.0; auth_query example updated to set a safe search_path). Corrected: the auth_dbname hedge replaced by the version from the changelog. Removed: auth_type default and per-value behaviour claims, TLS default values, pg_read_all_data and the log-line format (not confirmed in the fetched pages).

Method: documentation only; no commands were run.
