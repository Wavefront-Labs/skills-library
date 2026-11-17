---
id: computing-software.database-administration.clickhouse.rbac-users-roles-and-grants
name: rbac-users-roles-and-grants
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, rbac, grant, revoke, create-user, role, set-role]
level: practitioner
status: docs-checked
description: "Create ClickHouse users and roles, grant minimal privileges, inspect them with SHOW GRANTS and revoke access."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/sre/user-management/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rbac users roles and grants
Manage access with SQL-driven RBAC. Create a user, a role, and grant privileges to the role rather than to each user:
```sql
CREATE USER ana IDENTIFIED BY 'strong-password';
CREATE ROLE analyst;
GRANT SELECT ON db.* TO analyst;
GRANT analyst TO ana;
SET DEFAULT ROLE analyst TO ana;
GRANT ALTER ADD COLUMN ON db.events TO ana;   -- narrow, table-level
GRANT SELECT ON db.events TO ana WITH GRANT OPTION; -- allows re-granting
REVOKE SELECT ON db.events FROM ana;
```
Inspect with `SHOW GRANTS FOR ana`, `SHOW ACCESS` and `SHOW CREATE USER ana`. A session activates roles with `SET ROLE analyst`.

Gotchas: the user granting or revoking must hold `WITH GRANT OPTION` and the privilege itself. `ALTER` privileges are hierarchical for tables and views only; for example `ALTER ROW POLICY` is not a child of `ALTER TABLE` and must be granted explicitly.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Users and roles" (user-management): CREATE USER and GRANT/REVOKE, `WITH GRANT OPTION` rules, `GRANT ALTER ADD COLUMN ON db.table`, SHOW GRANTS, SHOW ACCESS, SHOW CREATE USER, SET ROLE and SET DEFAULT ROLE as listed statements. Removed: advice and the Verify step not stated there.
Method: documentation only; no commands were run.
