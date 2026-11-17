---
id: computing-software.database-administration.cockroachdb.users-roles-and-privileges
name: users-roles-and-privileges
category: computing-software
field: database-administration
product: cockroachdb
tags: [authorization, users, roles, grant, revoke, privileges, rbac]
level: practitioner
status: docs-checked
description: "Manage CockroachDB SQL users, roles and privileges with CREATE USER/ROLE, ALTER, GRANT, REVOKE and SHOW GRANTS, including the public role default."
sources:
  - https://www.cockroachlabs.com/docs/stable/authorization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build least-privilege access through roles.

Principles from the page:
- Users and roles are created with `CREATE USER` / `CREATE ROLE`, changed with `ALTER USER` / `ALTER ROLE` (passwords, role options, default session variables), removed with `DROP USER` / `DROP ROLE`.
- A new user belongs to the `public` role and has no privileges other than those given to `public`. Each database and table the user needs must be granted explicitly.
- `GRANT` manages privileges on databases and tables and also adds a user or role as member of a role; `REVOKE` removes privileges or membership.
- Inspect with `SHOW USERS`, `SHOW ROLES` and `SHOW GRANTS`.

Pattern: grant privileges to roles with `GRANT`, and add users to roles with `GRANT` too (the page says `GRANT` also adds a role or user as member of a role). Exact statement syntax lives on the per-statement reference pages, which this skill does not reproduce.

## Checked

2026-11-03. Confirmed against the authorization page: user and role statements, the `public` role default, GRANT and REVOKE roles, `SHOW USERS`, `SHOW ROLES`, `SHOW GRANTS`. Removed: a dangling sentence, the unsourced `admin` gotcha and the invented verification step.
Method: documentation only; no commands were run.
