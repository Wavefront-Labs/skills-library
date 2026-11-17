---
id: computing-software.database-administration.supabase.postgres-roles
name: postgres-roles
category: computing-software
field: database-administration
product: supabase
tags: [roles, postgres-roles, grants, service-role, authenticator]
level: practitioner
status: docs-checked
description: "Create per-service Postgres roles in Supabase and know the predefined roles (anon, authenticated, service_role, authenticator) and their jobs."
sources:
  - https://supabase.com/docs/guides/database/postgres/roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give each client or service its own least-privilege database identity.

Roles manage system access; for application access use RLS. A user is a role with login; a group is a role without login.

```sql
create role "role_name";
create role "role_name" with login password 'extremely_secure_password';
REVOKE permission_type ON object_name FROM role_name;
create role "child_role_name" inherit "parent_role_name";
alter role "child_role_name" noinherit;
```

Permissions (SELECT, INSERT, UPDATE, DELETE) are granted with `GRANT` on tables, views, functions and triggers. Child roles inherit permissions from their parent (the page shows the `inherit` option on `create role`, as above). `noinherit` prevents a role having a child relationship, which the page says is typically wanted for superuser roles.

Passwords: at least 12 characters, no dictionary words, mixed case, digits and symbols. Percent-encode special symbols in connection strings.

Practice:
- Never hand the `postgres` password to a third-party service. Create a role per service; this also lets you trace each role's queries in `pg_stat_statements`.
- The project password is the `postgres` role's password; change it under Database Settings in the Dashboard. It causes no downtime: connected Supabase-managed services (PostgREST, the dedicated pooler and others) update automatically, but external services with hardcoded credentials need manual updates.
- A custom role may inherit privileges you did not grant explicitly.

Predefined roles:
- `postgres`: default admin.
- `anon`: API requests that are unauthenticated.
- `authenticator`: limited role that validates a JWT and switches to another role.
- `authenticated`: signed-in API users.
- `service_role`: API role that bypasses RLS.
- `supabase_auth_admin`: used by the Auth middleware to connect and run migrations; scoped to the `auth` schema.
- `supabase_storage_admin`: used by the Storage middleware to connect and run migrations; scoped to the `storage` schema.
- `supabase_etl_admin`: used by Supabase Pipelines for database replication; read-all access, replication privileges, bypasses RLS, can create event triggers and write to the `etl` schema.
- `dashboard_user`: not used by the Dashboard; dashboard queries run as `postgres` with a `-- source: dashboard` comment.
- `supabase_admin`: internal, for administrative tasks such as upgrades and automations.

## Checked

2026-11-04: Read the Postgres Roles guide in full. Confirmed each SQL statement, the password tips, the percent-encoding note, the password-change behaviour, the inheritance text and every predefined role. Reworded the inheritance sentence to the page's, and added the role details the page gives for the Auth, Storage and ETL roles.
Method: documentation only; no commands were run.
