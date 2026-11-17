---
id: computing-software.cybersecurity-defensive.system-hardening.postgresql-hardening
name: postgresql-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-hardening, postgresql-hardening, pg-hba, scram-sha-256, postgres-tls, least-privilege-roles, public-schema]
level: advanced
status: docs-checked
description: "Harden PostgreSQL: listen addresses, pg_hba.conf with scram-sha-256 and hostssl, TLS, least-privilege roles, locked-down public schema and safe extensions."
sources: ["https://www.postgresql.org/docs/current/auth-pg-hba-conf.html", "https://www.postgresql.org/docs/current/auth-password.html", "https://www.postgresql.org/docs/current/ssl-tcp.html", "https://www.postgresql.org/docs/current/runtime-config-connection.html", "https://www.postgresql.org/docs/current/ddl-schemas.html", "https://www.postgresql.org/docs/current/predefined-roles.html", "https://www.postgresql.org/docs/current/view-pg-roles.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL hardening

**Goal:** only expected clients connect, over TLS with strong auth, as roles with minimum privileges.

## Network and auth
`postgresql.conf`:
```
listen_addresses = '10.0.2.15'          # not '*'
password_encryption = scram-sha-256
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_min_protocol_version = 'TLSv1.2'
```
`pg_hba.conf` (first match wins, order matters):
```
# TYPE    DATABASE  USER       ADDRESS         METHOD
local     all       postgres                   peer
hostssl   appdb     app_rw     10.0.3.0/24     scram-sha-256
hostssl   all       +dba       10.250.0.0/24   scram-sha-256
host      all       all        0.0.0.0/0       reject
```
Never use `trust` outside local maintenance; migrate `md5` hashes by resetting passwords after switching `password_encryption`. Reload: `SELECT pg_reload_conf();` and check `SELECT * FROM pg_hba_file_rules;` for errors.

## Roles and privileges
- Apps connect as non-superuser, non-owner roles. Owner role owns schema objects; app role gets `SELECT/INSERT/UPDATE/DELETE` only.
- `REVOKE CREATE ON SCHEMA public FROM PUBLIC;` (default from PG 15) and `REVOKE ALL ON DATABASE appdb FROM PUBLIC;`.
- `ALTER DEFAULT PRIVILEGES` so new tables get the intended grants.
- Audit superusers: `SELECT rolname FROM pg_roles WHERE rolsuper OR rolcreaterole OR rolbypassrls;`.
- Row-level security (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`) for multi-tenant tables.

## Dangerous capabilities
- `COPY ... PROGRAM` and `pg_read_server_files`, `pg_execute_server_program` roles allow OS access; grant to nobody routine.
- Only install needed extensions; untrusted languages (`plpython3u`) superuser-only.
- Set `log_connections`, `log_disconnections`, `log_line_prefix` with user/db/client; consider an audit extension for statement-level auditing.

## Gotchas
- Managed services replace the superuser role with their own admin roles; read the provider's documentation and apply the same least-privilege logic.
- Connection poolers sit between clients and the server and need their own authentication hardening and TLS.

## Verify
- [ ] `psql "sslmode=disable host=db user=app_rw"` is refused.
- [ ] App role cannot `CREATE TABLE` or read other schemas.

## Checked
2026-10-31. Confirmed against the PostgreSQL current documentation: pg_hba.conf record format, `hostssl`, `reject`, `peer`, `+group` role syntax, first matching record wins, reload via `pg_reload_conf()`; SCRAM and the md5-to-scram migration steps; `password_encryption` default; `ssl_min_protocol_version` values (default TLSv1.2); public schema CREATE default change in PostgreSQL 15 and the `REVOKE CREATE ON SCHEMA public FROM PUBLIC` fix for older versions; predefined roles `pg_read_server_files` and `pg_execute_server_program`; `COPY ... PROGRAM`; `pg_roles` columns `rolsuper`, `rolcreaterole`, `rolbypassrls`; `pg_hba_file_rules`; row-level security syntax; `plpython3u`; `log_connections`, `log_disconnections`, `log_line_prefix`. Removed: the CIS benchmark source, named RDS/PgBouncer/pgAudit specifics.
Method: documentation only; no commands were run.
