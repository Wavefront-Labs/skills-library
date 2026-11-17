---
id: computing-software.database-administration.postgresql.role-attributes-and-connection-limits
name: role-attributes-and-connection-limits
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, database-roles, role-attributes, connection-limit, createrole, bypassrls, valid-until, least-privilege]
level: practitioner
status: verified
description: "Set role attributes deliberately (LOGIN, CREATEDB, CREATEROLE, REPLICATION, BYPASSRLS, CONNECTION LIMIT, VALID UNTIL) and audit who has dangerous ones."
sources:
  - https://www.postgresql.org/docs/current/role-attributes.html
  - https://www.postgresql.org/docs/current/sql-createrole.html
  - https://www.postgresql.org/docs/current/sql-alterrole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role attributes and connection limits

Attributes are cluster-wide properties of a role, separate from object privileges, and
**are not inherited** through role membership (a member of a SUPERUSER role is not superuser
unless it `SET ROLE`s).

| Attribute | Grants | Notes |
|---|---|---|
| `LOGIN` | can connect | `CREATE USER` = `CREATE ROLE ... LOGIN` |
| `SUPERUSER` | bypasses all checks | keep to 1-2 break-glass roles |
| `CREATEDB` | create databases | |
| `CREATEROLE` | create/alter/drop roles | PG16+: only roles it created or has `ADMIN OPTION` on; before 16 effectively near-superuser |
| `REPLICATION` | physical/logical replication connections, create slots | needs a `replication` pg_hba line for physical |
| `BYPASSRLS` | ignores row-level security | audit like superuser |
| `INHERIT` (default) | uses privileges of granted roles automatically | PG16: also a per-grant option |
| `CONNECTION LIMIT n` | max concurrent sessions for the role | -1 = unlimited; superusers exempt (a second superuser session was accepted at limit 1) |
| `VALID UNTIL 'ts'` | password expiry | only the **password** expires; peer/cert logins still work (an expired password gives `password authentication failed`, with `User "x" has an expired password.` in the server log) |
| `PASSWORD` | sets password | hashed per `password_encryption` |

## Common setups
```sql
CREATE ROLE app_owner NOLOGIN;                         -- owns schema objects, nobody logs in as it
CREATE ROLE app LOGIN PASSWORD '...' CONNECTION LIMIT 200 IN ROLE app_rw;
CREATE ROLE replicator LOGIN REPLICATION PASSWORD '...';
CREATE ROLE contractor LOGIN PASSWORD '...' VALID UNTIL '2026-12-31';
CREATE ROLE dba_ops LOGIN CREATEROLE CREATEDB;         -- day-to-day admin without SUPERUSER
ALTER ROLE app CONNECTION LIMIT 300;
ALTER ROLE contractor VALID UNTIL 'infinity';
```

## Audit
```sql
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolreplication, rolbypassrls,
       rolcanlogin, rolconnlimit, rolvaliduntil
FROM pg_roles
WHERE rolsuper OR rolcreaterole OR rolreplication OR rolbypassrls
ORDER BY rolname;
```
Also check per-role settings that change behaviour: `SELECT * FROM pg_db_role_setting;`.

## Gotchas
- Connection limits count per role across all databases; pooled apps hit them under
  load spikes with `FATAL: too many connections for role "app"`.
- Superuser connections still count against `max_connections` but use the
  `superuser_reserved_connections` slots (and PG16 `reserved_connections` for
  `pg_use_reserved_connections` members).
- `VALID UNTIL` with no timezone is read in the TimeZone of the session running the statement (the same date stored as `00:00+10` from a UTC+10 session and `01:00+10` from a Tokyo one); write timestamps with an offset.
- Managed services restrict SUPERUSER and provide their own admin roles; read your provider's documentation for what they map to.

## Verify
`\du+` in psql lists attributes; test a limited role cannot exceed its connection limit and
that an expired password is refused with `password authentication failed`.

## Checked
PostgreSQL 17.6: `CREATE ROLE ... IN ROLE`, `LOGIN REPLICATION`, `CREATEROLE CREATEDB`, `VALID UNTIL 'infinity'` work; a member of a SUPERUSER role has `rolsuper = f` and `is_superuser = off`; a `CREATEROLE` role can create a role and alter it, but `ALTER ROLE app` and `DROP ROLE replicator` fail with `Only roles with the CREATEROLE attribute and the ADMIN option on role ... may ...` and `CREATE ROLE x SUPERUSER` is refused; with `CONNECTION LIMIT 1` a session in another database was refused with `FATAL: too many connections for role "app"`; `superuser_reserved_connections` is 3, `reserved_connections` 0 and `pg_use_reserved_connections` exists (PG16+); with a scram `pg_hba` line, a role whose `VALID UNTIL` was in 2020 was refused and the same login worked after resetting it to `infinity`. PG16 release notes for the CREATEROLE change; role-attributes docs for the inherit and connection-limit rows. `password_encryption` defaults to `scram-sha-256`.
